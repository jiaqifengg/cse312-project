var voting;
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
    // console.log(Object.keys(data).length)
    var overallDiv = html_post(data[Object.keys(data).length - 1]);
    $("#postArea")[0].innerHTML += overallDiv;
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
                          <button id="upButton" type="button" onclick="voting(this);">Upvote <span class="badge badge-primary badge-pill" id="upvotes_' + String(post_id) + '">' + String(countUp) + '</span></button><br>\
                          <button id="downButton" type="button" onclick="voting(this);">Downvote <span class="badge badge-primary badge-pill" id="downvotes_' + String(post_id) + '">'+ String(countDown) + '</span></button>\
                        </div>\
                    </div>\
                    <br>'
    return overallDiv
  };

  voting = function(element) {
    console.log("upButton func")
    var vote_type = $(element).attr('id');
    var id = $(element).parent().attr('id');
    var post_id = parseInt(id.split("_")[1]);
    var vote = ""
    if (vote_type == "upButton"){
      var vote = "upvotes";
    }else if (vote_type == "downButton"){
      var vote = "downvotes";
    }  
    var data = {vote: vote, post_id:post_id}
    console.log(data)
    socket.emit("vote", { vote: vote, post_id: post_id });
  };

  socket.on("updateVote", function(data){
    console.log("updateVote");
    console.log(post_data)
    var post_data = data["post_data"];
    
    var post_id = post_data['post-id'];
    var upvotes = post_data["upvotes"];
    var downvotes = post_data["downvotes"];
    var recount_upvotes = Object.keys(upvotes).length;
    var recount_downvotes = Object.keys(downvotes).length;
    console.log(post_id)
    console.log(post_data)
    console.log(recount_upvotes)
    console.log(recount_downvotes)
    var upvotes_id = "upvotes_" + String(post_id);
    var downvotes_id = "downvotes_" + String(post_id)
    document.getElementById(upvotes_id).innerHTML = recount_upvotes;
    document.getElementById(downvotes_id).innerHTML = recount_downvotes;
  });
});
