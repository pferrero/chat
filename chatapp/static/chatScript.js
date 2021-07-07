var messageList;
var contact;
var divMessages;

var loadMessages = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            messageList = JSON.parse(this.responseText);
            fill();
        }
    };
    xhttp.open("GET", "/messages/" + contact, true);
    xhttp.send();
}

var sendMessage = function(msg) {
    var xhhtp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            clearMessages();
            fill();
        }
    };
    xhttp.open("POST", "/sendMessage/" + contact, true);
    // params
    xhttp.send();
}
  
function createMessage(name, msg, time) {
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
    divMessages.appendChild(newMsg, divMessages.firstChild);
    // Scroll to bottom
    divMessages.scrollTop = divMessages.scrollHeight;
}

function clearMessages() {
    divMessages.innerText = '';
}

function fill() {
    messageList.forEach(item => createMessage(item.sender, item.message, item.time));
}

function init() {
    divMessages = document.getElementById("divMessages");
    contact = document.getElementById("contact").textContent;
    loadMessages();
}