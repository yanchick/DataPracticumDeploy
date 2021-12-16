from flask import Flask
from flask import request
import json


app = Flask(__name__)


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


###app.run()