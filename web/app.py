from flask import Flask
import os, time
import mysql.connector

app = Flask(__name__)

def get_db():
    # Retry so the first request works even if DB is still starting
    retries = 10
    last_exc = None
    while retries:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'db'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'example'),
                database=os.environ.get('DB_NAME', 'mydb'),
            )
            return conn
        except Exception as e:
            last_exc = e
            retries -= 1
            time.sleep(2)
    raise RuntimeError(f"DB connection failed after retries: {last_exc}")

@app.route("/")
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))")
    cur.execute("INSERT INTO visits (message) VALUES ('Hello from Flask!')")
    db.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return f"Hello! This page has been visited {count} times.\n"

if __name__ == "__main__":
    # Listen on all interfaces, port 5000
    app.run(host="0.0.0.0", port=5000)
