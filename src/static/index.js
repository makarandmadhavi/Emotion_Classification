function sendtoprocess() {
    video = $("#toprocess").val();
    interval = $("#interval").val();
    if(interval==0){
        alert("please enter interval");
        return;
    }
    alert(video + " sent to process");
    $.ajax({
        type: "GET",
        url: "/processvideo",
        contentType: 'application/json;charset=UTF-8',
        data: {
            //data goes here
            video,
            interval
        },
        success: function (data) {
            alert(data);
            window.location= "";
        }
    });

    
}