import flask
from flask import render_template, request, url_for, flash, redirect, g, jsonify
from flask_httpauth import HTTPBasicAuth

from user import *

auth = HTTPBasicAuth()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkbvkfjbjfbldsovfmvbkfmbfkbkjhkgkkldksdlklfdlfkkprkppcpkfkpewp'

# later: change to normal secret_key


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user: User = UsersGetter.get_user_by_name(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/")
def index():
    if g is None or g.user is None:
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
    if request.method == 'POST':
        # noinspection PyShadowingNames
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        else:
            verify_password(login, password)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout", methods=('GET', 'POST'))
@auth.login_required
def logout():  # TODO incorrect log out
    if request.method == 'POST':
        del g.user
        flask.g = None
        # verify_password("", "")
        return redirect(url_for('index'))
    return render_template('logout.html')


@app.route("/register", methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        # noinspection PyShadowingNames
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        else:
            user = User(name=login, id=len(user_to_list_of_tag))
            users_login_to_index[login] = len(user_to_list_of_tag)
            user_to_list_of_tag.append((user, []))
            user.hash_password(password)
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/unregister", methods=('GET', 'POST'))  # TODO incorrect result
@auth.login_required
def unregister():
    if request.method == 'POST':
        del users_login_to_index[g.user]
        g.user = None
        return redirect(url_for('login'))
    return render_template('unregister.html')


@app.route('/<int:post_id>')
@auth.login_required
def post(post_id):
    current_preference = get_tag(post_id, g.user.name)
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
            append_to_list_of_preferences(title, description, g.user.name)
            return redirect(url_for('index'))

    return render_template('create.html')


# noinspection PyShadowingBuiltins
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@auth.login_required
def edit(id):
    current_post = get_tag(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            set_to_list_of_preferences(id, title, description, g.user.name)
            return redirect(url_for('index'))
    return render_template('edit.html', post=current_post)


# noinspection PyShadowingBuiltins
@app.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    current_preference = get_tag(id)
    delete_preference(id)
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
