// const websocket = new WebSocket("ws://192.168.50.158:8001");
// const websocket = new WebSocket("ws://127.0.0.1:8001"); //'me'
const websocket = new WebSocket("ws://192.168.50.246:8001");


function sendMessageToServer(data) {
    websocket.send(JSON.stringify(data));
}

const SINGLE_MESSAGE = 0;
const PREVIOUS_CHAT = 1;

// identify type of data that if coming from server
function identifyData(data){
    if(data.message) return SINGLE_MESSAGE;
    // if no message i must be reciveing a previous chat
    return PREVIOUS_CHAT;
}

// add one single message to list of messages
function addSingleMessage(data){
    const newSpan = document.createElement("span");
    newSpan.innerHTML =  data.message;
    logDiv.prepend(newSpan);
}

function addListOfMessages(list){
    for(const data of list){
        addSingleMessage(data);
    }
}

websocket.addEventListener("message", ({ data }) => {
    const parsedData = JSON.parse(data);

    console.log(parsedData);

    const dataType =  identifyData(parsedData);

    switch(dataType){
        case SINGLE_MESSAGE :
            addSingleMessage(parsedData)
            break
        case PREVIOUS_CHAT :
            addListOfMessages(parsedData)
            break
    }

    return false;
})