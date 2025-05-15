from flask import Flask, jsonify, Response
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running", "endpoints": ["/check_enrollment_hours"]})

@app.route('/check_enrollment_hours', methods=['GET'])
def check_enrollment_hours():
    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%A")
    current_time = current_datetime.time()
    
    enrollment_days = ["Monday", "Wednesday", "Friday"]
    start_time = datetime.strptime("10:00 AM", "%I:%M %p").time()
    end_time = datetime.strptime("3:00 PM", "%I:%M %p").time()

    is_enrollment_day = current_day in enrollment_days
    is_enrollment_time = start_time <= current_time <= end_time
    is_within_hours = is_enrollment_day and is_enrollment_time
    
    return jsonify({
        "is_within_hours": is_within_hours,
        "is_enrollment_day": is_enrollment_day,
        "is_enrollment_time": is_enrollment_time,
        "current_day": current_day,
        "current_time": current_datetime.strftime("%I:%M %p"),
        "enrollment_days": enrollment_days,
        "enrollment_hours": "10:00 AM to 3:00 PM",
        "reason": "Not an enrollment day" if not is_enrollment_day else 
                  "Outside enrollment hours" if not is_enrollment_time else 
                  "Enrollment is currently open"
    })

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    
# This part is crucial for Vercel serverless deployment
app.debug = False
