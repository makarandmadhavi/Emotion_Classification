var video = document.getElementById('video');
const logElem = document.getElementById("log");
var canvas = document.createElement("CANVAS");
var context = canvas.getContext('2d');

var interval = 1;
var emotionsinterval;

function camera() {
    // Get access to the camera!
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({
            video: true
        }).then(function (stream) {
        //video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();
        });
    }
}

function startCapture(displayMediaOptions) {
    let captureStream = null;
   
    return navigator.mediaDevices.getDisplayMedia(displayMediaOptions)
       .catch(err => { console.error("Error:" + err); return null; });
}

var displayMediaOptions = {
    video: {
      cursor: "always"
    },
    audio: false
};

async function screencap() {
    logElem.innerHTML = "";
  
    try {
      video.srcObject = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
      //dumpOptionsInfo();
    } catch(err) {
      console.error("Error: " + err);
    }
}

function stopCapture(evt) {
    let tracks = video.srcObject.getTracks();
  
    tracks.forEach(track => track.stop());
    video.srcObject = null;
}

function start() {
    interval = document.getElementById("live_interval").value;
    console.log(interval);
    let width  = video.clientWidth;
    let height = video.clientHeight;
    let live = document.getElementById("name").value;
    let fps =  1.0/interval;
    $.ajax({
        type: "POST",
        url: "/start_live_video",
        processData: false,
        contentType: "application/json",
        data: JSON.stringify( {
            width,
            height,
            live,
            fps
        }),
        success: function (data) {
            console.log(data); 
            emotionsinterval = setInterval(getEmotions,interval*1000);
        }
    });
}

function stop() {
    clearInterval(emotionsinterval);
    $.ajax({
        type: "POST",
        url: "/stop_live_video",
        processData: false,
        contentType: "application/json",
        data: null,
        success: function (data) {
            console.log(data); 
            window.location ='videoclass?video='+document.getElementById("name").value;
        }
    });
}


function dataURItoBlob(dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    var blob = new Blob([ab], {type: mimeString});
    return blob;
  
  }

function getEmotions() {
    canvas.width  = video.clientWidth;
    canvas.height = video.clientHeight;
    context.drawImage(video, 0, 0, video.clientWidth, video.clientHeight);
    let file = canvas.toDataURL('image/png');
    let fd = new FormData();
    fd.set("imgBase64", dataURItoBlob(file), "live.png");
    $.ajax({
        type: "POST",
        url: "/uploadlive",
        processData: false,
        contentType: false,
        data: fd,
        success: function (data) {
            console.log(data);
            graph(data.preds);
            var img = new Image();
            var output = document.getElementById('canop');
            var outputcontext = output.getContext('2d');
            img.onload = function(){
                output.width = img.width;
                output.height = img.height;
                outputcontext.drawImage( img, 0, 0 );
            };
            img.src = "/getliveimage"+"?"+Math.random(); 
        }
    });
	
}

function graph(preds) {
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: false,
    
        title: {
            text: "Summary"
        },
        axisX: {
            interval: 1
        },
        axisY2: {
            interlacedColor: "rgba(1,77,101,.2)",
            gridColor: "rgba(1,77,101,.1)",
            title: "Weights"
        },
        data: [{
            type: "bar",
            name: "companies",
            axisYType: "secondary",
            color: "#014D65",
            dataPoints: [{
                    y: preds[0],
                    label: "Angry"
                },
                {
                    y: preds[1],
                    label: "Disgusted"
                },
                {
                    y: preds[2],
                    label: "Fearful"
                },
                {
                    y: preds[3],
                    label: "Happy"
                },
                {
                    y: preds[4],
                    label: "Neutral"
                },
                {
                    y: preds[5],
                    label: "Sad"
                },
                {
                    y: preds[6],
                    label: "Surprised"
                }
    
            ]
        }]
    });
    chart.render();
}

load();

function load() {
    let dt = new Date().toISOString().replace(/:/g,'-').replace('.','');
    document.getElementById("name").value = dt;
    graph([0,0,0,0,0,0,0])
}




// Trigger photo take
