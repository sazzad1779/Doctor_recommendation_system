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
  "text": "Dr. Md. Forhad Jamal is a Cardiologist (Heart) with 18 years of experience. He holds the qualifications MBBS, FCPS(Medicine), MD(Cardiology). Currently practicing at Khidmah Hospital Private Limited located at C-287/2-3 , Bishwa Road, Khilgaon, Dhaka, 1219, Bangladesh. Availability: Saturday to Thursday: 06:00 PM - 09:00 PM; Friday: Off. Expertise includes Angioplasty, Cardioversion, Non-Invasive Cardiology, BP Monitoring, Echocardiography, Aortic Valve Surgery, Chest Pain, ECHO, Heart Disease, Coronary, Heart Attacks, Dyslipidemia, Heart Valve Disease, Blood Pressure, Stress, Stenting, Color doppler.",
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

