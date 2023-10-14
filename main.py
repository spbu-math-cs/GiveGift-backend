from flask import render_template, request, url_for, flash, redirect

from user import *

# auth = HTTPBasicAuth()
g = None
# later: change to normal secret_key


@app.route("/")
def index():
    # if auth.current_user() is None:
    #     return redirect(url_for('login'))
    # if not hasattr(g, 'user'):
    #     print("NO attr user")
    #     return redirect(url_for('login'))
    # if g.user is None:
    #     print(g.user is None)
    #     return redirect(url_for('login'))
    return render_template("index.html", posts=get_list_of_preferences())


@app.route("/login", methods=('GET', 'POST'))
def login():
    # if hasattr(g, 'user'):
    #     if g.user is not None:
    #         return redirect(url_for('logout'))
    if request.method == 'POST':
        # noinspection PyShadowingNames
        login = request.form['login']
        password = request.form['password']
        if not login:
            flash('Login is required!')
        elif not password:
            flash('Password is required!')
        # else:
            # verify_password(login, password)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout", methods=('GET', 'POST'))
def logout():  # TODO incorrect log out
    if request.method == 'POST':
        # del g.user
        # flask.g = None
        # verify_password("", "")
        return redirect(url_for('index'))
    return render_template('logout.html')


@app.route("/register", methods=('GET', 'POST'))
def register():
    # if hasattr(g, 'user'):
    #     if g.user is not None:
    #         return redirect(url_for('logout'))
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
            # user.hash_password(password)
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/unregister", methods=('GET', 'POST'))  # TODO incorrect result
def unregister():
    if request.method == 'POST':
        # del users_login_to_index[g.user]
        # g.user = None
        return redirect(url_for('login'))
    return render_template('unregister.html')


@app.route('/<int:post_id>')
def post(post_id):
    current_preference = get_tag(post_id, g.user.name)
    return render_template('post.html', post=current_preference)


@app.route('/create', methods=('GET', 'POST'))
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
def delete(id):
    current_preference = get_tag(id)
    delete_preference(id)
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
