from flask import render_template, request, url_for, jsonify
from .. import app
from .tasks import send_async_email
import uuid


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/status/<task_id>")
def task_status(task_id):
    process = send_async_email.AsyncResult(task_id)
    if process.state == 'PENDING':
        response = {
            'id': task_id,
            'state': process.state,
            'current': 0,
            'total': 1,
            'status': "Pending"
        }
    elif process.state != 'FAILURE':
        response = {
            'id': task_id,
            'state': process.state,
            'current': process.info.get('current', 0),
            'total': process.info.get('total', 1),
            'status': process.info.get('status', '')
        }
    else:
        response = {
            'id': task_id,
            'state': process.state,
            'current': 1,
            'total': 1,
            'status': str(process.info)
        }
    return jsonify(response)


@app.route("/tasks/send-email", methods=["GET", "POST"])
def send_email():
    if request.method == "GET":
        return render_template("send_email.html")
    email = request.form["email"]
    email_data = {
        'subject': "Sample message from localhost",
        'to': email,
        'body': "This is a test email sent from a bachground Celery task"
    }
    if request.form['submit'] == "Send":
        task = send_async_email.apply_async(args=[email_data], task_id=uuid.uuid4().hex)
    else:
        task = send_async_email.apply_async(args=[email_data], countdown=60)
    return jsonify({}), 202, {"location": url_for('task_status', task_id=task.id)}