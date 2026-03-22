from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import eventlet
eventlet.monkey_patch()
from scraper import get_all_opportunities
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

opportunities = []

def refresh_opportunities():
    global opportunities
    opportunities = get_all_opportunities()
    socketio.emit("new_opportunities", opportunities)
    print(f"Pushed {len(opportunities)} opportunities to all clients")

@app.route("/")
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route("/api/opportunities")
def get_opportunities():
    return jsonify(opportunities)

@socketio.on("connect")
def on_connect():
    print("Student connected!")
    socketio.emit("new_opportunities", opportunities)

scheduler = BackgroundScheduler()
scheduler.add_job(refresh_opportunities, "interval", seconds=30)
scheduler.start()

if __name__ == "__main__":
    refresh_opportunities()
    print("Pulse server running on http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))