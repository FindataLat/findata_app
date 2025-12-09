from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from findata.modules_auth.auth import login_required
from findata.db.engine import query_exec
from werkzeug.security import generate_password_hash


bp = Blueprint('admin', __name__)


@bp.route("/users-list", methods=["GET", "POST"])
@login_required
def users_list():
    data_user = session
    error = request.args.get('error')
    success = request.args.get('success')

    users_list = query_exec.execute_query_from_file('get_all_register_users.sql')

    return render_template('admin_templates/module_admin.html', data_user=data_user, users_list=users_list, success=success, error=error)


@bp.route("/update-user/<id>", methods=["GET", "POST"])
@login_required
def update_user(id):

    if request.method == "POST":
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        age = request.form.get('age')
        contry = request.form.get('contry')
        job = request.form.get('job')
        mail = request.form.get("mail", "").lower()
        password = request.form.get('password')
        phone = request.form.get('phone')

        hashed_password = generate_password_hash(password)

        update_user_excute = query_exec.execute_insert_from_file('update_user.sql', 
        params=(name, lastname, phone, contry, int(age), mail, hashed_password, 1, job, id), return_id=True)

        # DEVOLVER JSON EN LUGAR DE REDIRECT
        if update_user_excute.get("success"):
            return jsonify({"success": True, "message": "Usuario actualizado exitosamente"})
        else:
            return jsonify({"success": False, "message": "Error al actualizar el registro"})
                    
    # GET - Devolver datos del usuario como JSON
    data_user = query_exec.execute_query_from_file('get_data_user_for_update.sql', params=(id,), fetch_one=True)
    return data_user