import re
import json
import re

days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def parse_slot(slot):
    match = re.search(r'(\d{1,2})[.:](\d{2})\s*(AM|PM)\s*-\s*(\d{1,2})[.:](\d{2})\s*(AM|PM)', slot, re.IGNORECASE)
    if not match:
        return "Off"
    return f"{match.group(1).zfill(2)}:{match.group(2)} {match.group(3).upper()} - {match.group(4).zfill(2)}:{match.group(5)} {match.group(6).upper()}"

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
    # Remove ObjectId wrapper
    entry["_id"] = str(entry.get("_id", {}).get("$oid", ""))

    # Normalize name, designation, etc.
    entry["name"] = entry["name"].strip()
    entry["designation"] = entry["designation"].strip()
    entry["specialization"] = entry["specialization"].strip()
    entry["reg_no"] = entry.get("reg_no", "N/A").strip()

    # Normalize availability
    entry["availability"] = group_availability_exact(entry.get("availability", []))# if a.strip()

    # Normalize tags as a single string
    entry["tags"] = ', '.join(tag.strip() for tag in entry.get("tags", []))

    # Normalize hospital info
    entry["hospital_info"] = entry["hospital_info"].strip()
    entry["hospital_address"] = re.sub(r'\s+', ' ', entry["hospital_address"]).strip()

    # Normalize URLs
    entry["doctor_url"] = entry["doctor_url"].strip()
    entry["hospital_url"] = entry["hospital_url"].strip()

    # Normalize years of experience
    entry["yoe"] = int(entry["yoe"]) if entry["yoe"].isdigit() else None

    return preprocess_doc_info_for_vector_db(entry)
def preprocess_doc_info_for_vector_db(doc):
    text = (
        f"{doc['name']} is a {doc['specialization']} with {doc['yoe']} years of experience. "
        f"He holds the qualifications {doc['designation']}. "
        f"Currently practicing at {doc['hospital_info']} located at {doc['hospital_address']}. "
        f"Availability: {'; '.join(doc['availability'])}. "
        f"Expertise includes {doc['tags']}."
    )

    return {
        "id": doc["_id"],
        "text": text,
        "metadata": {
            "name": doc["name"],
            "specialization": doc["specialization"],
            "yoe": doc["yoe"],
            "tags": [t.strip() for t in doc["tags"].split(",")],
            "designation": doc["designation"],
            "hospital": doc["hospital_info"],
            "hospital_address": doc["hospital_address"],
            "availability": doc["availability"]
        }
    }
if __name__ == "__main__":
    # Example usage
    sample_doc = {
    "_id": {
        "$oid": "67fe06cf13b6d75e7dd15d48"
    },
    "doctor_url": "https://www.doctorspedia.co/doctor/dr-md-forhad-jamal",
    "availability": [
        "sun 06.00 PM - 09.00 PM",
        "mon 06.00 PM - 09.00 PM",
        "tue 06.00 PM - 09.00 PM",
        "wed 06.00 PM - 09.00 PM",
        "thu 06.00 PM - 09.00 PM",
        "",
        "sat 06.00 PM - 09.00 PM"
    ],
    "designation": "MBBS, FCPS(Medicine), MD(Cardiology)",
    "hospital_address": "C-287/2-3 , Bishwa Road, Khilgaon, Dhaka, 1219, Bangladesh",
    "hospital_info": "Khidmah Hospital Private Limited",
    "name": "Dr. Md. Forhad Jamal",
    "reg_no": "N/A",
    "tags": [
        "Angioplasty",
        "Cardioversion",
        "Non-Invasive Cardiology",
        "BP Monitoring",
        "Echocardiography",
        "Aortic Valve Surgery",
        "Chest Pain",
        "ECHO",
        "Heart Disease",
        "Coronary",
        "Heart Attacks",
        "Dyslipidemia",
        "Heart Valve Disease",
        "Blood Pressure",
        "Stress",
        "Stenting",
        "Color doppler"
    ],
    "yoe": "18",
    "hospital_url": "https://www.doctorspedia.co/hospital/khidmah-hospital-private-limited",
    "specialization": "Cardiologist (Heart)"
    }

    normalized = normalize_doctor_entry(sample_doc)
    print(json.dumps(normalized, indent=2))
