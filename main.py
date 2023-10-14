from flask import render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from user import *

g = None
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# later: change to normal secret_key


@login_manager.user_loader
def load_user(userid):
    return UsersGetter.get_user_by_index(int(userid))


@app.route("/")
@login_required
def index():
    return render_template("index.html", posts=get_list_of_preferences(current_user.name))


@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # noinspection PyShadowingNames
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        else:
            user = UsersGetter.get_user_by_name(login)
            if user is None:
                flash('Username is incorrect!')
            elif not user.verify_password(password):
                flash('Password is incorrect!')
            else:
                login_user(user, remember=False)
                return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout", methods=('GET', 'POST'))
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route("/register", methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
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
            user = User(name=login, id=len(user_to_list_of_tag)).hash_password(password)
            users_login_to_index[login] = len(user_to_list_of_tag)
            user_to_list_of_tag.append((user, []))
            flash('Successfully registered! Now log in, please!')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/unregister", methods=('GET', 'POST'))  # TODO incorrect result
@login_required
def unregister():
    if request.method == 'POST':
        del users_login_to_index[current_user.name]  # delete from users too
        logout_user()
        return redirect(url_for('login'))
    return render_template('unregister.html')


@app.route('/<int:post_id>')
@login_required
def post(post_id):
    current_preference = get_tag(post_id, current_user.name)
    return render_template('post.html', post=current_preference)


@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            append_to_list_of_preferences(title, description, current_user.name)
            return redirect(url_for('index'))

    return render_template('create.html')


# noinspection PyShadowingBuiltins
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    current_post = get_tag(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            set_to_list_of_preferences(id, title, description, current_user.name)
            return redirect(url_for('index'))
    return render_template('edit.html', post=current_post)


# noinspection PyShadowingBuiltins
@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    current_preference = get_tag(id)
    delete_preference(id, current_user.name)
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
