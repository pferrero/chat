var messageList;

var loadMessages = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            messageList = JSON.parse(this.responseText);
        }
    };
    xhttp.open("GET", "/messages", true);
    xhttp.send();
}
//<img src="/w3images/bandmember.jpg" alt="Avatar">
//<p>Hello. How are you today?</p>
//<span class="time-right">11:00</span>
  
function createMessage(name, msg, time) {
    var divMessages = document.getElementById("divMessages");
    // Create new div message
    var newMsg = document.createElement("div");
    newMsg.classList.add("chatContainer")
    // Create new title for message (name of the sender)
    var newTitle = document.createElement("span");
    newTitle.innerText = name;
    newMsg.appendChild(newTitle);
    // Create new paragraph for message (content of message)
    var newText  = document.createElement("p");
    newText.innerText = msg;
    newMsg.appendChild(newText);
    // Create new time for message
    var newTime  = document.createElement("span");
    newTime.innerText = time;
    newMsg.appendChild(newTime);
    
    // Add message to chat
    divMessages.insertBefore(newMsg, divMessages.firstChild);
    // Scroll to bottom
    divMessages.scrollTop = divMessages.scrollHeight;
}

loadMessages();
function fill() {
    messageList.forEach(item => createMessage(item.sender, item.message, item.time));
}