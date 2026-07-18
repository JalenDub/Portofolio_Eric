from flask import Flask
from config import Config
from models import db, Admin, Profil
from Backend.utama.routes import utama_bp
from Backend.admin.routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(utama_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        try:
            db.create_all()
            
            default_admin = Admin.query.filter_by(username='admin').first()
            if not default_admin:
                admin_user = Admin(username='admin')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()

            profil = Profil.query.order_by(Profil.id.desc()).first()
            if not profil:
                profil = Profil(nama='Eric Christian', bio='Full-Stack Web Developer crafting high-performance user experiences with modern systems.', foto_url='/static/img/profile_new.jpg')
                db.session.add(profil)
            else:
                # Update fallback foto
                profil.foto_url = '/static/img/profile_new.jpg'
                db.session.commit()
        except Exception as e:
            print(f"Gagal inisialisasi database: {str(e)}")
            
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
