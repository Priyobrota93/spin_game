from flask import Flask, render_template, jsonify
import psycopg2
import random

app = Flask(__name__)

# Establish connection parameters
DB_NAME = 'attend'
DB_USER = 'openpg'
DB_PASSWORD = 'openpgpwd'
DB_HOST = 'localhost'

# Function to connect to the PostgreSQL database
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin')
def spin():
    conn = get_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed.'})

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT employee_id FROM \"user\" ORDER BY RANDOM() LIMIT 1;")
        employee_id = cursor.fetchone()[0]
        cursor.close()
        conn.commit()
    except Exception as e:
        print(f"Database operation error: {e}")
        return jsonify({'error': 'An error occurred.'})

    conn.close()
    return jsonify({'employee_id': employee_id})

if __name__ == '__main__':
    app.run(debug=True)
