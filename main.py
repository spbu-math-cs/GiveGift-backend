from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import jwt  # to add authorization

time = datetime.now()

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)
SECRET_KEY = "KEY"


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_data
    except jwt.PyJWTError:
        return None

# TODO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkbvkfjbjfbldsovfmvbkfmbfkbkjhkgkkldksdlklfdlfkkprkppcpkfkpewp'

list_of_preferences = [
    {"id": 0, "title": "Apple", "created": time, "description": "She loves big red apples."},
    {"id": 1, "title": "Kitten", "created": time, "description": "She loves small black kittens with black eyes."}
]

users = {
    "USER_1": ["USER_1", generate_password_hash("ABCD"), list_of_preferences]
}
# check_password_hash(hash, "secret password")

# some functions to work with DB


def get_current_preference(preference_id: int, user="USER_1"):
    return users[user][2][preference_id]


def get_list_of_preferences(user="USER_1"):
    return users[user][2]


def append_to_list_of_preferences(title, description, user="USER_1"):
    return users[user][2].append(
                {"id": len(list_of_preferences), "title": title, "description": description, "created": datetime.now()}
            )


def set_to_list_of_preferences(preference_id, title, description, user="USER_1"):
    users[user][2][preference_id] = {
                "id": preference_id, "title": title, "created": datetime.now(), "description": description
            }


def delete_preference(preference_id, user="USER_1"):
    del users[user][2][preference_id]


# replace all to get a correct behavior

def get_preference(preference_id):
    try:
        current_preference = get_current_preference(preference_id)
        return current_preference
    except IndexError:
        abort(404)


@app.route("/")
def index():
    return render_template("index.html", posts=get_list_of_preferences())


@app.route('/<int:post_id>')
def post(post_id):
    current_preference = get_preference(post_id)
    return render_template('post.html', post=current_preference)


@app.route('/create', methods=('GET', 'POST'))
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
def delete(id):
    current_preference = get_preference(id)
    delete_preference(id)
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
