from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkbvkfjbjfbldsovfmvbkfmbfkbkjhkgkkldksdlklfdlfkkprkppcpkfkpewp'

list_of_preferences = [
    {"id": 0, "title": "Apple", "created": "later", "description": "NO"},
    {"id": 1, "title": "Microsoft", "created": "now", "description": "YES"}
]


def get_preference(preference_id):
    try:
        current_preference = list_of_preferences[preference_id]
        return current_preference
    except IndexError:
        abort(404)


@app.route("/")
def index():
    return render_template("index.html", posts=list_of_preferences)


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
            list_of_preferences.append(
                {"id": len(list_of_preferences), "title": title, "description": description, "created": "NOW"}
            )
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
            list_of_preferences[id] = {
                "id": id, "title": title, "created": "NOW", "description": description
            }
            return redirect(url_for('index'))
    return render_template('edit.html', post=current_post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    current_preference = get_preference(id)
    del list_of_preferences[id]
    flash('"{}" was successfully deleted!'.format(current_preference['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
