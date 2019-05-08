import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory, session
from werkzeug import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return "please login."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username == 'admin':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return "wrong username"
    return '<form action="" method="post"><input type="text" name="username"><input type="submit" value="Login"></form>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))




@app.route('/hello/')
def hello():
    return render_template('hello.html', message='Hello world!')

@app.route('/send', methods=['GET', 'POST'])
def send():

    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html')
        else:
            return "<p>this file does not allow. please check file type</p>"
    else:
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run()

