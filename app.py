from flask import Flask, render_template, request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
import numpy as np
import random
import csv

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '1935341323'  # replace with your secret key

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']

        with open('user.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username and row[1] == password:
                    user = User(username)
                    login_user(user)
                    return redirect(url_for('dash'))

            return "Invalid username or password"

    return render_template('login.html')



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))










app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secim.db'
db = SQLAlchemy(app)

class Secim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ogrenci_numarasi = db.Column(db.String(80), nullable=False)
    dersler = db.Column(db.String(500), nullable=False)
    ip_adresi = db.Column(db.String(15), nullable=False)

dersler = ["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih", "Coğrafya", "Edebiyat", "İngilizce"]

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    if request.method == 'POST':
        secilen_dersler = []
        ogrenci_numarasi = username #request.form.get('ogrenci_numarasi') # Formdan öğrenci numarasını alıyoruz
        ip_adresi = request.remote_addr  # Kullanıcının IP adresini al
        for i in range(1,9): # 1'den 8'e kadar döngü (Python'da üst sınır dahil değildir)
            secilen_ders = request.form.get(f'ders{i}') # ders1, ders2, ... ,ders8 adındaki form elemanlarını alıyoruz
            if secilen_ders:
                secilen_dersler.append(secilen_ders)
        secim = Secim(ogrenci_numarasi=ogrenci_numarasi, dersler=str(secilen_dersler), ip_adresi=ip_adresi) # veritabanına yeni kayıt
        db.session.add(secim)
        db.session.commit() # Veritabanına değişiklikleri uygula
        return f"Seçilen dersler: {secilen_dersler}" # Seçilen dersleri döndürüyoruz
    return render_template('index.html', dersler=dersler) # HTML formunu render ediyoruz








if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Veritabanındaki tüm tabloları oluştur
    app.run(debug=True)




