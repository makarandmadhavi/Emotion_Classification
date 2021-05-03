from flask import Flask,request, render_template, url_for, redirect,send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import cv2
from predict import predictemotion
import json
from processvideo import predict_video
import pandas as pd
import json
import base64

app = Flask(__name__)
app.debug = False
CORS(app)
app.config['UPLOAD_IMG'] = "uploads" 
app.config['UPLOAD_VIDEO'] = "videos" 

@app.route('/', methods=['POST', 'GET'])
def index():
    uploadedvideos = []
    for file in os.listdir("videos"):
        if file.endswith(".mp4"):
            uploadedvideos.append(file[:-4])
    processedvids = []
    for file in os.listdir(os.path.join("static","csvdata")):
        if file.endswith(".csv"):
            processedvids.append(file[:-4])
    queue = [] + uploadedvideos
    for vid in processedvids:
        queue.remove(vid)
    return render_template('index.html',uploadedvids=uploadedvideos,queue=queue,processedvids=processedvids)

@app.route('/uploadimage', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['imgfile']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_IMG'],filename))
        img = cv2.imread('uploads/'+filename)
        prediction, img = predictemotion(img)
        cv2.imwrite(os.path.join("static/predict/" , filename), img)
        prediction = prediction.sum(axis=0)
        return render_template("imageclassifier.html",filename=filename,prediction=prediction)
    else:
        return "nope"

@app.route('/uploadvideo', methods = ['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        f = request.files['vidfile']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_VIDEO'],filename))
        return redirect("/")
    else:
        return "nope"


@app.route('/processvideo', methods = ['GET','POST'])
def process_video():
    video = request.args['video']
    interval = float(request.args['interval'])
    print(video)
    path = os.path.join("videos",video+".mp4")
    predict_video(video,path,video+".mkv",video+".csv",interval)
    return video + "Processed"

@app.route('/videoclass', methods = ['GET', 'POST'])
def view_video():
    video = request.args['video']
    return render_template('videoclass.html',video=video)

@app.route('/videocsvdata', methods = ['GET', 'POST'])
def csv_video():
    video = request.args['vidname']
    time = float(request.args['time'])
    
    df = pd.read_csv ("static/csvdata/"+video+'.csv')
    i = int(time//df.interval[0])
    print(i)

    return df.iloc[[time//df.interval[0]]].to_dict(orient='records')[0]

@app.route('/livepage', methods = ['GET'])
def livepage():
    interval = float(request.args['live_interval'])
    print("live interval:",interval)
    prediction = [0,0,0,0,0,0,0]
    return render_template('live.html',prediction=prediction,interval=interval)

@app.route('/uploadlive', methods = ['POST'])
def uploadlive():
    if request.method == 'POST':
        f = request.files['imgBase64']
        print(f);
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_IMG'],filename))
        img = cv2.imread('uploads/'+filename)
        prediction, img = predictemotion(img)
        cv2.imwrite(os.path.join("static/predict/" , filename), img)
        prediction = prediction.sum(axis=0)
        return {"preds":tuple(prediction)}
    else:
        return "nope"

@app.route('/getliveimage', methods = ['GET'])
def get_live_image():
    filename = os.path.join("static/predict/" , 'live.png')
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    app.debug = True
    app.run()