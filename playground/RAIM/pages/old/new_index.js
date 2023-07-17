// index page
const video = document.getElementById('video');
const video_back = document.getElementById('video_back');
const label_pepper_see = document.getElementById('label_pepper_see');
const index_pepper_logo = document.getElementById('index_pepper_logo');

const cropped_unk_face = document.getElementById('cropped_unk_face');
const cropped_unk_face_text = document.getElementById('cropped_unk_face_text');

class PepperBrowser {
    constructor(
        {
            min_ms_interval = 800,
            unknown_face_threshold = 4,
            chosen_one_max_threshold = 8,
            camera_type = config.camera_type,
            lang = "en-US",
            debug = true,
        }
    ) {

        this.initState(); // Initial state of the machine

        // Logger
        this.console = new BetterConsole({enabled: debug});
        // Speech-to-text service
        this.stt = new SpeechRecognitionBrowser(lang);
        // language
        this.languageText = new LanguageText(
            lang, 
            {
                "YES": {
                    "en-US": "yes",
                    "it-IT": "si"
                },
                "NO": {
                    "en-US": "no",
                    "it-IT": "no"
                },
                "DETECT_NEW_FACES": {
                    "en-US": "I'm detecting new faces!",
                    "it-IT": "Vedo delle possibili facce nuove!"
                },
                "PEPPER_LOST_CHOSEN_ONE": {
                    "en-US": "Oh no, I lost you. Come back whenever you want!",
                    "it-IT": "Oh no, ti ho perso di vista. Ritorna quando vuoi!"
                },
                "PEPPER_EXPERT_USER_INTRO": {
                    "en-US": "Welcome back %s! Do you want that I explain again the game?",
                    "it-IT": "Ciao di nuovo %s! Vuoi che ti spieghi di nuovo il gioco?"
                },
                "PEPPER_NEW_USER_INTRO": {
                    "en-US": "Hello %s! My name is PepperTale! Do you want an explanation of the game?",
                    "it-IT": "Piacere di conoscerti %s! Vuoi che ti spieghi come funziona il gioco?"
                }
            },
            (lang) => {
                this.stt.recognition.lang = lang;
            }
        );

        this.console.log("Chosen min_ms_time:", min_ms_interval, "Chosen camera:", camera_type)

        this.min_ms_interval = min_ms_interval;
        this.CHOSEN_ONE_MAX_THRESHOLD = chosen_one_max_threshold;
        this.camera_type = camera_type;
        this.last_frame_time = Date.now();

        // RAIM Client
        this.RAIMClient = new RAIMClient("browser");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(this.receiveListener.bind(this));
        this.RAIMClient.onDisconnect = () => {/* TODO */}
        
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(async ()=>{

            try {
                let responseCommand = await this.setUnknownFaceThreshold(unknown_face_threshold);
                this.console.log("Starting camera service...");
                await this.startCamera();
            } catch (error) {
                this.console.error("Something went wrong on the face recognition server");
            }

        });

    }

    initState() {
        this.state = {
            "starting_page": "index_page",
            "camera_enabled": false,
            "camera_enabled_errors": 0,
            // we need to choose one person for the game
            "chosen_one": undefined,
            "is_chosen_one_new": false,
            "cropped_unknown_faces": {},
            "new_faces": [],
            // we need to consider a threshold that if for N frames we don't see the chosen one, then we need to select another one!
            "chosen_one_threshold": 0,
        }

        // Routing
        this.routing = new Routing(this.state.starting_page);
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
            to_client_id: "face_recognition",
            request: true,
        });
        return this.RAIMClient.dispatchCommand(command);
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

        let startCameraCommand = (is_successful) => new RAIMClient.Command({
            data: {
                "action_type": "start_video", "is_successful": is_successful
            },
            to_client_id: "browser"
        });

        navigator.mediaDevices.getUserMedia({ audio: true, video: true })
            .then(() => {
                navigator.mediaDevices.enumerateDevices()
                    .then(devices => {
                        // Filter the list to include only video devices
                        const videoDevices = devices.filter(device => device.kind === 'videoinput');
                        this.console.log("Cameras discovered:", videoDevices);
                        if (videoDevices.length > 0) {
                            // Populate the drop-down menu with the names of the video devices
                            const device = videoDevices[0];
                            // Request access to the selected camera
                            navigator.mediaDevices.getUserMedia({ video: { deviceId: device.deviceId } })
                                .then(stream => {
                                    // Display the video stream in the <video> element
                                    video.srcObject = stream;
                                    index_pepper_logo.style = "width: 30vh;";
                                    this.RAIMClient.dispatchCommand(startCameraCommand(true));
                                })
                                .catch(error => {
                                    this.console.error('Error accessing camera:', error);
                                    label_pepper_see.innerText = 'Error accessing camera:' + error;
                                    this.RAIMClient.dispatchCommand(startCameraCommand(false));
                                });
                        } else {
                            this.console.error('No cameras found!');
                            label_pepper_see.innerText = 'No cameras found!';
                            this.RAIMClient.dispatchCommand(startCameraCommand(false));
                        }

                    })
                    .catch(error => {
                        console.error('Error enumerating devices:', error);
                        label_pepper_see.innerText = 'Error enumerating devices';
                        this.RAIMClient.dispatchCommand(startCameraCommand(false));
                    })
            })
    }

    startCameraRobot() {
        let command = new RAIMClient.Command({
            data: {
                "actions": [{ "action_type": "start_video" }]
            },
            to_client_id: "pepper"
        });
        return this.RAIMClient.dispatchCommand(command);
    }

    checkIfVideoIsEnabled(command) {
        let isEnabled = command.data.is_successful;
        if (isEnabled) {
            this.state.camera_enabled = true;
            console.log(`Camera ${this.camera_type} enabled!`);
            this.sendFrameCameraRequestDeltaTime();
        }
        else if (!isEnabled && this.camera_enabled_errors < 1) {
            console.error(`Camera not enabled using ${this.camera_type}, trying the other one...`);
            this.camera_enabled_errors += 1;
            if (this.camera_type == "browser") {
                this.camera_type = "robot";
                this.startCameraRobot();
            } else {
                this.camera_type = "browser";
                this.startCameraBrowser();
            }

        }
        else {
            console.error(`Camera not enabled, tried ${this.camera_enabled_errors} times`);
        }
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
        if (this.camera_type == "browser") this.sendFrameCameraBrowserRequest();
        else if (this.camera_type == "robot") this.sendFrameCameraRobotRequest();
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
            data: { 
                "action_type": "take_video_frame", 
                "action_properties": { "img": this.getFrameCameraBrowser() } 
            },
            to_client_id: "browser"
        });
        return this.RAIMClient.dispatchCommand(command);
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
        return this.RAIMClient.dispatchCommand(command);
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
        console.log(command);

        if (
            (
                command.from_client_id == "pepper" ||
                command.from_client_id == "browser"
            ) && (
                "action_type" in command.data &&
                command.data["action_type"] == "start_video"
            )
        ) this.checkIfVideoIsEnabled(command);

        else if (command.from_client_id == "face_recognition") this.listenerFaceRecognition(command);
        else if (
            (
                command.from_client_id == "pepper" ||
                command.from_client_id == "browser"
            ) && (
                "action_properties" in command.data &&
                "img" in command.data["action_properties"]
            )
        ) this.sendFrameToFaceRecognition(command.data["action_properties"]["img"]);
        else return;
    }

    async listenerFaceRecognition(command) {
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
                    this.state.is_chosen_one_new = false;
                    // Inform the user that we lost it:
                    let command_out = await this.robotSayMove({
                        action_type:"say_move",
                        text: this.languageText.get("PEPPER_LOST_CHOSEN_ONE"),
                        move_name: "fancyRightArmCircle",
                        request: true
                    })
                    this.console.log("Pepper lost the chosen one!")
                }
            }
            else {
                if (known_faces_names.length > 0) {
                    let chosen_one = known_faces_names[0];
                    this.state.chosen_one = known_faces_names[0];
                    if(this.state.new_faces.includes(chosen_one)) this.state.is_chosen_one_new = true;
                    if(this.state.is_chosen_one_new) await this.talkToNewUser();
                    else await this.talkToExpertUser();
                }
                else if (Object.keys(command.data["cropped_unknown_faces"]).length > 0) {
                    // No known face, but there is someone that the robot does not know!
                    console.log("PHASE UNKNOWN: adding new faces!");
                    this.routing.goToPage("new_face_page");
                    await this.setNewFacesNames(command);
                }
            }

            // Output to label the info for the user!
            let out_text = "";
            if(this.state.chosen_one != undefined) {
                if(this.state.is_chosen_one_new) out_text = this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', this.state.chosen_one)
                else out_text = this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', this.state.chosen_one)
            }
            else {
                out_text = this.languageText.get("DETECT_NEW_FACES")
            }
            label_pepper_see.innerText = out_text;
        }

        this.sendFrameCameraRequestDeltaTime();
    }

    async setNewFacesNames(command) {
        const objList = [];
        for (const key in command.data["cropped_unknown_faces"]) {
            const value = command.data["cropped_unknown_faces"][key];
            const pair = [key, value];
            objList.push(pair);
        }
        await this.setNewFaceName(command, objList, 0);
    }
    async setNewFaceName(command, objList, idx) {
        if (objList.length <= idx) {
            // All names have been done, send them to face recognition...
            try {
                let command_in = new RAIMClient.Command({
                    data: {
                        "actions": [{ 
                            "action_type": "set_unknown_faces",
                            "action_properties": {"cropped_unknown_faces":this.state.cropped_unknown_faces}
                        }]
                    },
                    to_client_id: "face_recognition",
                    request: true,
                });
                let command_out = await this.RAIMClient.dispatchCommand(command_in);
                this.console.log("Success! Setting new faces here...");
                this.state.new_faces = this.state.new_faces.concat(command_out.data["new_faces"]);
            } catch (error) {
                this.console.error("Error on setting the new faces:",error);
            } finally {
                this.console.log("Going back to face selection...");
                this.routing.goBack();
                return;
            }
            
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
                this.setNewFaceName(command, objList, idx + 1);
            }
            else this.setNewFaceName(command, objList, idx);
        } catch (error) {
            this.setNewFaceName(command, objList, idx);
        }
        

    }

    robotSayMove({action_type, text, move_name, request}) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [{ 
                    "action_type": action_type,
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

    async talkToExpertUser() {
        // This user has already played check if user wants an explanation!
        let command_out = await this.robotSayMove({
            action_type:"say_move",
            text: this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', this.state.chosen_one),
            move_name: "fancyRightArmCircle",
            request: true
        });

        let confirm_text = await this.stt.startListening();
        if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
            await this.explainGameToUser();
        }
        // TODO: proceed with the game!

    }

    async talkToNewUser() {
        // This user is new, explain the game!
        let command_out = await this.robotSayMove({
            action_type: "say_move",
            text: this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', this.state.chosen_one),
            move_name: "fancyRightArmCircle",
            request: true
        });
        await this.explainGameToUser();
        // TODO: proceed with the game!
    }

    async explainGameToUser() {
        // TODO: This user wants an explaination!
    }

}

(() => {
    let pepperbrowser = new PepperBrowser({});
})();

