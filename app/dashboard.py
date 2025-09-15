from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import os

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    # تحميل آخر 50 باكيت من CSV عند فتح الصفحة
    if os.path.exists('data/packets.csv'):
        df = pd.read_csv('data/packets.csv')
        records = df.tail(50).to_dict(orient='records')
    else:
        records = []
    return render_template("dashboard.html", packets=records)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
