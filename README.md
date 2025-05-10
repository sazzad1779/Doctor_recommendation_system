# Doctor_recommendation_system

### dataset Normalize 
1. availability field normalize:
```python
# convert to simplified format
## dataset format
"availability": [
    "sun 06.00 PM - 09.00 PM",
    "mon 06.00 PM - 09.00 PM",
    "tue 06.00 PM - 09.00 PM",
    "wed 06.00 PM - 09.00 PM",
    "thu 06.00 PM - 09.00 PM",
    "",
    "sat 06.00 PM - 09.00 PM"
  ]

  ## simplified format
  "availability": [
    "Saturday to Thursday: 06:00 PM - 09:00 PM",
    "Friday: Off"
  ]
```


```python
## this is a dataset sample
  {
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

## this is preprocessed sample for RAG system
{
  "id": "67fe06cf13b6d75e7dd15d48",
  "text": "Dr. Md. Forhad Jamal is a Cardiologist (Heart) with 18 years of experience. He holds the qualifications MBBS, FCPS(Medicine), MD(Cardiology). Currently practicing at Khidmah Hospital Private Limited located at C-287/2-3 , Bishwa Road, Khilgaon, Dhaka, 1219, Bangladesh. Availability: Saturday to Thursday: 06:00 PM - 09:00 PM; Friday: Off. Expertise includes Angioplasty, Cardioversion, Non-Invasive Cardiology, BP Monitoring, Echocardiography, Aortic Valve Surgery, Chest Pain, ECHO, Heart Disease, Coronary, Heart Attacks, Dyslipidemia, Heart Valve Disease, Blood Pressure, Stress, Stenting, Color doppler.For more information about Khidmah Hospital Private Limited, please visit https://www.doctorspedia.co/hospital/khidmah-hospital-private-limited",
  "metadata": {
    "name": "Dr. Md. Forhad Jamal",
    "specialization": "Cardiologist (Heart)",
    "yoe": 18,
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
    "designation": "MBBS, FCPS(Medicine), MD(Cardiology)",
    "hospital": "Khidmah Hospital Private Limited",
    "hospital_address": "C-287/2-3 , Bishwa Road, Khilgaon, Dhaka, 1219, Bangladesh",
    "availability": [
      "Saturday to Thursday: 06:00 PM - 09:00 PM",
      "Friday: Off"
    ]
  }
}

```

## Optimization scope
This doctor recommendation system, while functional, has several areas identified for potential optimization and enhancement:

1.  **Intelligent Symptom Narrowing and Conversational Flow:**
    * Currently, the system might directly query the retrieval system based on the initial user input. To improve the conversational experience and refine the search, future development will focus on implementing a mechanism to first **narrow down the user's symptoms and other specifications through conversational turns** before triggering the doctor retrieval. This could involve asking clarifying questions to better understand the user's needs.
    * The current approach of calling the retrieval system on every turn can be optimized by potentially using **Langchain Agents and Tools**. An agent could be designed to decide when it's necessary to invoke the retrieval tool based on the level of information gathered conversationally.

2.  **Enhanced Retrieval System:**
    * The retrieval system, which currently relies on vector similarity search, can be improved by incorporating a **keyword-based search mechanism**. This hybrid approach could enhance recall by matching explicit terms in the user's query with relevant keywords in the doctor data, especially for specific conditions or specializations.

3.  **Query Normalization for Intent Understanding:**
    * To better understand the user's intent, the incoming queries need to be **normalized**. This involves techniques like stemming, lemmatization, and handling synonyms to ensure that variations in user language are mapped to consistent representations for more accurate retrieval.

4.  **Optimized Vector Database:**
    * The current vector database can potentially be replaced with a **more optimized database** that offers better performance in terms of indexing speed, query latency, and scalability for the specific needs of this application. Evaluating alternatives like Milvus, Weaviate, or specialized cloud-based vector search services could be beneficial.

5.  **Preprocessing Pipeline Optimization:**
    * The preprocessing steps involved in preparing the doctor data for the vector database can be further **optimized** to improve efficiency and the quality of the embeddings generated. This could involve refining data cleaning techniques, text chunking strategies, and embedding model selection.

6.  **Fallback and Guardrails:**
    * To enhance the robustness and user experience, the system should include **Fallback mechanisms** to handle cases where no relevant doctors are found or the user's query is unclear. Additionally, **Guardrails** should be implemented to prevent the system from providing inappropriate or harmful medical advice, ensuring it strictly adheres to its role as a recommendation system based on the provided data.