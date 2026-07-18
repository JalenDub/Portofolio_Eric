from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Admin, Profil, Skill, Pengalaman, Proyek, PesanKontak
from datetime import datetime
import cloudinary.uploader

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin_session():
    if not session.get('admin_logged_in'):
        flash('Silakan login terlebih dahulu untuk mengakses halaman admin.', 'warning')
        return redirect(url_for('utama.login'))

def upload_file_to_cloudinary(file):
    if not file or file.filename == '':
        return None
    
    # Try Cloudinary first
    try:
        upload_result = cloudinary.uploader.upload(file)
        url = upload_result.get('secure_url')
        if url:
            return url
    except Exception as e:
        pass
    
    # Fallback: save locally
    try:
        import os
        from werkzeug.utils import secure_filename
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'img', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_name = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_dir, unique_name)
        
        file.seek(0)
        file.save(filepath)
        return f"/static/img/uploads/{unique_name}"
    except Exception as e:
        return None

@admin_bp.route('/')
def dashboard():
    profil = Profil.query.order_by(Profil.id.desc()).first()
    skills = Skill.query.all()
    pengalaman = Pengalaman.query.order_by(Pengalaman.tanggal_mulai.desc()).all()
    proyek = Proyek.query.order_by(Proyek.id.desc()).all()
    pesan = PesanKontak.query.order_by(PesanKontak.tanggal_kirim.desc()).all()
    
    return render_template('admin/dashboard.html',
                           profil=profil,
                           skills=skills,
                           pengalaman=pengalaman,
                           proyek=proyek,
                           pesan=pesan,
                           active_tab=request.args.get('tab', 'profil'))

@admin_bp.route('/profil/save', methods=['POST'])
def save_profil():
    nama = request.form.get('nama')
    bio = request.form.get('bio')
    github_url = request.form.get('github_url')
    linkedin_url = request.form.get('linkedin_url')
    email = request.form.get('email')
    
    foto = request.files.get('foto')
    
    profil = Profil.query.order_by(Profil.id.desc()).first()
    
    foto_url = None
    if foto and foto.filename != '':
        foto_url = upload_file_to_cloudinary(foto)
    
    if not profil:
        profil = Profil(nama=nama, bio=bio, github_url=github_url, 
                        linkedin_url=linkedin_url, email=email)
        if foto_url:
            profil.foto_url = foto_url
        db.session.add(profil)
    else:
        profil.nama = nama
        profil.bio = bio
        profil.github_url = github_url
        profil.linkedin_url = linkedin_url
        profil.email = email
        if foto_url:
            profil.foto_url = foto_url
            
    try:
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui profil: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='profil'))

@admin_bp.route('/skills/add', methods=['POST'])
def add_skill():
    nama_skill = request.form.get('nama_skill')
    kategori = request.form.get('kategori')
    persentase = request.form.get('persentase')
    
    try:
        skill = Skill(nama_skill=nama_skill, kategori=kategori, persentase=int(persentase))
        db.session.add(skill)
        db.session.commit()
        flash('Skill baru berhasil ditambahkan!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menambah skill: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='skills'))

@admin_bp.route('/skills/edit/<int:id>', methods=['POST'])
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    skill.nama_skill = request.form.get('nama_skill')
    skill.kategori = request.form.get('kategori')
    skill.persentase = int(request.form.get('persentase'))
    
    try:
        db.session.commit()
        flash('Skill berhasil diperbarui!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui skill: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='skills'))

@admin_bp.route('/skills/delete/<int:id>', methods=['POST'])
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    try:
        db.session.delete(skill)
        db.session.commit()
        flash('Skill berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus skill: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='skills'))

@admin_bp.route('/pengalaman/add', methods=['POST'])
def add_pengalaman():
    perusahaan = request.form.get('perusahaan')
    posisi = request.form.get('posisi')
    tanggal_mulai_str = request.form.get('tanggal_mulai')
    tanggal_selesai_str = request.form.get('tanggal_selesai')
    deskripsi = request.form.get('deskripsi')
    
    try:
        tanggal_mulai = datetime.strptime(tanggal_mulai_str, '%Y-%m-%d').date()
        tanggal_selesai = None
        if tanggal_selesai_str:
            tanggal_selesai = datetime.strptime(tanggal_selesai_str, '%Y-%m-%d').date()
            
        pengalaman = Pengalaman(perusahaan=perusahaan, posisi=posisi, 
                                tanggal_mulai=tanggal_mulai, tanggal_selesai=tanggal_selesai, 
                                deskripsi=deskripsi)
        db.session.add(pengalaman)
        db.session.commit()
        flash('Pengalaman berhasil ditambahkan!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menambah pengalaman: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='pengalaman'))

@admin_bp.route('/pengalaman/edit/<int:id>', methods=['POST'])
def edit_pengalaman(id):
    pengalaman = Pengalaman.query.get_or_404(id)
    pengalaman.perusahaan = request.form.get('perusahaan')
    pengalaman.posisi = request.form.get('posisi')
    
    tanggal_mulai_str = request.form.get('tanggal_mulai')
    tanggal_selesai_str = request.form.get('tanggal_selesai')
    pengalaman.deskripsi = request.form.get('deskripsi')
    
    try:
        pengalaman.tanggal_mulai = datetime.strptime(tanggal_mulai_str, '%Y-%m-%d').date()
        if tanggal_selesai_str:
            pengalaman.tanggal_selesai = datetime.strptime(tanggal_selesai_str, '%Y-%m-%d').date()
        else:
            pengalaman.tanggal_selesai = None
            
        db.session.commit()
        flash('Pengalaman berhasil diperbarui!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui pengalaman: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='pengalaman'))

@admin_bp.route('/pengalaman/delete/<int:id>', methods=['POST'])
def delete_pengalaman(id):
    pengalaman = Pengalaman.query.get_or_404(id)
    try:
        db.session.delete(pengalaman)
        db.session.commit()
        flash('Pengalaman berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus pengalaman: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='pengalaman'))

@admin_bp.route('/proyek/add', methods=['POST'])
def add_proyek():
    judul = request.form.get('judul')
    deskripsi = request.form.get('deskripsi')
    link_proyek = request.form.get('link_proyek')
    link_github = request.form.get('link_github')
    teknologi = request.form.get('teknologi')
    
    foto = request.files.get('foto')
    foto_url = upload_file_to_cloudinary(foto)
    
    try:
        proyek = Proyek(judul=judul, deskripsi=deskripsi, foto_url=foto_url,
                        link_proyek=link_proyek, link_github=link_github, teknologi=teknologi)
        db.session.add(proyek)
        db.session.commit()
        flash('Proyek baru berhasil ditambahkan!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menambah proyek: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='proyek'))

@admin_bp.route('/proyek/edit/<int:id>', methods=['POST'])
def edit_proyek(id):
    proyek = Proyek.query.get_or_404(id)
    proyek.judul = request.form.get('judul')
    proyek.deskripsi = request.form.get('deskripsi')
    proyek.link_proyek = request.form.get('link_proyek')
    proyek.link_github = request.form.get('link_github')
    proyek.teknologi = request.form.get('teknologi')
    
    foto = request.files.get('foto')
    if foto and foto.filename != '':
        foto_url = upload_file_to_cloudinary(foto)
        if foto_url:
            proyek.foto_url = foto_url
            
    try:
        db.session.commit()
        flash('Proyek berhasil diperbarui!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui proyek: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='proyek'))

@admin_bp.route('/proyek/delete/<int:id>', methods=['POST'])
def delete_proyek(id):
    proyek = Proyek.query.get_or_404(id)
    try:
        db.session.delete(proyek)
        db.session.commit()
        flash('Proyek berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus proyek: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='proyek'))

@admin_bp.route('/pesan/delete/<int:id>', methods=['POST'])
def delete_pesan(id):
    pesan = PesanKontak.query.get_or_404(id)
    try:
        db.session.delete(pesan)
        db.session.commit()
        flash('Pesan kontak berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus pesan: {str(e)}', 'danger')
        
    return redirect(url_for('admin.dashboard', tab='pesan'))
