from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 1. Database Configuration
# This creates a file named 'database.db' in your project folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. The Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# 3. Create the database tables
with app.app_context():
    db.create_all()

# 4. Routes
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(content=data['content'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created!"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = [{"id": task.id, "content": task.content} for task in tasks]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
