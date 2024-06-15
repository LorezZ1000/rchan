from flask import current_app, Blueprint, render_template, session, request, redirect,send_from_directory
from database_modules import database_module
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def check_banned_user():
    session["user_ip"] = request.headers.get('CF-Connecting-IP') or request.headers.get('X-Forwarded-For')
    if database_module.check_banned_user(session["user_ip"]):
        return render_template('banned.html')

@auth_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'imgs','decoration'), 'icon.png', mimetype='image/vnd.microsoft.icon')