class PepperClient {
    
    static PepperAction = class {
        constructor(type, properties = {}){
            this.type = type
            this.properties = properties
        }
        
        toServerObj(){
            return { 
                "action_type": this.type,
                "action_properties": this.properties
            }
        }
    }

    static MOVE_NAMES = {
        bothArmsBumpInFront: "bothArmsBumpInFront", 
        fancyRightArmCircle: "fancyRightArmCircle", 
        normalPosture: "normalPosture"
    };
    static EYE_PARTS = {Both:"Both", Left:"Left", Right:"Right"}

    constructor({receiveListener = (command) => {}, onConnect = () => {}, onDisconnect = () => {}}){
        // RAIM Client
        this.RAIMClient = new RAIMClient("pepperclient");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(receiveListener);
        this.RAIMClient.onDisconnect = onDisconnect;
        
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(onConnect);
    }

    sendAction(action, request = true) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [action.toServerObj()]
            },
            to_client_id: "pepper",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command_in)
    }

    quit(){
        let action = new PepperClient.PepperAction("quit")
        return this.sendAction(action, false);
    }

    say(text, request = false) {
        let action = new PepperClient.PepperAction("say", {
            text
        })
        return this.sendAction(action, request);
    }

    stand(request = false) {
        let action = new PepperClient.PepperAction("stand")
        return this.sendAction(action, request);
    }


    move(move_name, request = false) {
        let action = new PepperClient.PepperAction("move",{
            move_name
        })
        return this.sendAction(action, request);
    }

    sayMove(text, move_name = MOVE_NAMES.bothArmsBumpInFront, request = false) {
        let action = new PepperClient.PepperAction("say_move", {
            text, move_name
        })
        return this.sendAction(action, request);
    }

    sayMoveLed(text, move_name = MOVE_NAMES.bothArmsBumpInFront, r = 0, g = 0, b = 1, duration = 10, part = EYE_PARTS.Both, request = false) {
        let action = new PepperClient.PepperAction("say_move_led", {
            text, move_name, r, g, b, duration, part
        })
        return this.sendAction(action, request);
    }

    startVideo(request){
        let action = new PepperClient.PepperAction("start_video")
        return this.sendAction(action, request);
    }

    takeVideoFrame(request){
        let action = new PepperClient.PepperAction("take_video_frame")
        return this.sendAction(action, request);
    }

    setVolume(value, request){
        let action = new PepperClient.PepperAction("set_volume",{value})
        return this.sendAction(action, request);
    }

    echo(text,request){
        let action = new PepperClient.PepperAction("echo",{text})
        return this.sendAction(action, request);
    }

    takeFakeVideoFrame(request){
        let action = new PepperClient.PepperAction("take_fake_video_frame")
        return this.sendAction(action, request);        
    }

}