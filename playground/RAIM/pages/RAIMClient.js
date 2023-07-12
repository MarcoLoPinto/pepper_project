class RAIMCommand {
    constructor({ request = true, id = Math.floor(Math.random() * 9000 + 1000), to_client_id = "0", from_client_id = "browser", data = {} }) {
        this.request = request;
        this.id = id
        this.to_client_id = to_client_id;
        this.from_client_id = from_client_id;
        this.data = data;
    }

    serialize() {
        return { "request": this.request, "id": this.id, "to_client_id": this.to_client_id, "from_client_id": this.from_client_id, "data": this.data };
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

    static fromObject(obj) {
        return new Command({ request: obj["request"], id: obj["id"], to_client_id: obj["to_client_id"], from_client_id: obj["from_client_id"], data: obj["data"] });
    }
}

class RAIMClient {

    static Command = RAIMCommand

    constructor(name = "RAIMClient_" + Math.floor(Math.random() * 9000 + 1000)) {
        this.name = name;
        this.generalCommandListener = null;
        this.onConnect = null;
        this.onDisconnect = null;
        this.responseCallbacks = {};
        this.socket = null;
    }

    connect(protocol = "ws", host = "localhost", port = 5002) {
        let portStr = port == 0 ? "" : `:${port}`
        this.socket = new WebSocket(`${protocol}://${host}${portStr}`);
        this.socket.onopen = () => {
            this.socket.send(this.name);
            if (this.onConnect) this.onConnect();
        };

        this.socket.onmessage = (event) => {
            const jsonCommand = event.data;
            let command = typeof jsonCommand == "string" ? Command.fromJson(jsonCommand) : Command.fromObject(jsonCommand);
            console.log(`${this.name} received a command from ${command.from_client_id}: ${command.data}`);
            this.__internalDispatchCommand(command);
        };

        this.socket.onclose = () => {
            if (this.onDisconnect) this.onDisconnect();
        };
    }

    disconnect() {
        console.log(`Disconnecting RAIM client ${this.name}...`);
        this.socket.close();
        this.socket = null;
    }

    __internalDispatchCommand(command) {
        if (!command.request && this.responseCallbacks.hasOwnProperty(command.id)) {
            const responseCallback = this.responseCallbacks[command.id];
            delete this.responseCallbacks[command.id];
            responseCallback(command);
        } else if (this.generalCommandListener) {
            this.generalCommandListener(command);
        }
    }

    dispatchCommand(command, responseCallback = null) {
        if (command.from_client_id === "") {
            command.from_client_id = this.name;
        }
        if (responseCallback && command.request) {
            this.responseCallbacks[command.id] = responseCallback;
        }
        this.socket.send(command.toJson());
    }

    dispatchCommandPromise(command) {
        if (command.from_client_id === "") {
            command.from_client_id = this.name;
        }

        return new Promise((resolve, reject) => {

            if (command.request) {
                this.responseCallbacks[command.id] = (command) => {
                    resolve(command)
                };
            }

            try {
                this.socket.send(command.toJson());
            } catch (error) {
                reject(error);
            }
        });
    }

    setCommandListener(callback) {
        this.generalCommandListener = callback;
    }

    
}