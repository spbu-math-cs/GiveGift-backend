from flask import Flask, render_template, request, url_for, flash, redirect, g, jsonify
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from flask_httpauth import HTTPBasicAuth

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

auth = HTTPBasicAuth()
time = datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkbvkfjbjfbldsovfmvbkfmbfkbkjhkgkkldksdlklfdlfkkprkppcpkfkpewp'


class User:
    def __init__(self, name: str, id: int):
        self.name = name
        self.password_hash = None
        self.id = id

    def hash_password(self, password: str):
        self.password_hash = pwd_context.encrypt(password)
        return self

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = users[data['id']][0]
        return user


# check_password_hash(hash, "secret password")

# some functions to work with DB

list_of_preferences = [
    {"id": 0, "title": "Apple", "created": time, "description": "She loves big red apples."},
    {"id": 1, "title": "Kitten", "created": time, "description": "She loves small black kittens with black eyes."}
]

users = [
    (User("USER_1", 0).hash_password("123"), list_of_preferences)
]

users_login_index = {
    "USER_1": 0
}


class UsersClass:
    @staticmethod
    def get_user_by_name(name: str) -> User:
        try:
            return users[users_login_index[name]][0]
        except KeyError:
            return None

    @staticmethod
    def get_user_by_index(index_: int) -> User:
        return users[index_][0]

    @staticmethod
    def get_user_tags(name: str) -> list:
        try:
            return users[users_login_index[name]][1]
        except KeyError:
            return None


def get_current_preference(preference_id: int, user="USER_1"):
    return users[users_login_index[user]][1][preference_id]


def get_list_of_preferences(user="USER_1"):
    return users[users_login_index[user]][1]


def append_to_list_of_preferences(title, description, user="USER_1"):
    users[users_login_index[user]][1].append(
        {"id": len(list_of_preferences), "title": title, "description": description, "created": datetime.now()}
        )


def set_to_list_of_preferences(preference_id, title, description, user="USER_1"):
    users[users_login_index[user]][0][preference_id] = {
                "id": preference_id, "title": title, "created": datetime.now(), "description": description
    }


def delete_preference(preference_id, user="USER_1"):
    del users[users_login_index[user]][0][preference_id]


# replace all to get a correct behavior

def get_preference(preference_id):
    try:
        current_preference = get_current_preference(preference_id)
        return current_preference
    except IndexError:
        abort(404)


# @auth.verify_password
# def verify_password(username, password):
#     user: User = users[username][0]
#     if not user or not user.verify_password(password):
#         return False
#     g.user = user
#     return True


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user: User = UsersClass.get_user_by_name(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/")
def index():
    if g is None:
        return redirect(url_for('index'))
    return render_template("index.html", posts=get_list_of_preferences())


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/login", methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('logout'))
    # if request.method == 'POST':
    #     username = request.json.get('username')
    # password = request.json.get('password')
    # if username is None or password is None:
    #     abort(400) # missing arguments
    # if User.query.filter_by(username = username).first() is not None:
    #     abort(400) # existing user
    # user = User(username = username)
    # user.hash_password(password)
    # db.session.add(user)
    # db.session.commit()
    # return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        else:
            user = User(name=login, id=len(users))
            users_login_index[login] = len(users)
            users.append((user, []))
            user.hash_password(password)
            # append_to_list_of_preferences(title, description)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout", methods=('GET', 'POST'))
@auth.login_required
def logout():
    if request.method == 'POST':
        g.user = None
        return url_for('login')
    return render_template('logout.html')


@app.route("/register", methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        else:
            #append_to_list_of_preferences(title, description)
            user = User(name=login, id=len(users))
            users_login_index[login] = len(users)
            users.append((user, []))
            user.hash_password(password)
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/unregister", methods=('GET', 'POST'))
@auth.login_required
def unregister():
    if request.method == 'POST':
        # del users[users_login_index[g.user]] can't be deleted, another indexes will be invalid
        del users_login_index[g.user]
        g.user = None
        return redirect(url_for('login'))
    return render_template('unregister.html')


@app.route('/<int:post_id>')
@auth.login_required
def post(post_id):
    current_preference = get_preference(post_id)
    return render_template('post.html', post=current_preference)


@app.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            append_to_list_of_preferences(title, description)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@auth.login_required
def edit(id):
    current_post = get_preference(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            set_to_list_of_preferences(id, title, description)
            return redirect(url_for('index'))
    return render_template('edit.html', post=current_post)


@app.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    current_preference = get_preference(id)
    delete_preference(id)
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
