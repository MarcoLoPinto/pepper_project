class FaceRecognitionClient {

    constructor({receiveListener = (command) => {}, onConnect = () => {}, onDisconnect = () => {}}){
        // RAIM Client
        this.RAIMClient = new RAIMClient("facerecognitionclient");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(receiveListener);
        this.RAIMClient.onDisconnect = onDisconnect;
        
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(onConnect);
    }
    
    /**
     * Sends the base64 string encoded image to the face recognition server
     *
     * @param {string} img - The base64 string encoded image
     * @param {boolean} request - If true, it expects a response from the server
     * @returns {Promise}
     */
    sendFrame(img, request = false) {
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
     * @param {Object.<number, string>} faces - An object containing integer keys representing unknown faces and their corresponding string values representing their names.
     * @param {boolean} request - If true, it expects a response from the server
     * @returns {Promise}
     */
    setUnknownFaces(faces, request = false) {
        let command = new RAIMClient.Command({
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
     * @param {number} value - The number of frames to wait before a possible unknown face is really unknown
     * @param {boolean} request - If true, it expects a response from the server
     * @returns {Promise}
     */
    setUnknownFaceThreshold(value, request = true) {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": "set_unknown_face_threshold",
                    "action_properties": {"value":value}
                }]
            },
            to_client_id: "face_recognition",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command);
    }

    /**
     * Initializes the face recognition system (must be a request!)
     *
     * @param {number} unknown_face_threshold - The number of frames to wait before a possible unknown face is really unknown
     * @param {number} resize_value - The number of frames to wait before a possible unknown face is really unknown (defaults to 4)
     * @returns {Promise}
     */
    initFaceRecognition(unknown_face_threshold, resize_value = 4) {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": "init_face_recognition",
                    "action_properties": {
                        "resize_value":resize_value,
                        "unknown_face_threshold":unknown_face_threshold
                    }
                }]
            },
            to_client_id: "face_recognition",
            request: true,
        });
        return this.RAIMClient.dispatchCommand(command);
    }
    
}