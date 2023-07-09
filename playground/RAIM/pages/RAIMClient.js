RAIMClient = {
    Command: null,
    dispatchCommand: null, // Called to send a command to the server, that will forward it to all the connected ipc clients
    executeCommand: null, // Called when a command is sent from an ipc client to this browser
    setCommandListener: null // Sets the callback to receive commands from the ipc clients connected
}

RAIMClient.setCommandListener = function(callback) {
    this.executeCommand = callback
}.bind(RAIMClient);

(function(BlockObject){

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

    BlockObject.Command = Command

    const socket = io();

    /**
     * alled to send a command to the server, that will forward it to all the connected clients
     * @param {Command} command -- Command to send
     */
    BlockObject.dispatchCommand = function(command){
        socket.emit('command', command.toJson());
        console.log(`Sent command(${command.id}) to ipc clients`);
    }

    socket.on('command', (jsonCommand) => {
        let command = Command.fromJson(jsonCommand)
        console.log(`Received command(${command.id}) from ipc clients`);
        if( BlockObject.executeCommand != null ){
            BlockObject.executeCommand(command)
        }
    });


})(RAIMClient);
