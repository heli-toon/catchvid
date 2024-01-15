var socket = new WebSocket('ws://' + window.location.host + '/progress/');
socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var percentage_of_completion = data.percentage_of_completion;
    var progress_bar = document.getElementById('progress-bar');
    progress_bar.value = percentage_of_completion;
};