from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from models import db, Profil, Skill, Pengalaman, Proyek, PesanKontak, Admin
from config import Config
import resend

utama_bp = Blueprint('utama', __name__)

@utama_bp.route('/')
def index():
    profil = Profil.query.order_by(Profil.id.desc()).first()
    skills = Skill.query.all()
    pengalaman = Pengalaman.query.order_by(Pengalaman.tanggal_mulai.desc()).all()
    proyek = Proyek.query.order_by(Proyek.id.desc()).all()
    
    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s.kategori, []).append(s)
        
    return render_template('utama/index.html', 
                           profil=profil, 
                           skills_by_category=skills_by_category, 
                           pengalaman=pengalaman, 
                           proyek=proyek)

@utama_bp.route('/kontak', methods=['POST'])
def kontak():
    nama = request.form.get('nama')
    email = request.form.get('email')
    subjek = request.form.get('subjek')
    pesan = request.form.get('pesan')
    
    if not (nama and email and subjek and pesan):
        return jsonify({'status': 'error', 'message': 'Semua field wajib diisi!'}), 400
        
    try:
        pesan_baru = PesanKontak(nama=nama, email=email, subjek=subjek, pesan=pesan)
        db.session.add(pesan_baru)
        db.session.commit()
        
        if Config.RESEND_API_KEY and Config.RESEND_TO_EMAIL:
            try:
                resend.api_key = Config.RESEND_API_KEY
                email_body = f"""
                <h3>Pesan Baru dari Website Portofolio</h3>
                <p><strong>Nama:</strong> {nama}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Subjek:</strong> {subjek}</p>
                <p><strong>Pesan:</strong><br>{pesan}</p>
                """
                resend.Emails.send({
                    "from": Config.RESEND_FROM_EMAIL,
                    "to": Config.RESEND_TO_EMAIL,
                    "subject": f"Kontak Portofolio: {subjek}",
                    "html": email_body
                })
            except Exception as email_err:
                pass
            
        return jsonify({'status': 'success', 'message': 'Pesan Anda berhasil dikirim dan disimpan!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Gagal mengirim pesan: {str(e)}'}), 500

@utama_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin.username
            flash('Login berhasil! Selamat datang.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
            
    return render_template('utama/login.html')

@utama_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('utama.login'))
