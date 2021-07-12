var messageList;
var contact;
var divMessages;

var loadMessages = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            messageList = JSON.parse(this.responseText);
            clearMessages();
            fill();
        }
    };
    xhttp.open("GET", "/messages/" + contact, true);
    xhttp.send();
}

var sendMessage = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            loadMessages();
            document.getElementById("msg").value = '';
        }
    };
    xhttp.open("POST", "/sendMessage/" + contact, true);
    let formData = new FormData();
    formData.append("txtMessage", document.getElementById("msg").value);
    xhttp.send(formData);
}
  
function createMessage(name, msg, time) {
    // Create new div message
    var newMsg = document.createElement("div");
    if (name == contact) {
        newMsg.classList.add("fromThem");
    } else {
        newMsg.classList.add("fromMe");
    }
    // Create new title for message (name of the sender)
    var newTitle = document.createElement("span");
    if (name == contact) {
        newTitle.innerText = name;
    } else {
        newTitle.innerText = "me";
    }
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
    //document.getElementById("sendBtn").onclick = sendMessage;
    loadMessages();
}