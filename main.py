from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Config app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))

    def __init__(self, content):
        self.content = (content)

    def __repr__(self) -> str:
        return f'<Todo {self.id}, {self.content}>'

    def to_json(self) -> dict:
        return {'id': self.id, 'content': self.content}


@app.route('/api/todo', methods=['GET'])
def get_todos():
    # Convert list object to dict
    result = {'todo': [object.to_json() for object in Todo.query.all()]}
    return jsonify(result)

@app.route('/api/todo/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    if todo is not None:
        return jsonify(todo.to_json())
    else:
        return jsonify({'message': f'Todo not found with id = {id}'})


@app.route('/api/todo', methods=['POST'])
def create_todo():
    req = request.get_json()
    if 'content' not in req:
        return jsonify({'message': 'Please input content'})
    todo = Todo(content=req['content'])
    try:
        db.session.add(todo)
        db.session.commit()
        return jsonify({'message': 'Add new success'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Add new failed'})


@app.route('/api/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    req = request.get_json()
    todo = Todo.query.get(id)
    if todo is not None:
        try:
            if 'content' in req:
                todo.content = req['content']
            db.session.commit()
            return jsonify({'message': 'Update success'})
        except:
            db.session.rollback()
            return jsonify({'message': 'Update failed'})
    else:
        return jsonify({'message': f'Todo not found with id = {id}'})


@app.route('/api/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is not None:
        try:
            db.session.delete(id)
            db.session.commit()
            return jsonify({'message': "Delete success"})
        except:
            db.session.rollback()
            return jsonify({'message': "Delete failed"})
    else:
        return jsonify({'message': f'Todo not found with id = {id}'})


if __name__ == '__main__':
    app.run(debug=True)