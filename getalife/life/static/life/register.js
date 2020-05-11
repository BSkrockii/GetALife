function mouseoverDown(obj) {
    var obj = document.getElementById('password');
    obj.type = "text";
  }
  function mouseoutUp(obj) {
    var obj = document.getElementById('password');
    obj.type = "password";
  }
  function mouseoverDownPassRepear(obj) {
    var obj = document.getElementById('passrepeat');
    obj.type = "text";
  }
  function mouseoutUpPassRepeat(obj) {
    var obj = document.getElementById('passrepeat');
    obj.type = "password";
  }

  function checkUsername(){
    var username = document.getElementById('username').value;
    console.log(username.length)
    if (username.length > 3){
      $.ajax({
          type: "GET",
          url: "http://127.0.0.1:8000/checkUsername",
          dataType: "json",
          async: true,
          data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                  username: username},
          success: function (json){
              console.log("Success")
              if (json.username == true){
                  console.log("TRUE")

                  var obj = document.getElementById('checkUser');
                  obj.innerHTML = "Username is unavailable";
                  obj.style.color = "red";
                  
              }else{
                  console.log("FALSE")
                  var obj = document.getElementById('checkUser');
                  obj.innerHTML = "Username is available";
                  obj.style.color = "green";
              }
          }
      })
    }else{
        var obj = document.getElementById('checkUser');
        obj.innerHTML = "Must be longer";
        obj.style.color = "red";
    }
  }
