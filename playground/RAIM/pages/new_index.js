const cameraList = document.getElementById('camera-list');
const connectButton = document.getElementById('connect-button');
const video = document.getElementById('video');
const video_back = document.getElementById('video_back');
const debugOutput = document.getElementById('debugOutput');

const cropped_unk_face = document.getElementById('cropped_unk_face');
const cropped_unk_face_text = document.getElementById('cropped_unk_face_text');

class PepperBrowser {
    constructor(
        {
            min_ms_interval = 800,
            unknown_face_threshold = 4,
            chosen_one_max_threshold = 8,
            camera_type = config.camera_type,
            lang = "en-US"
        }
    ) {
        this.min_ms_interval = min_ms_interval;
        this.CHOSEN_ONE_MAX_THRESHOLD = chosen_one_max_threshold;
        this.camera_type = camera_type;
        this.last_frame_time = Date.now();

        // language
        this.languageText = new LanguageText(lang, {
            "YES": {
                "en-US": "yes",
                "it-IT": "si"
            },
            "NO": {
                "en-US": "no",
                "it-IT": "no"
            }
        });
        // speech-to-text service:
        this.stt = new SpeechRecognitionBrowser(lang);

        // routing:
        this.routing = new Routing("index_page");

        console.log("Chosen min_ms_time:", min_ms_interval, "Chosen camera:", camera_type)

        this.initState(); // Memory state of the machine

        // RAIM Client
        this.RAIMClient = new RAIMClient("browser");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(this.receiveListener.bind(this));
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(()=>{
            this.setUnknownFaceThreshold(unknown_face_threshold);
            // this.startCamera();
        });
        this.RAIMClient.onDisconnect = () => {/* TODO */}

    }

    initState() {
        this.state = {
            "camera_enabled": false,
            "camera_enabled_errors": 0,
            // we need to choose one person for the game
            "chosen_one": undefined,
            "cropped_unknown_faces": {},
            "new_faces": [],
            // we need to consider a threshold that if for N frames we don't see the chosen one, then we need to select another one!
            "chosen_one_threshold": 0,
            // routing
            "route": "index_page",
        }
    }

    setUnknownFaceThreshold(number_of_frames) {
        this.unknown_face_threshold = number_of_frames;
        let command = new RAIMClient.Command({
            data: {
                "actions": [{
                    "action_type": "set_unknown_face_threshold",
                    "action_properties": { "value": number_of_frames }
                }]
            },
            to_client_id: "face_recognition"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    startCamera() {
        if (this.state.camera_enabled) {
            console.log('Camera is already enabled!');
            return;
        }
        switch (this.camera_type) {
            default:
            case "browser":
                this.startCameraBrowser();
                break;
            case "robot":
                this.startCameraRobot();
                break;
        }
    }

    startCameraBrowser() {
        navigator.mediaDevices.getUserMedia({ audio: true, video: true })
            .then(() => {
                navigator.mediaDevices.enumerateDevices()
                    .then(devices => {
                        // Filter the list to include only video devices
                        const videoDevices = devices.filter(device => device.kind === 'videoinput');
                        console.log("Cameras discovered:", videoDevices);
                        if (videoDevices.length > 0) {
                            // Populate the drop-down menu with the names of the video devices
                            const device = videoDevices[0];
                            // Request access to the selected camera
                            navigator.mediaDevices.getUserMedia({ video: { deviceId: device.deviceId } })
                                .then(stream => {
                                    // Display the video stream in the <video> element
                                    video.srcObject = stream;

                                    let command = new RAIMClient.Command({
                                        data: {
                                            "action_type_callback": "start_video",
                                            "action_properties": { "success": true }
                                        },
                                        to_client_id: "browser"
                                    });
                                    this.RAIMClient.dispatchCommand(command);
                                })
                                .catch(error => {
                                    console.error('Error accessing camera:', error);
                                    debugOutput.innerText = 'Error accessing camera:' + error;

                                    let command = new RAIMClient.Command({
                                        data: {
                                            "action_type_callback": "start_video",
                                            "action_properties": { "success": false }
                                        },
                                        to_client_id: "browser"
                                    });
                                    this.RAIMClient.dispatchCommand(command);
                                });
                        } else {
                            console.error('No cameras found!');

                            let command = new RAIMClient.Command({
                                data: {
                                    "action_type_callback": "start_video",
                                    "action_properties": { "success": false }
                                },
                                to_client_id: "browser"
                            });
                            this.RAIMClient.dispatchCommand(command);
                        }

                    })
                    .catch(error => {
                        console.error('Error enumerating devices:', error);

                        let command = new RAIMClient.Command({
                            data: {
                                "actions": [{
                                    "action_type_callback": "start_video",
                                    "action_properties": { "success": false }
                                }]
                            },
                            to_client_id: "browser"
                        });
                        this.RAIMClient.dispatchCommand(command);
                    })
            })
    }

    checkIfVideoIsEnabled(command) {
        let isEnabled = command.data.action_properties.success;
        if (isEnabled) {
            this.state.camera_enabled = true;
            console.log("Cameras enabled!");
            this.sendFrameCameraRequestDeltaTime();
        }
        else if (!isEnabled && this.camera_enabled_errors < 1) {
            console.error(`Camera not enabled using ${this.camera_type}, trying the other one...`);
            this.camera_enabled_errors = 1;
            if (this.camera_type == "browser") {
                this.camera_type = "robot";
                this.startCameraRobot();
            } else {
                this.camera_type = "browser";
                this.startCameraBrowser();
            }

        }
        else {
            console.error(`Camera not enabled, tried robot and browser`);
        }
    }

    startCameraRobot() {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{ "action_type": "start_video" }]
            },
            to_client_id: "pepper"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    getFrameCameraBrowser() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const base64ImageData = canvas.toDataURL('image/jpeg');
        return base64ImageData;
    }

    sendFrameCameraRequest() {
        if (this.isFrameCameraRequestActive != false) {
            if (this.camera_type == "browser") this.sendFrameCameraBrowserRequest();
            else if (this.camera_type == "robot") this.sendFrameCameraRobotRequest();
        }
    }

    stopFrameCameraRequest() {
        this.isFrameCameraRequestActive = false;
    }

    startFrameCameraRequest() {
        this.isFrameCameraRequestActive = true;
    }

    sendFrameCameraRequestDeltaTime() {
        let deltaTime = Date.now() - this.last_frame_time;
        if (deltaTime < this.min_ms_interval) deltaTime = this.min_ms_interval;
        else deltaTime = 1;
        setTimeout(() => {
            this.last_frame_time = Date.now();
            this.sendFrameCameraRequest();
        }, deltaTime);
    }

    sendFrameCameraBrowserRequest() {
        let command = new RAIMClient.Command({
            data: { "img": this.getFrameCameraBrowser() },
            to_client_id: "browser"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    sendFrameCameraRobotRequest() {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{
                    "action_type": "take_fake_video_frame", // TODO: to change into "take_video_frame"! Here taking the fake image!
                }]
            },
            to_client_id: "pepper"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    sendFrameToFaceRecognition(base64ImageData) {
        console.log("Sending frame to face recognition...");
        let command = new RAIMClient.Command({
            data: {
                "actions": [{
                    "action_type": "run_recognition_frame",
                    "action_properties": { "img": base64ImageData }
                }]
            },
            to_client_id: "face_recognition"
        });
        this.RAIMClient.dispatchCommand(command);
    }

    receiveListener(command) {
        console.log(command)

        if (
            (
                command.from_client_id == "pepper" ||
                command.from_client_id == "browser"
            ) && (
                "action_type_callback" in command.data &&
                command.data["action_type_callback"] == "start_video"
            )
        ) this.checkIfVideoIsEnabled(command);

        else if (command.from_client_id == "face_recognition") this.listenerFaceRecognition(command);
        else if (
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
        if (["known_faces", "cropped_unknown_faces"].every(key => command.data.hasOwnProperty(key))) {
            let known_faces_names = Object.keys(command.data["known_faces"]);
            // Threshold for the chosen one
            if (this.state.chosen_one != undefined) {
                if (known_faces_names.includes(this.state.chosen_one)) this.state.chosen_one_threshold = 0;
                else this.state.chosen_one_threshold += 1;
                if (this.state.chosen_one_threshold >= this.CHOSEN_ONE_MAX_THRESHOLD) {
                    // We lost the chosen one! We need a new candidate!
                    // TODO: choose how to reset: we reload the page or run an init again? Reload is easier but the page needs to reload correctly!
                    this.state.chosen_one = undefined;
                }
            }
            else {
                if (known_faces_names.length > 0) {
                    this.state.chosen_one = known_faces_names[0];
                    // TODO: send to the robot the say commmand "I know you..."
                }
                else if (Object.keys(command.data["cropped_unknown_faces"]).length > 0) {
                    // No known face, but there is someone that the robot does not know!
                    console.log("PHASE UNKNOWN: adding new faces!")
                    this.stopFrameCameraRequest();
                    this.routing.goToPage("new_face_page");
                    this.setNewFacesNames(command.data["cropped_unknown_faces"]);
                }
            }

            debugOutput.innerText = (
                "chosen one: " + this.state.chosen_one +
                " | known faces: " + known_faces_names.join(', ') +
                " | unknown n°: " + Object.keys(command.data["cropped_unknown_faces"]).length +
                " | threshold: " + this.state.chosen_one_threshold
            );
        }

        this.sendFrameCameraRequestDeltaTime();
    }

    setNewFacesNames(cropped_unk_faces) {
        const objList = [];
        for (const key in cropped_unk_faces) {
            const value = cropped_unk_faces[key];
            const pair = [key, value];
            objList.push(pair);
        }
        this.setNewFaceName(objList, 0);
    }
    async setNewFaceName(objList, idx) {
        console.log(objList, idx)
        if (objList.length <= idx) {
            // All names have been done, send them to face recognition...
            // TODO
            return;
        };
        let [key, value] = objList[idx];

        try {
            cropped_unk_face_text.innerText = "What is the name of this person?"
            cropped_unk_face.src = value;
            let name_text = await this.stt.startListening();
            cropped_unk_face_text.innerText = name_text + ", correct?";

            let confirm_text = await this.stt.startListening();
            cropped_unk_face_text.innerText += " " + confirm_text;

            if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                this.state.cropped_unknown_faces[key] = name_text;
                this.state.new_faces.push(name_text);
                this.setNewFaceName(objList, idx + 1);
            }
            else this.setNewFaceName(objList, idx);
        } catch (error) {
            this.setNewFaceName(objList, idx);
        }
        

    }

}

(() => {
    let pepperbrowser = new PepperBrowser({});
})();

