from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profil(db.Model):
    __tablename__ = 'profil'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    foto_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), nullable=True)

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_skill = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    persentase = db.Column(db.Integer, nullable=False)

class Pengalaman(db.Model):
    __tablename__ = 'pengalaman'
    
    id = db.Column(db.Integer, primary_key=True)
    perusahaan = db.Column(db.String(100), nullable=False)
    posisi = db.Column(db.String(100), nullable=False)
    tanggal_mulai = db.Column(db.Date, nullable=False)
    tanggal_selesai = db.Column(db.Date, nullable=True)
    deskripsi = db.Column(db.Text, nullable=True)

class Proyek(db.Model):
    __tablename__ = 'proyek'
    
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    foto_url = db.Column(db.String(255), nullable=True)
    link_proyek = db.Column(db.String(255), nullable=True)
    link_github = db.Column(db.String(255), nullable=True)
    teknologi = db.Column(db.String(255), nullable=True)

class PesanKontak(db.Model):
    __tablename__ = 'pesan_kontak'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subjek = db.Column(db.String(150), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    tanggal_kirim = db.Column(db.DateTime, default=datetime.utcnow)
