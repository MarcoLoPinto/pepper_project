const raimClient = new RAIMClient("browser")
raimClient.connect(...RAIMgetWebsocketUrlParams()).then(()=>{
    console.log("RAIMClient connected to server")
})

const form = document.getElementById("form")
const byeButton = document.getElementById('bye-btn');
const responseButton = document.getElementById('response-btn');
const messageInput = document.getElementById('message-input');

form.addEventListener('submit', (e) => {
    e.preventDefault()
    const message = messageInput.value.trim();
    if (message.length == 0) return
    command = new RAIMClient.Command({
        data:{
            msg: message
        },
        to_client_id: "talking_robot"
    })
    raimClient.dispatchCommand(command)
    // socket.emit('command', command.toJson());
    messageInput.value = '';
});

byeButton.addEventListener('click', async (e) => {
    e.preventDefault()
    command = new RAIMClient.Command({
        data:{
            msg: "BYE"
        },
        to_client_id: "talking_robot",
        request: true
    })
    raimClient.dispatchCommand(command, (command) => {
        console.log('Received last response:', command);
    })
    
    // socket.emit('command', command.toJson());
});

responseButton.addEventListener('click', async (e) => {
    e.preventDefault()
    command = new RAIMClient.Command({
        data:{
            msg: "BACK2"
        },
        to_client_id: "talking_robot",
        request: true
    })
    responseCommand = await raimClient.dispatchCommand(command)
    console.log('Received response:', command);
    // socket.emit('command', command.toJson());
});

// socket.on('command', (message) => {
//     console.log('Received message:', message);
// });
raimClient.setCommandListener((command)=>{
    console.log('Received command:', command);
})

