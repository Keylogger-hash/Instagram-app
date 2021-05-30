window.onload = function(){
  var room_label = document.getElementById("chat-log").getAttribute('value')
  var connectionString = 'ws://'+window.location.host+'/ws/chat/'+room_label+'/'
  var socket = new WebSocket(connectionString);
  var form = document.getElementById("chat-message")
  var message = document.querySelector("#chat-message-input").innerHTML
  var data = {"message":message}
  const mydata = "{{room|escapejs}}"
  console.log(mydata)
  form.addEventListener('submit',function(event){
    event.preventDefault();
    socket.send(JSON.stringify(data))
    form.reset()
  })


  function connect(){
    socket.onopen = function(event){
      console.log('socket is connected');
    }
    socket.onclose = function(event){
      console.log('socket is disconnected');
    }
    socket.onmessage = function(event){
      let data = JSON.parse(e.data);
      console.log(data)
    }
  }

  connect()
}
