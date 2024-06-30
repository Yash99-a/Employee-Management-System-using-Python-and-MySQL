from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from decimal import Decimal


app = Flask(__name__)

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="emp"
)
cursor = con.cursor()

# Function to check if an employee exists
def check_employee(employee_id):
    sql = 'SELECT * FROM employee WHERE id=%s'
    cursor.execute(sql, (employee_id,))
    cursor.fetchall()  # Fetch all to clear any pending results
    return cursor.rowcount == 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        Id = request.form['id']
        if check_employee(Id):
            return "Employee already exists. Please try again."

        Name = request.form['name']
        Post = request.form['post']
        Salary = request.form['salary']

        sql = 'INSERT INTO employee (id, name, post, salary) VALUES (%s, %s, %s, %s)'
        data = (Id, Name, Post, Salary)
        try:
            cursor.reset()
            cursor.execute(sql, data)
            con.commit()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            con.rollback()
            return f"Error: {err}"

    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove_employee():
    if request.method == 'POST':
        Id = request.form['id']
        if not check_employee(Id):
            return "Employee does not exist. Please try again."

        sql = 'DELETE FROM employee WHERE id=%s'
        data = (Id,)
        try:
            cursor.reset()
            cursor.execute(sql, data)
            con.commit()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            con.rollback()
            return f"Error: {err}"

    return render_template('remove.html')

@app.route('/promote', methods=['GET', 'POST'])
def promote_employee():
    if request.method == 'POST':
        Id = request.form['id']
        if not check_employee(Id):
            return "Employee does not exist. Please try again."

        try:
            Amount = float(request.form['amount'])

            sql_select = 'SELECT salary FROM employee WHERE id=%s'
            cursor.reset()
            cursor.execute(sql_select, (Id,))
            current_salary = cursor.fetchone()[0]
            new_salary = current_salary + Amount

            sql_update = 'UPDATE employee SET salary=%s WHERE id=%s'
            cursor.reset()
            cursor.execute(sql_update, (new_salary, Id))
            con.commit()
            return redirect(url_for('index'))

        except (ValueError, mysql.connector.Error) as e:
            con.rollback()
            return f"Error: {e}"

    return render_template('promote.html')

@app.route('/display')
def display_employee():
    try:
        sql = 'SELECT * FROM employee'
        cursor.reset()
        cursor.execute(sql)
        employees = cursor.fetchall()
        return render_template('display.html', employees=employees)
    except mysql.connector.Error as err:
        return f"Error: {err}"

if __name__ == "__main__":
    app.run(debug=True)
