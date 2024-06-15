from flask import current_app, Blueprint, render_template, redirect, request, flash, session
from database_modules import database_module, timeout_module
from flask_socketio import SocketIO, emit
import re
import os

posts_bp = Blueprint('posts', __name__)
socketio = SocketIO()

@posts_bp.route('/new_post',methods=['POST'])
def new_post():
    socketio = current_app.extensions['socketio']
    user_ip = session["user_ip"]
    subject = request.form['subject']
    board_id = request.form['board_id']
    comment = request.form['text']
    embed = request.form['embed']
    if database_module.check_timeout_user(session["user_ip"]):
        flash('você precisa esperar um pouco para postar novamente.')
        return redirect(request.referrer)
    timeout_module.timeout(session["user_ip"])
    if not database_module.check_board(board_id):
        flash('Eu sei oq vc tentou fazer, seu bobão.')
        return redirect(request.referrer)
    match = re.match(r'^#(\d+)', comment)
    if len(comment) >= 10000:
        flash('Você atingiu o limite')
        return redirect(request.referrer)
    if comment == '':
        flash('Você precisa digitar algo, seu bocó!')
        return redirect(request.referrer)
    if match:
        reply_to = match.group(1)
        database_module.check_post_exist(int(reply_to))
        if not database_module.check_post_exist(int(reply_to)):
            reply_to = request.form['thread_id']
            if reply_to == '':
                reply_to = match.group(1)
            if 'fileInput' in request.files:
                file = request.files['fileInput']
                if file.filename != '' and file.filename.endswith(('.jpeg','.mov', '.jpg', '.gif', '.png', '.webp', '.webm', '.mp4')):
                    upload_folder = './static/reply_images/'
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, file.filename))
                    database_module.add_new_reply(user_ip,reply_to,comment, embed, file.filename)
                    socketio.emit('nova_postagem', 'puta barata', broadcast=True)
                    return redirect(request.referrer)
            file = ""
            database_module.add_new_reply(user_ip,reply_to,comment, embed, file)
            socketio.emit('nova_postagem', 'puta barata', broadcast=True)
            return redirect(request.referrer)

        if 'fileInput' in request.files:
            file = request.files['fileInput']
            if file.filename != '' and file.filename.endswith(('.jpeg','.mov', '.jpg', '.gif', '.png', '.webp', '.webm', '.mp4')):
                upload_folder = './static/reply_images/'
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, file.filename))
                database_module.add_new_reply(user_ip,reply_to,comment, embed, file.filename)
                socketio.emit('nova_postagem', 'puta barata', broadcast=True)
                return redirect(request.referrer)
        file = ""
        database_module.add_new_reply(user_ip,reply_to,comment, embed, file)
        socketio.emit('nova_postagem', 'puta barata', broadcast=True)
        return redirect(request.referrer) 

    if 'fileInput' in request.files:
        file = request.files['fileInput']
        if file.filename != '' and file.filename.endswith(('.jpeg', '.jpg','.mov', '.gif', '.png', '.webp', '.webm', '.mp4')):
            upload_folder = './static/post_images/'
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, file.filename))
            database_module.add_new_post(user_ip,board_id,comment, embed, file.filename)
            socketio.emit('nova_postagem', 'puta barata', broadcast=True)
            return redirect(request.referrer)
    flash("Você precisa upar alguma imagem, isso é um imageboard...")
    return redirect(request.referrer)

@posts_bp.route('/socket.io/')
def socket_io():
    socketio_manage(request.environ, {'/': SocketIOHandler}, request=request)
