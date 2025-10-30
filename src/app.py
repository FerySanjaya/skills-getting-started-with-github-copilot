"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports-related activities
    "Soccer Team": {
        "description": "Competitive soccer team practice and matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "lisa@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and intramural tournaments",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["maria@mergington.edu", "kevin@mergington.edu"]
    },
    # Artistic activities
    "Art Club": {
        "description": "Drawing, painting, and mixed-media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "gabe@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, rehearsals, and school plays",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["harper@mergington.edu", "leo@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Debate techniques, research, and interschool competitions",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["sam@mergington.edu", "maya@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Hands-on STEM challenges and contest preparation",
        "schedule": "Saturdays, 9:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": ["ryan@mergington.edu", "zoe@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(
    activity_name: str,
    email: str = Query(..., description="The email of the student to sign up", examples=["student@mergington.edu"])
):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")  

    # Add student
    activity["participants"].append(email)
    return JSONResponse(
        status_code=200,
        content={"message": f"Signed up {email} for {activity_name}"}
    )

@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(
    activity_name: str,
    email: str = Query(..., description="The email of the student to unregister", examples=["student@mergington.edu"])
):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Get the activity
    activity = activities[activity_name]
    
    # Validate student is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not registered for this activity")
    
    # Remove student
    activity["participants"].remove(email)
    return JSONResponse(
        status_code=200,
        content={"message": f"Unregistered {email} from {activity_name}"}
    )
