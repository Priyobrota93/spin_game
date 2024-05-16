import psycopg2
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_NAME = 'raffle_draw'
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
def fetch_random_draw_sl():
    global last_3_ids
    if last_3_ids:
        cur.execute("SELECT draw_sl FROM \"card1\" WHERE draw_sl NOT IN %s ORDER BY RANDOM() LIMIT 1", (tuple(last_3_ids),))
    else:
        cur.execute("SELECT draw_sl FROM \"card1\" ORDER BY RANDOM() LIMIT 1")
    draw_sl = cur.fetchone()[0]

    # Update
    last_3_ids.append(draw_sl)
    print(last_3_ids)
    if len(last_3_ids) > 10:
        last_3_ids.pop(0)

    return draw_sl

from flask import render_template, jsonify

@app.route('/')
def index():
    try:
        # Fetch 3-digit integer values from the database
        cur.execute("SELECT draw_sl FROM card1 ORDER BY draw_sl")
        draw_sl_values = [str(row[0]).zfill(3) for row in cur.fetchall()]
        
        # Render the HTML template with the values
        return render_template('index.html', draw_sl_values=draw_sl_values)
    except Exception as e:
        # Handle any exceptions that may occur during database access
        return render_template('error.html', error=str(e))

@app.route('/spin', methods=['GET'])
def spin():
    try:
        draw_sl = fetch_random_draw_sl()
        digits = [int(digit) for digit in str(draw_sl)]
        return jsonify(success=True, digits=digits, draw_sl=draw_sl)
    
    except Exception as e:
        return jsonify(success=False, error=str(e))


if __name__ == '__main__':
    app.run(debug=True)