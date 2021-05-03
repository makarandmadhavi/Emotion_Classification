var video = document.getElementById('video');
var canvas = document.createElement("CANVAS");
var context = canvas.getContext('2d');

var interval = 1;
var emotionsinterval;
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

function start() {
    interval = document.getElementById("live_interval").value;
    console.log(interval);
    emotionsinterval = setInterval(getEmotions,interval*1000);
}

function stop(l) {
    clearInterval(emotionsinterval);
}

function changeInterval(liveval) {
    interval = liveval;
    clearInterval(emotionsinterval);
    emotionsinterval = setInterval(getEmotions,interval*1000);
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

graph([0,0,0,0,0,0,0])





// Trigger photo take
