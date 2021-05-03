function showGraph() {
    video = document.getElementById("vid");
    vidname = video.getAttribute("name");
    time = vid.currentTime;
    console.log(time);
    $.ajax({
        type: "GET",
        url: "/videocsvdata",
        contentType: 'application/json;charset=UTF-8',
        data: {
            //data goes here
            vidname,
            time
        },
        success: function (data) {
            drawGraph(data);
        }
    });
}

function drawGraph(data) {
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: false,

        title: {
            text: "Emotions"
        },
        axisX: {
            interval: 1
        },
        axisY2: {
            interlacedColor: "rgba(1,77,101,.2)",
            gridColor: "rgba(1,77,101,.1)",
        },
        data: [{
            type: "bar",
            name: "companies",
            axisYType: "secondary",
            color: "#014D65",
            dataPoints: [{
                    y: data["Angry"],
                    label: "Angry"
                },
                {
                    y: data["Disgusted"],
                    label: "Disgusted"
                },
                {
                    y: data["Fearful"],
                    label: "Fearful"
                },
                {
                    y: data["Happy"],
                    label: "Happy"
                },
                {
                    y: data["Neutral"],
                    label: "Neutral"
                },
                {
                    y: data["Sad"],
                    label: "Sad"
                },
                {
                    y: data["Surprised"],
                    label: "Surprised"
                }

            ]
        }]
    });
    chart.render();
}

window.onload = function () {
    setInterval(showGraph, 200);
}