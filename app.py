from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from tracker_module import SavingsTracker
from auth import AuthService
from database import db, UserModel, TransactionModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_tracker.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

tracker = SavingsTracker()

with app.app_context():
    db.create_all()
    print("Registered tables: ", db.metadata.tables.keys())

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = str(request.form['password'])
        if AuthService.login_user(username, password):
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
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
            if AuthService.register_user(username, email, password):
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        name = request.form['expense_name']
        amount = request.form['expense_amount']
        category = request.form['expense_category']
        date = request.form['expense_date']
        tracker.add_expense(current_user.id, name, amount, category, date)
        return redirect(url_for('expense'))
    return render_template('expense.html')

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    if request.method == 'POST':
        amount = float(request.form.get('income_amount'))
        source = request.form['income_source']
        date = request.form['income_date']
        tracker.add_income(current_user.id, "Income", amount, source, date)
        return redirect(url_for('income'))
    return render_template('income.html')

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)
