from flask import Flask, render_template, session, request, redirect, url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#インスタンスの作成
app = Flask(__name__)

#暗号鍵の作成
key = os.urandom(21)
app.secret_key = key

#idとパスワードの作成
id_pwd = {'hello':'world'}

#データベース設定
URI = 'postgres:naoya708@localhost/flasktest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

#テーブル内容の設定
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column()

#メイン
@app.route('/')
def index():
    if not session.get('login'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logincheck', methods=['POST'])
def logincheck():
    user_id = request.form['user_id']
    password = request.form['password']

    if user_id in id_pwd:
        if password == id_pwd[user_id]:
            session['login'] = True
        else:
            session['login'] = False
    else:
        session['login'] = False

    if session['login']:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
