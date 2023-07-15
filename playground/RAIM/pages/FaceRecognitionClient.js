class FaceRecognitionClient {

    constructor({receiveListener = (command) => {}, onConnect = () => {}, onDisconnect = () => {}}){
        // RAIM Client
        this.RAIMClient = new RAIMClient("browser");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(receiveListener);
        this.RAIMClient.onDisconnect = onDisconnect;
        
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(onConnect);
    }
    
    /**
     * Sends the base64 string encoded image to the face recognition server
     *
     * @param {{ img: string; request?: boolean; }} options - An options object containing the following:
     * @param {Object.<number, string>} options.img - The base64 string encoded image
     * @param {boolean} options.request - If true, it expects a response from the server
     * @returns {Promise}
     */
    sendFrame({img, request}) {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{
                    "action_type": "run_recognition_frame",
                    "action_properties": { "img": img }
                }]
            },
            to_client_id: "face_recognition",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command);
    }
    
    /**
     * Sends the new face names to the face recognition server
     *
     * @param {{ faces: Object.<number, string>; request: boolean; }} options - An options object containing the following:
     * @param {Object.<number, string>} options.faces - An object containing integer keys representing unknown faces and their corresponding string values representing their names.
     * @param {boolean} options.request - If true, it expects a response from the server
     * @returns {Promise}
     */
    setUnknownFaces({faces, request}) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": "set_unknown_faces",
                    "action_properties": {"cropped_unknown_faces":faces}
                }]
            },
            to_client_id: "face_recognition",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command);
    }

    /**
     * Sends the value of the unknown face threshold to the face recognition server. 
     * This value decides how many frames a possible unknown face must be in it before classifying it as unknown (useful when wrongly detecting a known face as unknown).
     *
     * @param {{ faces: Object.<number, string>; request: boolean; }} options - An options object containing the following:
     * @param {Object.<number, string>} options.value - The number of frames to wait before a possible unknown face is really unknown
     * @param {boolean} options.request - If true, it expects a response from the server
     * @returns {Promise}
     */
    setUnknownFaceThreshold({value, request}) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": "set_unknown_faces",
                    "action_properties": {"cropped_unknown_faces":faces}
                }]
            },
            to_client_id: "face_recognition",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command);
    }
    
}