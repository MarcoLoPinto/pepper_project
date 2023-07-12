const cameraList = document.getElementById('camera-list');
const connectButton = document.getElementById('connect-button');
const video = document.getElementById('video');
const debugOutput = document.getElementById('debug');

class PepperBrowser {
    constructor({RAIMClient = null, min_ms_interval = 500, camera_type = config.camera_type}){
        this.RAIMClient = RAIMClient;
        this.min_ms_interval = min_ms_interval;
        this.camera_type = camera_type;
        this.last_frame_time = Date.now();
        
        this.initState(); // Memory state of the machine
        this.RAIMClient.setCommandListener(this.receiveListener.bind(this));

        this.startCamera();
    }

    initState(){
        this.state = {
            "camera_enabled": false,
            "camera_enabled_errors": 0,
            "chosen_one": undefined,
            // "current_frame": undefined,
            // "current_frame_request_ms_time_max": 1000,
        }
    }

    startCamera(){
        if(this.state.camera_enabled){
            console.log('Camera is already enabled!');
            return;
        }
        switch (this.camera_type){
            default:
            case "browser":
                this.startCameraBrowser();
                break;
            case "robot":
                this.startCameraRobot();
                break;
        }
    }
    
    startCameraBrowser(){
        navigator.mediaDevices.getUserMedia({audio: true, video: true})
            .then(()=> {
                navigator.mediaDevices.enumerateDevices()
                    .then(devices => {
                        // Filter the list to include only video devices
                        const videoDevices = devices.filter(device => device.kind === 'videoinput');
                        console.log("cameras discovered:", videoDevices);
                        if(videoDevices.length > 0) {
                            // Populate the drop-down menu with the names of the video devices
                            const device = videoDevices[0];
                            // Request access to the selected camera
                            navigator.mediaDevices.getUserMedia({ video: { deviceId: device.deviceId } })
                                .then(stream => {
                                    // Display the video stream in the <video> element
                                    video.srcObject = stream;

                                    let command = new RAIMClient.Command({
                                        data:{
                                            "action_type_callback": "start_video",
                                            "action_properties": {"success": true}
                                        },
                                        to_client_id: "browser"
                                    });
                                    this.RAIMClient.dispatchCommand(command);
                                })
                                .catch(error => {
                                    console.error('Error accessing camera:', error);
                                    debugOutput.innerText = 'Error accessing camera:' + error;

                                    let command = new RAIMClient.Command({
                                        data:{
                                            "action_type_callback": "start_video",
                                            "action_properties": {"success": false}
                                        },
                                        to_client_id: "browser"
                                    });
                                    this.RAIMClient.dispatchCommand(command);
                                });
                        } else {
                            console.error('No cameras found!');

                            let command = new RAIMClient.Command({
                                data:{
                                    "action_type_callback": "start_video",
                                    "action_properties": {"success": false}
                                },
                                to_client_id: "browser"
                            });
                            this.RAIMClient.dispatchCommand(command);
                        }
                        
                    })
                    .catch(error => {
                        console.error('Error enumerating devices:', error);

                        let command = new RAIMClient.Command({
                            data:{
                                "actions": [{
                                    "action_type_callback": "start_video",
                                    "action_properties": {"success": false}
                                }]
                            },
                            to_client_id: "browser"
                        });
                        this.RAIMClient.dispatchCommand(command);
                    })
            })
    }

    checkIfVideoIsEnabled(command){
        let isEnabled = command.data.action_properties.success;
        if(isEnabled) {
            this.state.camera_enabled = true;
            console.log("Cameras enabled!");
            this.sendFrameCameraRequest();
        }
        else if(!isEnabled && this.camera_enabled_errors < 1) {
            console.error(`Camera not enabled using ${this.camera_type}, trying the other one...`);
            this.camera_enabled_errors = 1;
            this.camera_type = "robot";
            this.startCameraRobot();
        } 
        else {
            console.error(`Camera not enabled, tried robot and browser`);
        }
    }

    startCameraRobot(){
        let command = new RAIMClient.Command({
            data:{
                "actions": [{"action_type": "start_video"}]
            },
            to_client_id: "pepper"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    getFrameCameraBrowser(){
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const base64ImageData = canvas.toDataURL('image/jpeg');
        return base64ImageData;
    }

    sendFrameCameraRequest() {
        if(this.camera_type == "browser") this.sendFrameCameraBrowserRequest();
        else if(this.camera_type == "robot") this.sendFrameCameraRobotRequest();
    }

    sendFrameCameraBrowserRequest(){
        let command = new RAIMClient.Command({
            data:{"img": this.getFrameCameraBrowser()},
            to_client_id: "browser"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    sendFrameCameraRobotRequest(){
        let command = new RAIMClient.Command({
            data:{
                "actions": [{
                    "action_type": "take_fake_video_frame", // TODO: to change into "take_video_frame"! Here taking the fake image!
                }]
            },
            to_client_id: "pepper"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    sendFrameToFaceRecognition(base64ImageData){
        console.log("Sending frame to face recognition...");
        let command = new RAIMClient.Command({
            data:{
                "actions": [{
                    "action_type": "run_recognition_frame",
                    "action_properties": {"img": base64ImageData}
                }]
            },
            to_client_id: "face_recognition"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    receiveListener(command) {
        if(
            (
                command.from_client_id == "pepper" ||
                command.from_client_id == "browser"
            ) && (
                "action_type_callback" in command.data &&
                command.data["action_type_callback"] == "start_video"
            )
        ) this.checkIfVideoIsEnabled(command);

        else if(command.from_client_id == "face_recognition") this.listenerFaceRecognition(command);
        else if(
            (
                command.from_client_id == "pepper" ||
                command.from_client_id == "browser"
            ) && (
                "img" in command.data
            )
        ) this.sendFrameToFaceRecognition(command.data["img"]);
        else return;
    }

    listenerFaceRecognition(command) {
        let deltaTime = Date.now() - this.last_frame_time;
        if(deltaTime < this.min_ms_interval) deltaTime = this.min_ms_interval;
        else deltaTime = 1;
        if(["known_faces", "cropped_unknown_faces"].every(key => command.data.hasOwnProperty(key))){
            let known_faces_names = Object.keys(command.data["known_faces"]);
            debugOutput.innerText = "known faces: " + known_faces_names.join(', ') + " | unknown n°: " + Object.keys(command.data["cropped_unknown_faces"]).length
            
            
        }

        console.log(command)
        
        setTimeout(()=>{
            this.last_frame_time = Date.now();
            this.sendFrameCameraRequest();
        }, deltaTime);
    }

}

(()=>{
    let pepperbrowser = new PepperBrowser({RAIMClient: RAIMClient});
})();

