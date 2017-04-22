if(!Recorder.isRecordingSupported()) {
    alert("Recording is not supported!");
}

var recordedChunks = [];

function onRecordingReady(e) {
    recordedChunks.push(e.data);
}

function onRecordingStopped(e) {
    var blob = new Blob(recordedChunks);
    var url = URL.createObjectURL(blob);
    var audio = document.getElementById('audio');
    audio.src = url;
    audio.play();
    blob2base64(blob, onBase64Ready);
}

function onBase64Ready(base64) {
    var formData = new FormData();
    formData.append('audioBase64', base64);

    $.ajax({
        method: 'POST',
        url: '/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(res) {
            console.log(res);
        },
        error: function(res) {
            console.log(res);
        }
    })
}

function blob2base64(blob, cb) {
    var reader = new FileReader();
    reader.onload = function() {
        var dataUrl = reader.result;
        var base64 = dataUrl.split(',')[1];
        cb(base64);
    }
    reader.readAsDataURL(blob);
}

$(document).ready(function() {
    var recording = false;
    var shouldStop = true;
    var startLink = document.getElementById('start');
    var downloadLink = document.getElementById('download');
    var stopLink = document.getElementById('stop');
    var mediaRecorder;


    var handleSuccess = function(stream) {
        var options = {mimeType: 'audio/webm'};

        mediaRecorder = new MediaRecorder(stream, options);
        mediaRecorder.addEventListener('dataavailable', onRecordingReady);
        mediaRecorder.addEventListener('stop', onRecordingStopped);
        mediaRecorder.start();
        startLink.disabled = true;
    }

    stopLink.addEventListener('click', function() {
        mediaRecorder.stop();
        startLink.disabled = false;
    });

    startLink.addEventListener('click', function() {
        navigator.mediaDevices.getUserMedia({ audio: true, video: false })
            .then(handleSuccess);
    })
});
