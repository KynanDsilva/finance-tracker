from flask import Flask, render_template, request, redirect, url_for
from tracker_module import *
from auth import *

app = Flask(__name__)

tracker = SavingsTracker()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get['username']
        password = str(request.form['password'])
        if User.authenticate(username, password):
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password==confirm_password:
            new_user = User(username, email, password)
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error="Passwords do not match")
    return render_template('register.html')

@app.route('/expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        name = str(request.form['expense_name'])
        amount = float(request.form['expense_amount'])
        category = str(request.form['expense_category'])
        date = str(request.form['expense_date'])
        tracker.add_expense(name, amount, category, date)
        print(f"Redirecting to: {url_for('expense')}")
        return redirect(url_for('expense'))
    return render_template('expense.html')

@app.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        amount = float(request.form['income_amount'])
        source = str(request.form['income_source'])
        date = str(request.form['income_date'])
        tracker.add_income(amount, source, date)
        print(f"Redirecting to: {url_for('income')}")
        return redirect(url_for('income'))
    return render_template('income.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)
