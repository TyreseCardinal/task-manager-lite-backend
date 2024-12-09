from flask import Blueprint, request, jsonify
from .db import db
from .models import Task

api_bp = Blueprint('api', __name__)

# --- TASK ROUTES ---

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'completed': t.completed,
        'created_at': t.created_at,
        'updated_at': t.updated_at
    } for t in tasks]), 200

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        }), 200
    return jsonify(message="Task not found"), 404

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        completed=data.get('completed', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(message="Task created", task_id=new_task.id), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        return jsonify(message="Task updated"), 200
    return jsonify(message="Task not found"), 404

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(message="Task deleted"), 200
    return jsonify(message="Task not found"), 404
