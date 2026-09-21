from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================
# SMARTBUILD - SMART BUILDING MANAGEMENT SYSTEM
# Local Backend API
# ============================================================

# ------------------------------------------------------------
# DEMO DATA
# Later these will be stored in AWS DynamoDB
# ------------------------------------------------------------

building = {
    "name": "Green Valley Residency",
    "city": "Ahmedabad",
    "state": "Gujarat",
    "total_residents": 120,
    "total_flats": 60,
    "occupied_flats": 52,
    "total_lifts": 2
}

monitoring = {
    "electricity": {
        "today": 68.5,
        "unit": "kWh",
        "status": "Normal"
    },
    "water": {
        "level": 72,
        "unit": "%",
        "status": "Normal"
    },
    "temperature": {
        "value": 28,
        "unit": "°C",
        "status": "Normal"
    },
    "occupancy": {
        "value": 86,
        "unit": "%",
        "status": "Normal"
    }
}

residents = [
    {
        "id": 1,
        "name": "Rahul Patel",
        "flat": "A-101",
        "phone": "9876543210",
        "status": "Active"
    },
    {
        "id": 2,
        "name": "Priya Shah",
        "flat": "A-202",
        "phone": "9876543211",
        "status": "Active"
    },
    {
        "id": 3,
        "name": "Amit Mehta",
        "flat": "B-301",
        "phone": "9876543212",
        "status": "Active"
    },
    {
        "id": 4,
        "name": "Neha Joshi",
        "flat": "B-402",
        "phone": "9876543213",
        "status": "Inactive"
    }
]

complaints = [
    {
        "id": 1001,
        "title": "Water Leakage",
        "flat": "A-203",
        "resident": "Raj Patel",
        "priority": "High",
        "status": "Pending",
        "date": "2026-09-20"
    },
    {
        "id": 1002,
        "title": "Lift Noise",
        "flat": "B-101",
        "resident": "Neha Shah",
        "priority": "Medium",
        "status": "In Progress",
        "date": "2026-09-19"
    },
    {
        "id": 1003,
        "title": "Parking Issue",
        "flat": "A-405",
        "resident": "Karan Patel",
        "priority": "Low",
        "status": "Resolved",
        "date": "2026-09-18"
    }
]

lifts = [
    {
        "id": 1,
        "name": "Lift A",
        "location": "Block A",
        "status": "Operational",
        "floor": 4,
        "last_service": "2026-09-10"
    },
    {
        "id": 2,
        "name": "Lift B",
        "location": "Block B",
        "status": "Maintenance",
        "floor": 2,
        "last_service": "2026-08-25"
    }
]

alerts = [
    {
        "id": 1,
        "type": "Water",
        "message": "Water tank level is below normal range.",
        "severity": "Medium",
        "time": "10 minutes ago"
    },
    {
        "id": 2,
        "type": "Security",
        "message": "Unusual movement detected at Gate 2.",
        "severity": "High",
        "time": "25 minutes ago"
    }
]

notices = [
    {
        "id": 1,
        "title": "Monthly Maintenance",
        "message": "Monthly maintenance payment is due before 10th.",
        "date": "2026-09-01"
    },
    {
        "id": 2,
        "title": "Water Tank Cleaning",
        "message": "Water tank cleaning scheduled for Sunday.",
        "date": "2026-09-20"
    }
]


# ============================================================
# BASIC ROUTES
# ============================================================

@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "SmartBuild API is running",
        "project": "Smart Building Management System"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    pending_complaints = len([
        c for c in complaints
        if c["status"] != "Resolved"
    ])

    active_alerts = len(alerts)

    return jsonify({
        "success": True,
        "building": building,
        "monitoring": monitoring,
        "statistics": {
            "residents": len(residents),
            "complaints": pending_complaints,
            "alerts": active_alerts,
            "lifts": len(lifts)
        }
    })


# ============================================================
# MONITORING
# ============================================================

@app.route("/api/monitoring", methods=["GET"])
def get_monitoring():

    return jsonify({
        "success": True,
        "data": monitoring
    })


# ============================================================
# RESIDENTS
# ============================================================

@app.route("/api/residents", methods=["GET"])
def get_residents():

    return jsonify({
        "success": True,
        "count": len(residents),
        "data": residents
    })


@app.route("/api/residents", methods=["POST"])
def add_resident():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data"
        }), 400

    new_resident = {
        "id": len(residents) + 1,
        "name": data.get("name"),
        "flat": data.get("flat"),
        "phone": data.get("phone"),
        "status": "Active"
    }

    residents.append(new_resident)

    return jsonify({
        "success": True,
        "message": "Resident added successfully",
        "data": new_resident
    }), 201


# ============================================================
# COMPLAINTS
# ============================================================

@app.route("/api/complaints", methods=["GET"])
def get_complaints():

    return jsonify({
        "success": True,
        "count": len(complaints),
        "data": complaints
    })


@app.route("/api/complaints", methods=["POST"])
def create_complaint():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request"
        }), 400

    new_complaint = {
        "id": 1000 + len(complaints) + 1,
        "title": data.get("title", "General Complaint"),
        "flat": data.get("flat", ""),
        "resident": data.get("resident", ""),
        "priority": data.get("priority", "Medium"),
        "status": "Pending",
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    complaints.append(new_complaint)

    return jsonify({
        "success": True,
        "message": "Complaint created successfully",
        "data": new_complaint
    }), 201


@app.route("/api/complaints/<int:complaint_id>", methods=["PUT"])
def update_complaint(complaint_id):

    data = request.get_json()

    for complaint in complaints:

        if complaint["id"] == complaint_id:

            if "status" in data:
                complaint["status"] = data["status"]

            if "priority" in data:
                complaint["priority"] = data["priority"]

            return jsonify({
                "success": True,
                "message": "Complaint updated",
                "data": complaint
            })

    return jsonify({
        "success": False,
        "message": "Complaint not found"
    }), 404


# ============================================================
# LIFTS
# ============================================================

@app.route("/api/lifts", methods=["GET"])
def get_lifts():

    return jsonify({
        "success": True,
        "count": len(lifts),
        "data": lifts
    })


@app.route("/api/lifts/<int:lift_id>", methods=["PUT"])
def update_lift(lift_id):

    data = request.get_json()

    for lift in lifts:

        if lift["id"] == lift_id:

            if "status" in data:
                lift["status"] = data["status"]

            if "floor" in data:
                lift["floor"] = data["floor"]

            return jsonify({
                "success": True,
                "message": "Lift updated",
                "data": lift
            })

    return jsonify({
        "success": False,
        "message": "Lift not found"
    }), 404


# ============================================================
# SECURITY ALERTS
# ============================================================

@app.route("/api/alerts", methods=["GET"])
def get_alerts():

    return jsonify({
        "success": True,
        "count": len(alerts),
        "data": alerts
    })


@app.route("/api/alerts", methods=["POST"])
def create_alert():

    data = request.get_json()

    new_alert = {
        "id": len(alerts) + 1,
        "type": data.get("type", "General"),
        "message": data.get("message", ""),
        "severity": data.get("severity", "Low"),
        "time": "Just now"
    }

    alerts.append(new_alert)

    return jsonify({
        "success": True,
        "message": "Alert created",
        "data": new_alert
    }), 201


# ============================================================
# NOTICES
# ============================================================

@app.route("/api/notices", methods=["GET"])
def get_notices():

    return jsonify({
        "success": True,
        "count": len(notices),
        "data": notices
    })


@app.route("/api/notices", methods=["POST"])
def create_notice():

    data = request.get_json()

    new_notice = {
        "id": len(notices) + 1,
        "title": data.get("title", ""),
        "message": data.get("message", ""),
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    notices.append(new_notice)

    return jsonify({
        "success": True,
        "message": "Notice created successfully",
        "data": new_notice
    }), 201


# ============================================================
# REPORT
# ============================================================

@app.route("/api/reports", methods=["GET"])
def reports():

    return jsonify({
        "success": True,
        "report": {
            "total_residents": len(residents),
            "total_complaints": len(complaints),
            "pending_complaints": len([
                c for c in complaints
                if c["status"] != "Resolved"
            ]),
            "total_alerts": len(alerts),
            "operational_lifts": len([
                l for l in lifts
                if l["status"] == "Operational"
            ]),
            "maintenance_lifts": len([
                l for l in lifts
                if l["status"] == "Maintenance"
            ])
        }
    })


# ============================================================
# 404 HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "message": "API endpoint not found"
    }), 404


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("==============================================")
    print("     SMARTBUILD BACKEND SERVER")
    print("==============================================")
    print("API Server : http://127.0.0.1:5000")
    print("Health     : http://127.0.0.1:5000/api/health")
    print("Dashboard  : http://127.0.0.1:5000/api/dashboard")
    print("==============================================")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

