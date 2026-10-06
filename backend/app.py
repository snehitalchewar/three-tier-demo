import os
from flask import Flask, jsonify, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

def db_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
        row_factory=dict_row,
    )

@app.get("/api/health")
def health():
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS ok")
                cur.fetchone()
        return jsonify(status="ok", database="connected", "version"="db_version_v2")
    except Exception as e:
        return jsonify(status="ok", database="error", detail=str(e)), 503

@app.get("/api/users")
def get_users():
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id DESC")
            return jsonify(cur.fetchall())

@app.post("/api/users")
def create_user():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()

    if not name or not email:
        return jsonify(error="name and email are required"), 400

    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) "
                    "RETURNING id, name, email, created_at",
                    (name, email),
                )
                user = cur.fetchone()
            conn.commit()
        return jsonify(user), 201
    except psycopg.errors.UniqueViolation:
        return jsonify(error="email already exists"), 409

@app.get("/")
def root():
    return jsonify(message="3-tier demo backend is running")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
