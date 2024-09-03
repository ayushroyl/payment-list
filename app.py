from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username != 'royayush':
        return
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'royayush' and password == 'roy@ayush':
            user = User()
            user.id = 'royayush'
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stu.json')

    with open(json_path, 'r') as file:
        students = json.load(file)

    return render_template('index.html', students=students, logged_in=current_user.is_authenticated)

@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stu.json')

    new_student = {
        "name": request.form['name'],
        "roll": request.form['roll'],
        "payment_status": request.form['payment_status']
    }

    with open(json_path, 'r+') as file:
        data = json.load(file)
        data.append(new_student)
        file.seek(0)
        json.dump(data, file, indent=4)

    return redirect(url_for('index'))

@app.route('/delete_student', methods=['POST'])
@login_required
def delete_student():
    roll_to_delete = request.form['roll']
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stu.json')

    with open(json_path, 'r+') as file:
        data = json.load(file)
        data = [student for student in data if student['roll'] != roll_to_delete]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

    return redirect(url_for('index'))

@app.route('/modify_student', methods=['POST'])
@login_required
def modify_student():
    original_roll = request.form['original_roll']
    new_name = request.form['name']
    new_roll = request.form['roll']
    new_payment_status = request.form['payment_status']
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stu.json')

    with open(json_path, 'r+') as file:
        data = json.load(file)
        for student in data:
            if student['roll'] == original_roll:
                student['name'] = new_name
                student['roll'] = new_roll
                student['payment_status'] = new_payment_status
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
