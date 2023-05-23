
class Command {
    constructor({request = true, id = Math.floor(Math.random() * 9000) + 1000, data = {}}) {
        this.request = request;
        this.id = id;
        this.data = data;
    }

    toJson() {
        const j_obj = { "request": this.request, "id": this.id, "data": this.data };
        return JSON.stringify(j_obj);
    }

    toString() {
        return this.toJson();
    }

    static fromJson(json_str) {
        const j_obj = JSON.parse(json_str);
        return new Command(j_obj["request"], j_obj["id"], j_obj["data"]);
    }
}


const socket = io();

const form = document.getElementById("form")
const byeButton = document.getElementById('bye-btn');
const messageInput = document.getElementById('message-input');

form.addEventListener('submit', () => {
    const message = messageInput.value.trim();
    if (message.length == 0) return
    command = new Command({data:{
        msg: message
    }})
    socket.emit('command', command.toJson());
    messageInput.value = '';
});

byeButton.addEventListener('click', (e) => {
    e.preventDefault()
    command = new Command({data:{
        msg: "BYE"
    }})
    socket.emit('command', command.toJson());
});


socket.on('command', (message) => {
    console.log('Received message:', message);
});

