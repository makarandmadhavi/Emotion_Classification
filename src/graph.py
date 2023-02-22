import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('Agg')


def plotgraphs(filename):
    df = pd.read_csv("static/csvdata/"+filename)
    filename = filename[:-4]
    df['Timestamp'] = df['Timestamp'].div(60)
    

    plt.plot('Timestamp','Angry', color="red", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Angry'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Disgusted',  color="green", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Disgusted'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Fearful',  color="orange", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Fearful'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Happy',  color="blue", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Happy'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Neutral',  color="yellow", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Neutral'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Sad',  color="black", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Sad'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

    plt.plot('Timestamp','Surprised',  color="purple", data=df)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.savefig('static/graphs/Surprised'+filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    plotgraphs("stockvideo.csv")
