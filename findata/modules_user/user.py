from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from findata.db.engine import query_exec
from findata.modules_auth.auth import login_required



bp = Blueprint('users', __name__)

@bp.route("/mis-finanzas", methods=["GET", "POST"])
@login_required
def users_module():
    data_user = session

    data_user_module={}

    return render_template('users_templates/module_user.html', data_user=session, data_user_module=data_user_module)
