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
      document.getElementById("middle-display").innerHTML = "";
      //console.log(currentUser)
    }
    //console.log($(this).text());
  });

  $("#send_post").on("click", function () {
    var post_msg = $("#postMessage").val();
    var from_user = $("#username_post").text();
    socket.emit("create_post", { post: post_msg, from: from_user });
  });

  socket.on("make_post", function (data) {
    console.log("here")
    console.log(data)
    var overallDiv = html_post(data)
    $("#postArea")[0].innerHTML += overallDiv
  });

  function html_post(data) {
    var post_id = data["post-id"];
    var post = data["post"];
    var username = data["user"][0];
    var userImg = data["user"][1];
    var countUp = Object.keys(data["upvotes"]).length;
    var countDown = Object.keys(data["downvotes"]).length;

    var overallDiv = '<div class="overall">\
                        <li class="box">\
                          <div class="chatProfile">\
                            <img class="profileImageIcon" src=' + String(userImg) + '>\
                            <h6>' + username + '<h6>\
                          </div>\
                          <p class="message">' + post + '</p>\
                        </li>\
                        <div class="chatComponent" id="post_' + String(post_id) + '">\
                          <button id="upButton">Upvote <span class="badge badge-primary badge-pill" id="upCounts">' + String(countUp) + '</span></button><br>\
                          <button id="downButton">Downvote <span class="badge badge-primary badge-pill" id="downCounts">' + String(countDown) + '</span></button>\
                        </div>\
                    </div>\
                    <br>'
    return overallDiv
  };

  $("#upButton").on("click", function () {
    var vote = 1
    var id = $(this).parent().attr('id');
    var post_id = id.split("_")[1];
    console.log(id)
    console.log(post_id);
    socket.emit("vote", { vote: vote});
  });

});
