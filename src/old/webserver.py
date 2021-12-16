from flask import Flask
from flask import request
import json
from rq import Queue
from rq.job import Job
from rq import get_current_job
from src.worker import conn
import src.tasks
q = Queue(connection=conn)
app = Flask(__name__)


@app.route("/")
def hello_world():
        return "<p>Hello, World!</p>"


@app.route('/get_word_count', methods=['POST'])
def get_word_count():
    data_json = json.loads(request.data)
    job = q.enqueue(tasks.foo, data_json["sentence"])
    return job.key

@app.route("/get_word_count_result/<job_key>", methods=['GET'])
def get_word_count_result(job_key):
    job_key = job_key.replace("rq:job:", "")
    job = Job.fetch(job_key, connection=conn)

    if(not job.is_finished):
        return "Not yet", 202
    else:
        return str(job.result), 200
