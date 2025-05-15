from flask import Flask, jsonify, request, Response
from datetime import datetime
import os

app = Flask(__name__)

# Default Configuration (Environment-Aware)
ENROLLMENT_DAYS = os.getenv("ENROLLMENT_DAYS", "Monday,Wednesday,Friday").split(",")
START_TIME = os.getenv("START_TIME", "10:00 AM")
END_TIME = os.getenv("END_TIME", "3:00 PM")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "API is running", 
        "endpoints": ["/check_enrollment_hours", "/set_enrollment_hours"]
    })

@app.route('/check_enrollment_hours', methods=['GET'])
def check_enrollment_hours():
    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%A")
    current_time = current_datetime.time()
    
    # Check if the current day is an enrollment day
    is_enrollment_day = current_day in ENROLLMENT_DAYS

    # Parse start and end times for enrollment hours
    start_time = datetime.strptime(START_TIME, "%I:%M %p").time()
    end_time = datetime.strptime(END_TIME, "%I:%M %p").time()

    # Check if current time is within enrollment hours
    is_enrollment_time = start_time <= current_time <= end_time

    # Final result based on both conditions
    is_within_hours = is_enrollment_day and is_enrollment_time
    
    # Directly returning these details for Retell AI
    return jsonify({
        "is_enrollment_day": is_enrollment_day,
        "is_enrollment_time": is_enrollment_time,
        "is_within_hours": is_within_hours,
        "current_day": current_day,
        "current_time": current_datetime.strftime("%I:%M %p"),
        "enrollment_days": ENROLLMENT_DAYS,
        "enrollment_hours": f"{START_TIME} to {END_TIME}"
    })

@app.route('/set_enrollment_hours', methods=['POST'])
def set_enrollment_hours():
    try:
        data = request.get_json()
        global ENROLLMENT_DAYS, START_TIME, END_TIME
        
        # Update enrollment days and hours
        ENROLLMENT_DAYS = data.get("enrollment_days", ENROLLMENT_DAYS)
        START_TIME = data.get("start_time", START_TIME)
        END_TIME = data.get("end_time", END_TIME)
        
        return jsonify({
            "message": "Enrollment settings updated successfully.",
            "enrollment_days": ENROLLMENT_DAYS,
            "enrollment_hours": f"{START_TIME} to {END_TIME}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    
# This part is crucial for Vercel serverless deployment
app.debug = False
