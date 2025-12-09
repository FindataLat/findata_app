from flask import Blueprint, render_template, request, session, redirect, url_for, g
from werkzeug.security import check_password_hash
from findata.db.engine import query_exec
from functools import wraps

bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        if request.endpoint and 'admin.' in request.endpoint:
            if int(session.get('user_rol', 0)) != 2:
                return 'PERMISOS DENEGADOS', 403

        return f(*args, **kwargs)
    return decorated_function


@bp.before_app_request
def mantener_seccion():
    user_id = session.get("user_id")
    
    if user_id is None:
        g.user = None
    else:
        try:
            user_data = query_exec.execute_query_from_file('get_user_by_id.sql', params=(user_id,), fetch_one=True)
            g.user = user_data
        except:
            g.user = None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form.get("mail", "").lower()
        password = request.form.get('password')
        
        try:
            data_user = query_exec.execute_query_from_file('get_data_user_login.sql', params=(mail,), fetch_one=True)
            
            if not data_user:
                return render_template('auth_templates/login.html', error="Correo o contraseña incorrectos")
            
            if check_password_hash(data_user.get('pass'), password):
                session['user_id'] = data_user['id']
                session['user_name'] = data_user['name']
                session['user_mail'] = data_user['mail']
                session['user_rol'] = data_user['rol']

                if data_user['rol'] == 2:
                    return redirect(url_for('admin.users_list'))
                else:
                    return redirect(url_for('users.users_module'))
            else:
                print(data_user.get('pass'))
                print(data_user)
                return render_template('auth_templates/login.html', error="Correo o contraseña incorrectos")
                
        except Exception as e:
            return render_template('auth_templates/login.html', error="Error al iniciar sesión. Intenta nuevamente.")
    
    return render_template('auth_templates/login.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

