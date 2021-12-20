from flask import Flask
from flask import request
import json
from rq import Queue
from rq.job import Job
from src.task import  very_long_task
import redis


redis_url = 'redis://10.180.250.26:6379'

conn = redis.from_url(redis_url)

app = Flask(__name__)
q = Queue(connection=conn)


@app.route("/",methods=['POST'])
def hello_world():
    return "<p>Привет участникам электива"

@app.route("/parse/<job>")
def parse_para(job):
    return "Вы обратились на {}".format(job)

@app.route("/sample_post",methods=["POST"])
def parse_para_post():
    d = json.loads(request.data)
    return "Вы обратились по посту на {}".format(d['body'])


@app.route("/do_long_task")
def do_long_task():
   job = q.enqueue(very_long_task)
   #result_url = "http://127.0.0.1/get_result/{}".format(str(job.key))
   return job.key

@app.route("/get_result/<job_key>")
def get_results(job_key):
    job_key = job_key.replace("rq:job:","")
    job = Job.fetch(job_key,connection=conn)
    if (not job.is_finished):
        return "Жди еще"
    else:
        return str(job.result)


##app.run()