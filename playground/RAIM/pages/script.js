
const form = document.getElementById("form")
const byeButton = document.getElementById('bye-btn');
const messageInput = document.getElementById('message-input');

form.addEventListener('submit', (e) => {
    e.preventDefault()
    const message = messageInput.value.trim();
    if (message.length == 0) return
    command = new RAIMClient.Command({data:{
        msg: message
    }})
    RAIMClient.dispatchCommand(command)
    // socket.emit('command', command.toJson());
    messageInput.value = '';
});

byeButton.addEventListener('click', (e) => {
    e.preventDefault()
    command = new RAIMClient.Command({data:{
        msg: "BYE"
    }})
    RAIMClient.dispatchCommand(command)
    // socket.emit('command', command.toJson());
});


// socket.on('command', (message) => {
//     console.log('Received message:', message);
// });
RAIMClient.setCommandListener((command)=>{
    console.log('Received command:', command);
})

