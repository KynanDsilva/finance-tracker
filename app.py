from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/expense', methods=['GET', 'POST'])
def expense():
    return render_template('expense.html')

@app.route('/income', methods=['GET', 'POST'])
def income():
    return render_template('income.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)
