from flask import Flask, render_template, request
from findata.db.engine import db
from werkzeug.security import generate_password_hash
from findata.db.engine import query_exec


def findata_main():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    @app.route('/',  methods=["GET", "POST"])
    def main():
        if request.method == "POST":
            name = request.form.get("nombre").title()
            lastname = request.form.get("apellido").title()
            age = request.form.get("edad")
            ocupation = request.form.get("ocupacion").title()
            contry = request.form.get("pais")
            phone = request.form.get("telefono")
            mail = request.form.get("correo", "").lower()
            password = request.form.get("password")
            
            try:
                hashed_password = generate_password_hash(password)
                
                register_finpartnerts = query_exec.execute_insert_from_file('register_user.sql', 
                    params=(name, lastname, phone, contry, int(age), mail, hashed_password, 1, ocupation),
                    return_id=True)
                
                if register_finpartnerts.get("success"):
                    return render_template('index.html', success=f"Tu cuenta se ha creado exitosamente!!!")
                else:
                    error_msg = register_finpartnerts.get("message", "")
                    
                    # Detectar correo duplicado
                    if "duplicate key" in error_msg and "mail" in error_msg:
                        return render_template('index.html', error=f"El correo {mail} ya está registrado. Por favor usa otro correo o inicia sesión.")
                    
                    return render_template('index.html', error="Error al procesar el registro. Intenta nuevamente.")
                    
            except Exception as e:
                error_str = str(e)
                
                if "duplicate key" in error_str and "mail" in error_str:
                    return render_template('index.html', error=f"El correo {mail} ya está registrado. Por favor usa otro correo o inicia sesión.")
                
                return render_template('index.html', error="Ocurrió un error inesperado. Por favor intenta nuevamente.")
            
        return render_template('index.html')


    from findata.modules_auth import auth
    from findata.modules_user import user
    from findata.modules_admin import admin
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)




    with app.app_context():
        import findata.db.models  
        db.create_all()

    return app
