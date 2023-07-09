RAIMClient = {
    Command: null,
    dispatchCommand: null, // Called to send a command to the server, that will forward it to all the connected ipc clients
    executeCommand: null, // Called when a command is sent from an ipc client to this browser
    setCommandListener: null, // Sets the callback to receive commands from the ipc clients connected,
    debugPrint: true
}

RAIMClient.setCommandListener = function(callback) {
    this.executeCommand = callback
}.bind(RAIMClient);

(function(BlockObject){

    function dbgLog(text){
        if(BlockObject.debugPrint) console.log(text)
    }

    class Command {
        constructor({request = true, to_client_id = "0", from_client_id="browser", data = {}}) {
            this.request = request;
            this.to_client_id = to_client_id;
            this.from_client_id = from_client_id;
            this.data = data;
        }

        serialize(){
            return { "request": this.request, "to_client_id": this.to_client_id, "from_client_id": this.from_client_id, "data": this.data };            
        }
    
        toJson() {
            const j_obj = this.serialize()
            return JSON.stringify(j_obj);
        }
    
        toString() {
            return this.toJson();
        }
    
        static fromJson(json_str) {
            const j_obj = JSON.parse(json_str);
            return Command.fromObject(j_obj)
        }

        static fromObject(obj){
            return new Command({request:obj["request"], to_client_id:obj["to_client_id"], from_client_id:obj["from_client_id"], data:obj["data"]}); 
        }
    }

    BlockObject.Command = Command

    const socket = io();
    dbgLog("Connected to socket server")

    /**
     * alled to send a command to the server, that will forward it to all the connected clients
     * @param {Command} command -- Command to send
     */
    BlockObject.dispatchCommand = function(command){
        if(command.from_client_id == "") command.from_client_id = "browser"
        socket.emit('command', command.toJson());
        dbgLog(`Sent command to ${command.to_client_id}`);
    }

    socket.on('command', (jsonCommand) => {
        let command = typeof jsonCommand == "string" ? Command.fromJson(jsonCommand) : Command.fromObject(jsonCommand) 
        dbgLog(`Received command from ${command.from_client_id}`);
        if( BlockObject.executeCommand != null ){
            BlockObject.executeCommand(command)
        }
    });


})(RAIMClient);
