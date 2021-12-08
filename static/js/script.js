$(document).ready(function () {
  var socket = io("http://" + document.domain + ":" + location.port);

  //on connect go to "connected"
  // socket.on("connect", function () {
  //   socket.emit("connected", "I am connected");
  // });
  //when the server sends the username, send it back to the server as "user"
  socket.on("connected", function (username) {
    socket.emit("user", username);
  });

  //on click for send messages
  $("#send").on("click", function () {
    var message = $("#myMessage").val();
    var toUser = $("#currentUser").text();
    socket.emit("private_message", {
      msg: message,
      To: toUser,
    });
  });

  //display incoming messages
  socket.on("private_message", function (msg) {
    $("#middle-display")[0].innerHTML +=
      '<p style="overflow-wrap: break-word; width: 100%;">' + msg + "</p>";

    //console.log(msg)
    // alert(msg)
  });
  //display message sent as well
  socket.on("curent_user_message", function (msg) {
    $("#middle-display")[0].innerHTML +=
      '<p style="overflow-wrap: break-word; width: 100%;">' + msg + "</p>";

    //console.log(msg)
  });

  //click on the user you want to dm
  $(".user").click(function () {
    newUser = $(this).text();
    currentUser = $("#currentUser").text();
    if (currentUser != newUser) {
      document.getElementById("currentUser").innerHTML = newUser;
      //console.log(currentUser)
    }

    //console.log($(this).text());
  });

  //console.log($(this).text());
  $("#send_post").on("click", function () {
    var post_msg = $("#postMessage").val();
    var from_user = $("#username_post").text();
    socket.emit("make_post", { post: post_msg, from: from_user });
  });
});
