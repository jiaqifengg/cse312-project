$(document).ready(function() {
    var socket = io.connect('http://127.0.0.1:5000');
    var socketMessages = io('http://127.0.0.01:5000/messages');

    $('#send').on('click', function () {
        var message = $('#messageChat').val();

        socketMessages.emit('message from user', message);
    });

    socketMessages.on('from flask', function(msg) {
        alert(msg);
    })

    socketMessages.on('server originated', function(msg) {
        alert(msg);
    });

    var privateSocket = io('http://127.0.0.1:5000/private');

    $('sendUsername')
});