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

