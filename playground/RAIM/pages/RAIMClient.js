function generateUUID() {
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = Math.random() * 16 | 0,
            v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
    return uuid;
}


class RAIMCommand {
    constructor({ request = false, id = generateUUID(), to_client_id = "0", from_client_id = "browser", data = {} }) {
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
        return RAIMCommand.fromObject(j_obj)
    }

    static fromObject(obj) {
        return new RAIMCommand({ request: obj["request"], id: obj["id"], to_client_id: obj["to_client_id"], from_client_id: obj["from_client_id"], data: obj["data"] });
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
        this.debug = true;
    }

    print(text) {
        if (this.debug) console.log(text)
    }

    connect(protocol = "ws", host = "localhost", port = 5002) {
        let portStr = port == 0 ? "" : `:${port}`
        this.socket = new WebSocket(`${protocol}://${host}${portStr}`);

        return new Promise((resolve, reject) => {

            this.socket.onopen = () => {
                this.socket.send(this.name);
                if (this.onConnect) this.onConnect();
                resolve()
            };

            this.socket.onmessage = (event) => {
                const jsonCommand = event.data;
                let command = typeof jsonCommand == "string" ? RAIMCommand.fromJson(jsonCommand) : RAIMCommand.fromObject(jsonCommand);
                this.print(`${this.name} received a command from ${command.from_client_id}: ${JSON.stringify(command.data)}`);
                this.__internalHandleReceivedCommand(command);
            };

            this.socket.onclose = () => {
                if (this.onDisconnect) this.onDisconnect();
            };
        })
    }

    disconnect() {
        console.log(`Disconnecting RAIM client ${this.name}...`);
        this.socket.close();
        this.socket = null;
    }

    __internalHandleReceivedCommand(command) {
        if (!command.request && this.responseCallbacks.hasOwnProperty(command.id)) {
            const responseCallback = this.responseCallbacks[command.id];
            delete this.responseCallbacks[command.id];
            responseCallback(command);
        } else if (this.generalCommandListener) {
            this.generalCommandListener(command);
        }
    }

    dispatchCommand(command, responseCallback = null) {
        /**
         * The then() callback is a function that gets the response command back
         */
        if (command.from_client_id === "") {
            command.from_client_id = this.name;
        }

        return new Promise((resolve, reject) => {

            if (command.request) {
                this.responseCallbacks[command.id] = (command) => {
                    if (responseCallback) responseCallback(command)
                    resolve(command)
                };
            }

            try {
                this.socket.send(command.toJson());
                this.print(`${this.name} sent a command to ${command.to_client_id}: ${JSON.stringify(command.data)}`);
            } catch (error) {
                reject(error);
            }
        });
    }

    // Retrocompatibility call. Uncomment if needed
    // dispatchCommandPromise(command){
    //     return this.dispatchCommand(command)
    // }

    setCommandListener(callback) {
        this.generalCommandListener = callback;
    }


}

function RAIMgetWebsocketUrlParams() {
    let domain = window.location.hostname
    let protocol = window.location.protocol === "https:" ? "wss" : "ws"
    if (domain == "localhost") {
        return [protocol, "localhost", Number(window.location.port) + 2]
    }
    else {
        return [protocol, "websocket." + domain, 0]
    }
}