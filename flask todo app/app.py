from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_content = request.form['content']
        new_todo = Todo(content=todo_content)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
