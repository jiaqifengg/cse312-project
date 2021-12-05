$(document).ready(function() {
    var socket = io('http://' + document.domain + ':' + location.port);

    socket.on('connect', () => {
         socket.emit("user",username);
    });
    


    //on click for send messages
    $('#send').on('click', function () {
        var message = $('#myMessage').val();
        var toUser = $('#toUser').val();
        socket.emit('private_message', {'username':username, 'msg':message, "To":toUser});
    });

    //display incoming messages
    socket.on("private_message", function(msg){
        $("#display")[0].innerHTML += "<h1>" + msg + "</h1>"
        console.log(msg)
        // alert(msg)
    })

    

});