from flask import session, redirect, url_for, render_template, request, Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form["name"]
        session['room'] = request.form["room"]
        print(f"세션: {session}")  # 세션: <SecureCookieSession {'name': '안녕', 'room': '안녕'}>
        return redirect(url_for('main.chat'))
    return render_template('index.html')


@main.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        print(f"이름: {name}, 방: {room}")
        return redirect(url_for('.index'))
    print(f"이름: {name}, 방: {room}")  # 이름: 안녕, 방: 안녕
    return render_template('chat.html', name=name, room=room)
