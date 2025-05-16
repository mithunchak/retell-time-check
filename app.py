from flask import Flask, jsonify, request
from datetime import datetime
import os
import pytz  # For timezone support

app = Flask(__name__)

# Default Configuration (Environment-Aware)
ENROLLMENT_DAYS = os.getenv("ENROLLMENT_DAYS", "Monday,Wednesday,Friday").split(",")
START_TIME = os.getenv("START_TIME", "10:00 AM")
END_TIME = os.getenv("END_TIME", "3:00 PM")
TIMEZONE = "Asia/Kolkata"  # Set to India Standard Time (GMT+5:30)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "API is running", 
        "endpoints": ["/check_enrollment_availability"]
    })

@app.route('/check_enrollment_availability', methods=['GET', 'POST'])
def check_enrollment_availability():
    try:
        timezone = pytz.timezone(TIMEZONE)
        current_datetime = datetime.now(timezone)
        current_day = current_datetime.strftime("%A")
        current_time = current_datetime.time()
        
        # Check if the current day is an enrollment day
        is_enrollment_day = current_day in ENROLLMENT_DAYS
        
        # Parse start and end times for enrollment hours
        start_time = datetime.strptime(START_TIME, "%I:%M %p").time()
        end_time = datetime.strptime(END_TIME, "%I:%M %p").time()
        
        # Check if current time is within enrollment hours
        is_enrollment_time = start_time <= current_time <= end_time
        
        # Single boolean response that's true only if both conditions are met
        is_correct_time_to_enroll = is_enrollment_day and is_enrollment_time
        
        # Format response for Retell AI
        return jsonify({
            "is_correct_time_to_enroll": is_correct_time_to_enroll,
            "enrollment_days": ENROLLMENT_DAYS,
            "enrollment_hours": f"{START_TIME} to {END_TIME}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
