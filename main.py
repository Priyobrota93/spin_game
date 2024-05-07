import psycopg2
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_NAME = 'attend'
DB_USER = 'openpg'
DB_PASSWORD = 'openpgpwd'
DB_HOST = 'localhost'
DB_PORT = '5432'


conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

last_3_ids = []
def fetch_random_employee_id():
    global last_3_ids
    if last_3_ids:
        cur.execute("SELECT employee_id FROM \"user\" WHERE employee_id NOT IN %s ORDER BY RANDOM() LIMIT 1", (tuple(last_3_ids),))
    else:
        cur.execute("SELECT employee_id FROM \"user\" ORDER BY RANDOM() LIMIT 1")
    employee_id = cur.fetchone()[0]

    # Update
    last_3_ids.append(employee_id)
    if len(last_3_ids) > 3:
        last_3_ids.pop(0)

    return employee_id

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spin', methods=['GET'])
def spin():
    try:
        employee_id = fetch_random_employee_id()
        digits = [int(digit) for digit in str(employee_id)]
        return jsonify(success=True, digits=digits, employee_id=employee_id)
    
    except Exception as e:
        return jsonify(success=False, error=str(e))


if __name__ == '__main__':
    app.run(debug=True)