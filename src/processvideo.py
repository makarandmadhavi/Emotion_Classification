from predict import predictemotion
import cv2
import numpy as np
import pandas as pd
import os
from graph import plotgraphs


def predict_video(video,filename,videoname,csvname,interval):
  print(filename)
  videoname = os.path.join("static","processedvids",videoname)
  csvname = os.path.join("static","csvdata",csvname)
  cap = cv2.VideoCapture(filename)
  # Check if camera opened successfully
  if (cap.isOpened()== False): 
    print("Error opening video stream or file")
  fps = cap.get(cv2.CAP_PROP_FPS)
  #create data object
  df = pd.DataFrame([], columns = ['Timestamp', 'Angry',"Disgusted","Fearful","Happy","Neutral","Sad","Surprised"]) 
  # Read until video is completed

  i=0
  emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

  width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)  ) # float
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  print(width,height)
  #size=(width,height)
  fourcc = cv2.VideoWriter_fourcc(*'X264')
  out = cv2.VideoWriter(videoname, fourcc, fps, (width,  height))
  while(cap.isOpened()):
    # Capture frame-by-frame
    ret, img = cap.read()
    print(i)
    i=i+1
    if ret == True:
      predictions, img = predictemotion(img)
      if(len(predictions)>0):
          pred = predictions.sum(axis=0)
          maxindex = int(np.argmax(pred))
          df2 = {'Timestamp':i, 'Angry':pred[0],"Disgusted":pred[1],"Fearful":pred[2],"Happy":pred[3],
          "Neutral":pred[4],"Sad":pred[5],"Surprised":pred[6],"interval":interval,"fps":fps} 
          df=df.append(df2,ignore_index = True)
          #print(df)
          print(emotion_dict[maxindex]) 
    # Break the loop
    else: 
      break
    out.write(img)
    #skip frames
    for _ in range(int(fps*interval)):
      ret, imgt = cap.read()  
      out.write(img)
  df.to_csv(csvname)
  out.release()
  plotgraphs(video+".csv")
if __name__ == "__main__":
  predict_video("reactionedited","reactionedited.mp4","test.avi","test.csv",1)
# # When everything done, release the video capture object
# cap.release()
# # Closes all the frames
# cv2.destroyAllWindows()