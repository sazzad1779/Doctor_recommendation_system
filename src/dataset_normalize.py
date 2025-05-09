import re
import json

days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def parse_slot(slot):
    match = re.search(r'(\d{1,2})[.:](\d{2})\s*(AM|PM)\s*-\s*(\d{1,2})[.:](\d{2})\s*(AM|PM)', slot, re.IGNORECASE)
    if not match:
        return "Off"
    return f"{match.group(1).zfill(2)}:{match.group(2)} {match.group(3).upper()} - {match.group(4).zfill(2)}:{match.group(5)} {match.group(6).upper()}"
def infer_specialization_from_fields(designation, tags):
    designation_lower = designation.lower()
    tags_combined = ", ".join(tags).lower() if isinstance(tags, list) else str(tags).lower()

    # Gynaecologist
    if any(term in designation_lower for term in ["g & o", "g&o", "obstetrics", "mrcog", "obg"]) or \
       any(term in tags_combined for term in ["gynae problems", "gynaecology", "obstetric"]):
        return "Gynaecologist (Obstetric)"
    
    # Oncologist
    elif "stem cell transplantation" in tags_combined or any(tag.strip().lower().endswith("cancer") for tag in tags):
        return "Oncologist (Cancer)"

    # # Orthopedic
    elif "nephro" in designation_lower or "adult nephrology" in tags_combined :
        return "Nephrologist (Kidney)"
    elif "neuro" in designation_lower :
        return "Neurologist"
    elif "(orthopaedics)" in designation_lower or "ortho" in designation_lower:
        return "Orthopedist"

    # # Plastic Surgery
    elif "plastic" in designation_lower:
        return "Plastic Surgeon"
    elif "geriatric ophthalmology" in tags_combined:
        return "Ophthalmologist (Eye)"

    # # General Surgery
    elif "ms (surgery)" in designation_lower or "(general surgery)" in designation_lower:
        return "General Surgeon"

    # # Internal Medicine
    elif "medicine" in designation_lower or "diabetes in children" in tags_combined or "childhood infections" in tags_combined:
        return "Medicine Specialist"
    elif "diabetic diet counseling" in tags_combined:
        return "Diabetologists"
    elif "endoscopic surgery" in tags_combined:
        return "Surgeon"
    elif "neuro surgery" in tags_combined:
        return "Neuro Surgeon"
    elif "spinal cord injury treatment" in tags_combined:
        return "Orthopedic Surgeon"
    elif  "maxillofacial surgery" in designation_lower:
        return "Dentist (Maxillofacial)"
    return "General Practitioner"


def group_availability_exact(availability_raw):
    # Reorder to Bangladeshi week (Sat to Fri)
    availability_raw = [availability_raw[6]] + availability_raw[:6]

    # Convert to list of (day, time)
    time_slots = []
    for i, raw in enumerate(availability_raw):
        day = days[i]
        time = parse_slot(raw.strip()) if raw.strip() else "Off"
        time_slots.append((day, time))

    # Group by consecutive same time
    groups = []
    prev_time = None
    current_group = []

    for day, time in time_slots + [("END", None)]:
        if time == prev_time:
            current_group.append(day)
        else:
            if current_group:
                groups.append((current_group, prev_time))
            current_group = [day]
            prev_time = time

    # Format groups into readable ranges
    readable = []
    for group, time in groups:
        if len(group) == 1:
            readable.append(f"{group[0]}: {time}")
        elif len(group) == 2:
            readable.append(f"{group[0]} & {group[1]}: {time}")
        else:
            readable.append(f"{group[0]} to {group[-1]}: {time}")
    return readable



def normalize_doctor_entry(entry):
    _id_val = entry.get("_id")
    entry["_id"] = _id_val["$oid"] if isinstance(_id_val, dict) and "$oid" in _id_val else str(_id_val)

    entry["name"] = entry.get("name", "Unknown Doctor").strip()
    entry["designation"] = entry.get("designation", "N/A").strip()
    # entry["specialization"] = entry.get("specialization", "General Practitioner").strip()
    specialization = entry.get("specialization", "").strip()
    if not specialization:
        specialization = infer_specialization_from_fields(
            entry.get("designation", ""),
            entry.get("tags", [])
        )
    entry["specialization"] = specialization
    entry["reg_no"] = entry.get("reg_no", "N/A").strip()

    # Availability: fill with 7 empty strings if missing or malformed
    availability_raw = entry.get("availability", [])
    if not isinstance(availability_raw, list) or len(availability_raw) != 7:
        availability_raw = [""] * 7
    entry["availability"] = group_availability_exact(availability_raw)

    # Tags: handle both list and comma string
    raw_tags = entry.get("tags", [])
    if isinstance(raw_tags, str):
        tags_list = [tag.strip() for tag in raw_tags.split(",")]
    else:
        tags_list = [tag.strip() for tag in raw_tags]
    entry["tags"] = ", ".join(tags_list)

    entry["hospital_info"] = entry.get("hospital_info", "Unknown Hospital").strip()
    entry["hospital_address"] = re.sub(r'\s+', ' ', entry.get("hospital_address", "Unknown Address")).strip()
    entry["doctor_url"] = entry.get("doctor_url", "").strip()
    entry["hospital_url"] = entry.get("hospital_url", "").strip()
    entry["yoe"] = int(entry["yoe"]) if str(entry.get("yoe", "")).isdigit() else None

    return preprocess_doc_info_for_vector_db(entry)

def preprocess_doc_info_for_vector_db(doc):
    text = (
        f"{doc['name']} is a {doc['specialization']} with {doc['yoe']} years of experience. "
        f"He holds the qualifications {doc['designation']}. "
        f"Currently practicing at {doc['hospital_info']} located at {doc['hospital_address']}. "
        f"Availability: {'; '.join(doc['availability'])}. "
        f"Expertise includes {doc['tags']}."
        f"For more information about {doc['hospital_info']}, please visit {doc['hospital_url']}"
    )
    tags = [t.strip() for t in doc["tags"].split(",")]
    availability = doc["availability"]
    return {
        "text": text,
        "metadata": {
            "id": doc["_id"],
            "name": doc["name"],
            "specialization": doc["specialization"],
            "yoe": doc["yoe"],
            "tags": f"{tags}",
            "designation": doc["designation"],
            "hospital": doc["hospital_info"],
            "hospital_address": doc["hospital_address"],
            "hospital_url":doc["hospital_url"],
            "availability": f"{availability}"
        }
    }
def batch_process_doctors(raw_docs):
    processed_docs = []
    for idx, doc in enumerate(raw_docs):
        try:
            processed = normalize_doctor_entry(doc)
            processed_docs.append(processed)
        except KeyError as e:
            doc_id = doc.get("_id", f"index {idx}")
            doc_name = doc.get("name", "UNKNOWN")
            print(f"[Error] Skipped doc at index {idx} (ID: {doc_id}, Name: {doc_name}) — missing field: {e}")
        except IndexError as e:
            print(f"[Error] Skipped doc at index {idx} — list index error: {e}")
        except Exception as e:
            print(f"[Error] Skipped doc at index {idx} — unexpected error: {e}")
    return processed_docs

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_path = "sample.json"
    output_path = "processed_doctors_for_indexing.json"

    raw_data = load_json_file(input_path)
    processed_data = batch_process_doctors(raw_data)
    print(processed_data)
    save_json_file(processed_data, output_path)

    print(f"Processed {len(processed_data)} out of {len(raw_data)} records.")
