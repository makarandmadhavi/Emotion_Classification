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
from graph import plotgraphs

app = Flask(__name__)
app.debug = False
CORS(app)
app.config['UPLOAD_IMG'] = "uploads" 
app.config['UPLOAD_VIDEO'] = "videos" 

live = "live"
interval = 1

videoname = os.path.join("static","processedvids",live+".mp4")
csvname = os.path.join("static","csvdata",live+".csv")
df = pd.DataFrame([], columns = ['Timestamp', 'Angry',"Disgusted","Fearful","Happy","Neutral","Sad","Surprised","interval"])
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = None


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
        if vid in queue:
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
    prediction = [0,0,0,0,0,0,0]
    return render_template('live.html',prediction=prediction)

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
        pred = tuple(prediction)
        out.write(img)
        global df
        df.loc[len(df.index)] = [len(df.index), pred[0],pred[1],pred[2],pred[3],pred[4],pred[5],pred[6],interval] 
        return {"preds":pred}
    else:
        return "nope"

@app.route('/getliveimage', methods = ['GET'])
def get_live_image():
    filename = os.path.join("static/predict/" , 'live.png')
    return send_file(filename, mimetype='image/png')

@app.route('/start_live_video', methods = ['POST'])
def start_live():
    width = request.json['width']
    height = request.json['height']
    fps = request.json['fps']
    global out
    global live
    global videoname
    global csvname
    global interval
    interval = 1.0/fps
    live = request.json['live']
    videoname = os.path.join("static","processedvids",live+".mkv")
    csvname = os.path.join("static","csvdata",live+".csv")
    out = cv2.VideoWriter(videoname, fourcc, fps, (width,  height))
    return "Recording Started"

@app.route('/stop_live_video', methods = ['POST'])
def stop_live():
    df.to_csv(csvname)
    out.release()
    plotgraphs(str(live)+'.csv')
    return "Recording Ended"

if __name__ == '__main__':
    app.debug = False
    app.templates_auto_reload = False
    app.run()