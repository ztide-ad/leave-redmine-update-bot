examples = [
    {
        "input": "Update the issue ID 5 to priority high and subject 'App crashed' and description 'Nothing is working now'.",
        "json": {
            "issue": {
                "priority_id": 3,
                "subject": "App crashed",
                "description": "Nothing is working now"
            }
        }
    },
    {
        "input": "Set the priority of issue ID 2 to Low.",
        "json": {
            "issue": {
                "priority_id": 1
            }
        }
    },
    {
        "input": "Change the status of issue ID 10 to In Progress.",
        "json": {
            "issue": {
                "status_id": 2
            }
        }
    },
    {
        "input": "Assign issue ID 15 to the user with ID 7.",
        "json": {
            "issue": {
                "assigned_to_id": 7
            }
        }
    },
    {
        "input": "Update the issue with ID 20 to have a due date of '1st August 2024.'",
        "json": {
            "issue": {
                "due_date": "2024-08-01"
            }
        }
    },
    {
        "input": "Set the done ratio of issue ID 25 to 75%.",
        "json": {
            "issue": {
                "done_ratio": 75
            }
        }
    },
    {
        "input": "In issue ID 8 change priority to low",
        "json": {
            "issue": {
                "priority_id": 1
            }
        }
    },
    {
        "input": "Set the estimated hours of issue ID 12 to 10 hours.",
        "json": {
            "issue": {
                "estimated_hours": 10.0
            }
        }
    }
]

