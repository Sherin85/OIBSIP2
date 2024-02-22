from flask import Flask, render_template, request, redirect, session, url_for
import bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = {}  # This will store registered users' information

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('secured'))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username not in users:
        error = 'User not registered. Please register first.'
        return render_template('index.html', error=error)

    if bcrypt.checkpw(password.encode('utf-8'), users[username]):
        session['username'] = username
        return redirect(url_for('secured'))
    else:
        return render_template('index.html', error='Incorrect password.')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/secured')
def secured():
    if 'username' in session:
        return render_template('secured.html', username=session['username'])
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
