class PepperClient {
    static MOVE_NAMES = ["bothArmsBumpInFront", "fancyRightArmCircle", "normalPosture"];
    constructor(){
        this.RAIMClient = undefined;
    }

    sayMove({text, move_name, request}) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": "say_move",
                    "action_properties": {
                        "text": text,
                        "move_name": move_name
                    }
                }]
            },
            to_client_id: "pepper",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command_in);
    }

}