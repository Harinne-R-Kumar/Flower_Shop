from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hrk@cit22",
    database="flower_shop"
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM flowers")
    flowers = cursor.fetchall()
    return render_template('index.html', flowers=flowers)

@app.route('/add', methods=['POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        cursor.execute("INSERT INTO flowers (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
        db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower(flower_id):
    cursor.execute("SELECT * FROM flowers WHERE id = %s", (flower_id,))
    flower = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        cursor.execute("UPDATE flowers SET name = %s, description = %s, price = %s WHERE id = %s", (name, description, price, flower_id))
        db.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', flower=flower)

@app.route('/delete/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    cursor.execute("DELETE FROM flowers WHERE id = %s", (flower_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
