// index page
const video = document.getElementById('video');
const video_back = document.getElementById('video_back');
const label_pepper_see = document.getElementById('label_pepper_see');
const index_pepper_logo = document.getElementById('index_pepper_logo');
// new face page
const cropped_unk_face = document.getElementById('cropped_unk_face');
const cropped_unk_face_text = document.getElementById('cropped_unk_face_text');
// explanation page
const label_explanation = document.getElementById('label_explanation');
// PRP page
const story_card_container = document.getElementById('card-container');
const prp_title = document.getElementById("prp_title");

class App {
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
        // Initial state of the app
        this.initState();
        // Logger
        this.console = new BetterConsole({ enabled: debug });
        // Speech-to-text service
        this.stt = new SpeechRecognitionBrowser(lang);
        // Language
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
                "AND": {
                    "en-US": "and",
                    "it-IT": "e"
                },
                "DETECT_NEW_FACES": {
                    "en-US": "I'm detecting new faces!",
                    "it-IT": "Vedo delle possibili facce nuove!"
                },
                "PEPPER_WHAT_IS_FACE_NAME": {
                    "en-US": "What is the name of this person?",
                    "it-IT": "Qual'è il nome di questa persona?"
                },
                "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION": {
                    "en-US": "So the name is %s, correct?",
                    "it-IT": "Quindi il nome è %s, corretto?"
                },
                "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION_YES": {
                    "en-US": "Ok, I'm saving the name then",
                    "it-IT": "Ok, allora mi salvo il nome"
                },
                "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION_NO": {
                    "en-US": "The name is not correct? Let's retry",
                    "it-IT": "Non è corretto? Allora riproviamo"
                },
                "PEPPER_WHAT_IS_FACE_AGE": {
                    "en-US": "And what is the age?",
                    "it-IT": "E qual'è l'età?"
                },
                "PEPPER_WHAT_IS_FACE_AGE_CONFIRMATION": {
                    "en-US": "So the age is %s, correct?",
                    "it-IT": "Quindi l'età è %s, corretto?"
                },
                "PEPPER_WHAT_IS_FACE_AGE_CONFIRMATION_YES": {
                    "en-US": "Ok, I'm saving the age then",
                    "it-IT": "Ok, allora mi salvo l'età"
                },
                "PEPPER_WHAT_IS_FACE_AGE_CONFIRMATION_NO": {
                    "en-US": "The age is not correct? Let's retry",
                    "it-IT": "Non è corretto? Allora riproviamo"
                },
                "PEPPER_WHAT_IS_FACE_SEX": {
                    "en-US": "And what is the sex?", // TODO: better something like "Are you a boy or a girl?"
                    "it-IT": "E qual'è il sesso?"
                },
                "PEPPER_WHAT_IS_FACE_SEX_CONFIRMATION": {
                    "en-US": "So the sex is %s, correct?", // TODO: better something like "So you're a %s, right?"
                    "it-IT": "Quindi il sesso è %s, corretto?"
                },
                "PEPPER_WHAT_IS_FACE_SEX_CONFIRMATION_YES": {
                    "en-US": "Ok, I'm saving the sex then",
                    "it-IT": "Ok, allora mi salvo il sesso"
                },
                "PEPPER_WHAT_IS_FACE_SEX_CONFIRMATION_NO": {
                    "en-US": "The sex is not correct? Let's retry",
                    "it-IT": "Non è corretto? Allora riproviamo"
                },
                "PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION": {
                    "en-US": "So the name is %s, the sex is %s and the age is %s, correct?",
                    "it-IT": "Quindi il nome è %s, il sesso è %s e l'età è %s, corretto?"
                },
                "PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION_YES": {
                    "en-US": "Ok, I'm saving these infos then",
                    "it-IT": "Ok, allora mi salvo queste informazioni"
                },
                "PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION_NO": {
                    "en-US": "They are not correct? Let's retry",
                    "it-IT": "Non son corretti? Allora riproviamo"
                },
                "PEPPER_NO_HEAR": {
                    "en-US": "I didn't hear your response, please speak up",
                    "it-IT": "Non ho sentito la tua risposta, per favore alza la voce"
                },
                "PEPPER_LOST_CHOSEN_ONE": {
                    "en-US": "Oh no, I lost you. Come back whenever you want!",
                    "it-IT": "Oh no, ti ho perso di vista. Ritorna quando vuoi!"
                },
                "PEPPER_EXPERT_USER_INTRO": {
                    "en-US": "Welcome back %s! Do you want me to explain the game again?",
                    "it-IT": "Ciao di nuovo %s! Vuoi che ti spieghi di nuovo il gioco?"
                },
                "PEPPER_NEW_USER_INTRO": {
                    "en-US": "Hello %s! My name is PepperTale! Do you want an explanation of the game?",
                    "it-IT": "Piacere di conoscerti %s! Vuoi che ti spieghi come funziona il gioco?"
                },
                "PEPPER_ASK_EXPLAIN_GAME": {
                    "en-US": "Do you want an explanation of the game?",
                    "it-IT": "Vuoi che ti spieghi come funziona il gioco?"
                },
                "PEPPER_EXPLAIN_GAME": {
                    "en-US": "I'm an interactive story telling robot. I'm going to propose you some stories. Pick one and we are going to tell it together. During the story, I'll choose an action and you'll choose the next one, until we reach a conclusion",
                    "it-IT": "Io sono un robot cantastorie interattive. TI proporrò alcune storie. Scegline una e la racconteremo insieme. Durante la storia, io sceglierò un azione e tu quella successiva, finche non raggiungiamo una conclusione"
                },
                "PEPPER_STORY_OVER_AGE": {
                    "en-US": "You said to be %s, so maybe you're too young for %s",
                    "it-IT": "Hai detto di avere %s anni, quindi forse sei troppo piccolo per %s"
                },
                "PEPPER_CHOOSE_STORY": {
                    "en-US": "Choose a story among those",
                    "it-IT": "Scegli una storia tra queste"
                },
                "PEPPER_CONFIRM_STORY": {
                    "en-US": "So the story is %s?",
                    "it-IT": "Quindi la storia è %s?"
                },
                "PEPPER_STORY_NOT_UNDERSTOOD": {
                    "en-US": "%s is not one of the available stories, maybe i got it wrong, can you repeat please?",
                    "it-IT": "%s non è tra le storie disponibili, forse ho capito male, puoi ripetere per favore?"
                },
                "PEPPER_START_STORY": {
                    "en-US": "Ok, let's begin!",
                    "it-IT": "Ok, iniziamo!"
                },
                "PEPPER_CHOOSE_STORY_ACTION": {
                    "en-US": "How do you want to proceed? Tell me the action number",
                    "it-IT": "Come vuoi precedere? Dimmi il numero dell'azione"
                },
                "PEPPER_CONFIRM_STORY_ACTION": {
                    "en-US": "So the next step is the action number %s?",
                    "it-IT": "Quindi il prossimo passo è l'azione numero %s?"
                },
                "PEPPER_ACTION_INDEX_NOT_UNDERSTOOD": {
                    "en-US": "%s is not one of the possible selectable actions, maybe i got it wrong, can you repeat?",
                    "it-IT": "%s non è una delle azioni che puoi selezionare, forse ho capito male, puoi ripetere?"
                },
                "PEPPER_ACTION_CHOSEN_BY_PEPPER": {
                    "en-US": "I'll select an action for you",
                    "it-IT": "Sceglierò io una azione al tuo posto"
                },
                "PEPPER_STORY_FINISHED": {
                    "en-US": "What an amazing story, so fun and personal! Did you like it?",
                    "it-IT": "Che storia fantastica, cosi divertente e personale! Ti è piaciuta?"
                },
                "PEPPER_STORY_LIKED": {
                    "en-US": "I'm glad to hear it! See you for the next one. Goodbye!",
                    "it-IT": "Sono felice di sentirlo! Alla prossima storia. Ciao!"
                },
                "PEPPER_STORY_NOT_LIKED": {
                    "en-US": "I'm sorry you didn't like it. I hope the next one will be better. Goodbye!",
                    "it-IT": "Mi dispiace non ti sia piaciuta. Spero la prossima sia migliore. Ciao!"
                },
                "PEPPER_STORY_LIKED_NO_HEAR": {
                    "en-US": "I couldn't understand your response. I still hope the story was good. Goodbye!",
                    "it-IT": "Non ho capito la tua risposta. Comunque spero la storia ti sia piaciuta. Ciao!"
                }
            },
            (lang) => {
                this.stt.recognition.lang = lang;
            }
        );

        this.console.log("Chosen min_ms_time:", min_ms_interval, "Chosen camera:", camera_type);

        this.min_ms_interval = min_ms_interval;
        this.unknown_face_threshold = unknown_face_threshold;
        this.CHOSEN_ONE_MAX_THRESHOLD = chosen_one_max_threshold;
        this.camera_type = camera_type;
        this.last_frame_time = Date.now();

        // APIs
        this.pepper = new PepperClient({
            onConnect: async () => {
                try {
                    await this.pepper.stand(true);
                    this.console.log("Pepper connected.");
                }
                catch (error) {
                    this.console.error("Something went wrong on the pepper server");
                }
            }
        });
        this.faceRecognition = new FaceRecognitionClient({
            receiveListener: this.listenerFaceRecognition.bind(this),
            onConnect: this.initFaceRecognition.bind(this)
        });
        this.storyTellingManager = new StoryTellingManager({
            lang: lang,
            onConnect: async () => {
                try {
                    this.console.log("Story telling connected.");
                }
                catch (error) {
                    this.console.error("Something went wrong on the story telling server");
                }
            }
        })
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /* Phase: init states and variables and start one camera service */

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

    parseUser(filename) { // utility function in order to parse e.g. "Marco Lo Pinto#25#male" into an object
        if (filename == undefined) return undefined;
        const parts = filename.split("#");
        const userObject = {
            name: parts[0],
            age: isNaN(parseInt(parts[1])) ? undefined : parseInt(parts[1]),
            sex: parts[2] || undefined
        };
        return userObject;
    }

    formatUser(name, age = undefined, sex = undefined) {
        return `${name}${age != undefined ? "#"+age : ""}${sex != undefined ? "#"+sex : ""}`; // TODO: if age=undefined but sex isn't, the file name will not be correctly parsed by parseUser (TIP: put a default non numerica value, like undefined or null)
    }

    async initFaceRecognition() {
        this.console.log("Face recognition connected.");
        try {
            await this.faceRecognition.initFaceRecognition(this.unknown_face_threshold);
            this.console.log("Starting camera service...");
            await this.startCamera();
        } catch (error) {
            this.console.error("Something went wrong on the face recognition server");
        }
    }

    async startCamera() {
        if (this.state.camera_enabled) {
            console.log('Camera is already enabled!');
            return;
        }
        let isEnabled = false;
        switch (this.camera_type) {
            default:
                this.camera_type = "browser";
            case "browser":
                isEnabled = await this.startCameraBrowser();
                break;
            case "robot":
                isEnabled = await this.startCameraRobot();
                break;
        }
        await this.checkIfVideoIsEnabled(isEnabled);
    }

    async startCameraBrowser() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: false, video: true });
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
            this.console.log("Cameras discovered:", videoDevices);
            if (videoDevices.length > 0) {
                const device = videoDevices[0];
                this.cameraStream = await navigator.mediaDevices.getUserMedia({ video: { deviceId: device.deviceId } });
                video.srcObject = this.cameraStream;
                index_pepper_logo.style = "width: 30vh;";
                return true;
            } else {
                return false;
            }
        } catch (error) {
            return false;
        }
    }

    stopCameraBrowser() {
        if (this.cameraStream) {
            this.console.log("Stopping camera browser");
            this.cameraStream.getTracks().forEach(track => track.stop()); // Stop all tracks in the camera stream
            this.cameraStream = null; // Remove the reference to the camera stream
        }
    }

    async startCameraRobot() {
        try {
            await this.pepper.startVideo(true);
            return true;
        } catch (error) {
            return false;
        }
    }

    async checkIfVideoIsEnabled(isEnabled) {
        if (isEnabled) {
            this.state.camera_enabled = true;
            this.console.log(`Camera ${this.camera_type} enabled!`);
            this.sendFrameCameraRequestDeltaTime();
        }
        else if (!isEnabled && this.camera_enabled_errors < 1) {
            this.console.error(`Camera not enabled using ${this.camera_type}, trying the other one...`);
            this.camera_enabled_errors += 1;
            if (this.camera_type == "browser") {
                this.camera_type = "robot";
                await this.startCameraRobot();
            } else {
                this.camera_type = "browser";
                await this.startCameraBrowser();
            }

        }
        else {
            this.console.error(`Camera not enabled, tried ${this.camera_enabled_errors} times`);
        }
    }

    /* Phase: get frame from camera source and send to face recogntition, then receive the output, finally repeat */

    async sendFrameCameraRequestDeltaTime() {
        // compute delta time
        let deltaTime = Date.now() - this.last_frame_time;
        if (deltaTime < this.min_ms_interval) deltaTime = this.min_ms_interval;
        else deltaTime = 1;
        await this.sleep(deltaTime);
        this.last_frame_time = Date.now();
        // send request
        let isSuccessful = await this.sendFrameCameraRequest();
        this.console.log("Image frame sent.");
        if (!isSuccessful) {
            this.console.error("Image frame not sent, retrying...");
            await this.sendFrameCameraRequestDeltaTime();
        }
    }

    async sendFrameCameraRequest() {
        try {
            if (this.camera_type == "browser") {
                let imgBase64 = this.getFrameCameraBrowser();
                this.faceRecognition.sendFrame(imgBase64, false); // this response will be captured by the listenerFaceRecognition
                return true;
            }
            else if (this.camera_type == "robot") {
                let imgBase64 = await this.pepper.takeFakeVideoFrame(true); // TODO: change into takeVideoFrame!
                this.faceRecognition.sendFrame(imgBase64, false); // this response will be captured by the listenerFaceRecognition
                return true;
            }
        } catch (error) {
            return false;
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

    async listenerFaceRecognition(command) {
        // this.console.log("command:",command);
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
                    await this.pepper.sayMove(
                        this.languageText.get("PEPPER_LOST_CHOSEN_ONE"),
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    this.console.log("Pepper lost the chosen one!");
                }
            }
            else {
                if (known_faces_names.length > 0) {
                    let chosen_one = known_faces_names[0];
                    this.state.chosen_one = known_faces_names[0];
                    if (this.state.new_faces.includes(chosen_one)) this.state.is_chosen_one_new = true;
                    await this.initialTalkToUser(this.state.is_chosen_one_new);
                    // if (this.state.is_chosen_one_new) await this.talkToNewUser();
                    // else await this.talkToExpertUser();
                    this.storyGame();
                }
                else if (Object.keys(command.data["cropped_unknown_faces"]).length > 0) {
                    // No known face, but there is someone that the robot does not know!
                    this.console.log("PHASE UNKNOWN: adding new faces!");
                    this.routing.goToPage("new_face_page");
                    await this.setNewFacesNames(command);
                }
            }

            // Output to label the info for the user!
            let out_text = "";
            if (this.state.chosen_one != undefined) {
                let user = this.parseUser(this.state.chosen_one);
                if (this.state.is_chosen_one_new) out_text = this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', user.name);
                else out_text = this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', user.name);
            }
            else {
                out_text = this.languageText.get("DETECT_NEW_FACES")
            }
            label_pepper_see.innerText = out_text;
        }

        await this.sendFrameCameraRequestDeltaTime();
    }

    /* Phase: new faces detected */

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
                let command_out = await this.faceRecognition.setUnknownFaces(this.state.cropped_unknown_faces, true);
                this.console.log("Success! Setting new faces on the state...");
                this.state.new_faces = this.state.new_faces.concat(command_out.data["new_faces"]);
            } catch (error) {
                this.console.error("Error on setting the new faces:", error);
            } finally {
                this.console.log("Going back to face selection...");
                this.routing.goBack();
                return;
            }

        };
        let [key, value] = objList[idx];
        cropped_unk_face.src = value;

        try {
            // Getting the name
            cropped_unk_face_text.innerText = this.languageText.get("PEPPER_WHAT_IS_FACE_NAME")
            await this.pepper.sayMove(
                this.languageText.get("PEPPER_WHAT_IS_FACE_NAME"),
                PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                true
            );
            let name_text = await this.stt.startListening();

            // Getting the age
            cropped_unk_face_text.innerText = this.languageText.get("PEPPER_WHAT_IS_FACE_AGE")
            await this.pepper.sayMove(
                this.languageText.get("PEPPER_WHAT_IS_FACE_AGE"),
                PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                true
            );
            let age_text = await this.stt.startListening();

            // Getting the sex
            cropped_unk_face_text.innerText = this.languageText.get("PEPPER_WHAT_IS_FACE_SEX")
            await this.pepper.sayMove(
                this.languageText.get("PEPPER_WHAT_IS_FACE_SEX"),
                PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                true
            );
            let sex_text = await this.stt.startListening();
            
            let conf_text = this.languageText.get("PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION")
                .replace('%s', name_text).replace('%s', sex_text).replace('%s', age_text)
            cropped_unk_face_text.innerText = conf_text
            await this.pepper.sayMove(
                conf_text,
                PepperClient.MOVE_NAMES.fancyRightArmCircle,
                true
            );

            let confirm_text = await this.stt.startListening();

            if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION_YES"),
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
                this.state.cropped_unknown_faces[key] = this.formatUser(name_text,age_text,sex_text);
                this.state.new_faces.push(name_text);
                await this.setNewFaceName(command, objList, idx + 1);
            }
            else {
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_WHAT_IS_FACE_ALL_CONFIRMATION_NO"),
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
                await this.setNewFaceName(command, objList, idx);
            }
        } catch (error) {
            this.console.log("An error occurred (propbably no response)");
            this.console.error(error);
            cropped_unk_face_text.innerText = this.languageText.get("PEPPER_NO_HEAR");
            await this.pepper.sayMove(
                this.languageText.get("PEPPER_NO_HEAR"),
                PepperClient.MOVE_NAMES.fancyRightArmCircle,
                true
            );
            await this.sleep(1000);
            await this.setNewFaceName(command, objList, idx);
        }


    }

    /* Phase: introduction of the game to the user */

    // async talkToExpertUser() {
    //     this.routing.goToPage("explanation_page");
    //     // This user has already played check if user wants an explanation!
    //     let user = this.parseUser(this.state.chosen_one);
    //     label_explanation.innerText = this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', user.name);
    //     await this.pepper.sayMove(
    //         this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', user.name),
    //         PepperClient.MOVE_NAMES.fancyRightArmCircle,
    //         true
    //     );
    //     while(true){
    //         try {
    //             let confirm_text = await this.stt.startListening();
    //             if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
    //                 this.console.log("Explain game to expert user: response yes")
    //                 await this.explainGameToUser();
    //                 return true
    //             }
    //             else {
    //                 this.console.log("Explain game to expert user: response no");
    //                 return true;
    //             }
    //         } catch (error) {
    //             this.console.error(error);
    //             label_explanation.innerText = this.languageText.get("PEPPER_NO_HEAR");
    //             await this.pepper.sayMove(
    //                 this.languageText.get("PEPPER_NO_HEAR"),
    //                 PepperClient.MOVE_NAMES.bothArmsBumpInFront,
    //                 true
    //             );
    //             this.sleep(2000);

    //             label_explanation.innerText = this.languageText.get("PEPPER_ASK_EXPLAIN_GAME");
    //             await this.pepper.sayMove(
    //                 this.languageText.get("PEPPER_ASK_EXPLAIN_GAME"),
    //                 PepperClient.MOVE_NAMES.bothArmsBumpInFront,
    //                 true
    //             );
    //         }
    //     }
    // }

    // async talkToNewUser() {
    //     this.routing.goToPage("explanation_page");
    //     // This user is new, explain the game!
    //     let user = this.parseUser(this.state.chosen_one);
    //     label_explanation.innerText = this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', user.name);
    //     await this.pepper.sayMove(
    //         this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', user.name),
    //         PepperClient.MOVE_NAMES.fancyRightArmCircle,
    //         true
    //     );
    //     await this.explainGameToUser();
    //     return true;
    // }

    async initialTalkToUser(newUser){
        this.routing.goToPage("explanation_page");
        // This user has already played check if user wants an explanation!
        let user = this.parseUser(this.state.chosen_one);
        let txt = ""
        if(newUser){
            txt = this.languageText.get("PEPPER_NEW_USER_INTRO").replace('%s', user.name);
        }
        else {
            txt = this.languageText.get("PEPPER_EXPERT_USER_INTRO").replace('%s', user.name);
        }
        label_explanation.innerText = txt
        await this.pepper.sayMove(
            txt,
            PepperClient.MOVE_NAMES.fancyRightArmCircle,
            true
        );
        while(true){
            try {
                let confirm_text = await this.stt.startListening();
                if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                    this.console.log("Explain game to user: response yes")
                    await this.explainGameToUser();
                    return true
                }
                else {
                    this.console.log("Explain game to user: response no");
                    return true;
                }
            } catch (error) {
                this.console.error(error);
                label_explanation.innerText = this.languageText.get("PEPPER_NO_HEAR");
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_NO_HEAR"),
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
                this.sleep(2000);

                label_explanation.innerText = this.languageText.get("PEPPER_ASK_EXPLAIN_GAME");
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_ASK_EXPLAIN_GAME"),
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
            }
        }
    }

    async explainGameToUser() {
        let txt = this.languageText.get("PEPPER_EXPLAIN_GAME");
        label_explanation.innerText = txt;
        await this.pepper.sayMove(
            txt,
            PepperClient.MOVE_NAMES.bothArmsBumpInFront,
            true
        );
    }

    /* Phase: the game! */

    async storyGame() {
        this.storyTellingManager.reset();
        this.clearContainer();
        this.routing.goToPage("prp_page");
        this.console.log("Selecting story!");
        let storyNameChosen = await this.selectStory();
        if (storyNameChosen !== false) {
            this.console.log("Starting story!");
            let jobExecuted = await this.startStory(storyNameChosen);
            if (jobExecuted !== false) {
                this.console.log("Ending story!");
                // Story finished
                let txt = this.languageText.get("PEPPER_STORY_FINISHED");
                prp_title.innerText = txt
                await this.pepper.sayMove(
                    txt,
                    PepperClient.MOVE_NAMES.excited,
                    true
                );

                try {
                    let confirm_text = await this.stt.startListening();
                    if (confirm_text.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                        let txt = this.languageText.get("PEPPER_STORY_LIKED");
                        prp_title.innerText = txt
                        await this.pepper.sayMove(
                            txt,
                            PepperClient.MOVE_NAMES.excited,
                            true
                        );
                    }
                    else if (confirm_text.toLowerCase() == this.languageText.get("NO").toLowerCase()){
                        let txt = this.languageText.get("PEPPER_STORY_NOT_LIKED");
                        prp_title.innerText = txt
                        await this.pepper.sayMove(
                            txt,
                            PepperClient.MOVE_NAMES.excited,
                            true
                        );
                    }
                    else {
                        let txt = this.languageText.get("PEPPER_STORY_LIKED_NO_HEAR");
                        prp_title.innerText = txt
                        await this.pepper.sayMove(
                            txt,
                            PepperClient.MOVE_NAMES.excited,
                            true
                        );
                    }
                } catch (error) {
                    this.console.error(error);
                    let txt =  this.languageText.get("PEPPER_STORY_LIKED_NO_HEAR");
                    label_explanation.innerText = txt;
                    await this.pepper.sayMove(
                        txt,
                        PepperClient.MOVE_NAMES.kisses,
                        true
                    );
                    this.sleep(1000);
                }
            } else {
                this.console.error("Error during story");
            }
        }
        this.routing.goToPage("index_page"); // TODO: to remove?
        // TODO: what to do when story finishes? Invoke new story?
    }

    async selectStory() {
        // Gathering the list of available stories
        let stories = [];
        let storiesOverage = [];
        let storiesLower = [];
        let user = this.parseUser(this.state.chosen_one);
        try {
            stories = await this.storyTellingManager.listStories();
            storiesOverage = await this.storyTellingManager.listStoriesOverage(user.age || 150); // 150 years old to say that there is no age limit
            storiesLower = stories.map((s) => s.toLowerCase());
        } catch (error) {
            this.console.log("Error in gathering stories:", error);
            return false;
        }
        // Displaying them
        for (let i in stories) {
            let storyName = stories[i];
            this.addCardToContainer(storyName);
            if(storiesOverage.includes(storyName)){
                this.setCardAsOverage(i)
            }
        }
        //Saying the overage stories
        if(storiesOverage.length > 0){
            storiesOverageStr = storiesOverage.join(", ")
            let txt = this.languageText.get("PEPPER_STORY_OVER_AGE").replace('%s', user.age).replace('%s', storiesOverageStr);
            prp_title.innerText = txt
            await this.pepper.sayMove(
                txt,
                PepperClient.MOVE_NAMES.thinking,
                true
            );
        }
        // Choose the story loop
        let storyChosen = -1;
        while (storyChosen == -1) {
            try {
                // Pepper asks to user which stories to select and the user responds
                prp_title.innerText = this.languageText.get("PEPPER_CHOOSE_STORY");
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_CHOOSE_STORY"),
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
                let selectedStoryNameLower = (await this.stt.startListening()).toLowerCase();
                // If the story selected is one of the proposed...
                if (storiesLower.includes(selectedStoryNameLower)) {
                    let selectedStoryIndex = storiesLower.indexOf(selectedStoryNameLower);
                    let selectedStoryName = stories[selectedStoryIndex];
                    this.setCardAsSelected(selectedStoryIndex);
                    // Pepper asks if the story selected is the correct one
                    let confirmationQuestion = this.languageText.get("PEPPER_CONFIRM_STORY").replace('%s', selectedStoryName);
                    prp_title.innerText = confirmationQuestion;
                    await this.pepper.sayMove(
                        confirmationQuestion,
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    let confirmationResponse = await this.stt.startListening();
                    // Checking the YES/NO response
                    if (confirmationResponse.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                        this.setCardAsConfirmed(selectedStoryIndex);
                        await this.pepper.sayMove(
                            this.languageText.get("PEPPER_START_STORY"),
                            PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                            true
                        );
                        storyChosen = selectedStoryIndex;
                    }
                    else {
                        this.setCardAsUnselected(selectedStoryIndex);
                    }
                }
                // ...otherwise:
                else {
                    let notUnderstoodQuestion = this.languageText.get("PEPPER_STORY_NOT_UNDERSTOOD").replace('%s', selectedStoryNameLower);
                    prp_title.innerText = notUnderstoodQuestion
                    await this.pepper.sayMove(
                        notUnderstoodQuestion,
                        PepperClient.MOVE_NAMES.confused,
                        true
                    );
                }
            }
            // If the robot does not hear
            catch (error) {
                this.console.log("An error occurred (propbably no response)");
                this.console.error(error);
                prp_title.innerText = this.languageText.get("PEPPER_NO_HEAR");
                await this.pepper.sayMove(
                    this.languageText.get("PEPPER_NO_HEAR"),
                    PepperClient.MOVE_NAMES.fancyRightArmCircle,
                    true
                );
                await this.sleep(1000); // TODO: check if necessary on tablet
            }

        }

        let storyNameChosen = stories[storyChosen];
        return storyNameChosen;
    }

    async startStory(storyNameChosen) {
        // Starting the story
        try {
            await this.storyTellingManager.startStory(storyNameChosen);
        } catch (error) {
            this.console.error("Error in starting the story:", error);
            return false;
        }
        this.console.log("Starting story loop...");
        // Story Loop
        while (!this.storyTellingManager.storyFinished) {
            this.clearContainer();
            let { newPrompts, newMoods, nextActions } = await this.storyTellingManager.getNewPromptsAndActions()
                .catch(() => {
                    this.console.log("Error in gathering new prompts:", error);
                    return false;
                });
            for (let i = 0; i < newPrompts.length; i++) {
                let prompt = newPrompts[i];
                let mood = newMoods[i];

                prp_title.innerText = prompt;
                await this.pepper.sayMove(
                    prompt,
                    mood,
                    true
                );
                await this.sleep(prompt.length * 50);
            }
            // If the story is finished, exit!
            if (this.storyTellingManager.storyFinished) break;
            // Show the new actions to the user:
            for (let i = 0; i < nextActions.length; i++) {
                let actionPretext = nextActions[i];
                this.addCardToContainer(`${i + 1}: ${actionPretext}`);
            }

            // Choose action loop:
            let actionChosen = -1;
            let maxRepeatCount = 3;
            let repeatCount = 0;
            while (actionChosen == -1) {
                try {
                    // Pepper asks to user which action to select and the user responds
                    let txt = this.languageText.get("PEPPER_CHOOSE_STORY_ACTION");
                    prp_title.innerText = txt;
                    await this.pepper.sayMove(
                        txt,
                        PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                        true
                    );
                    let selectedActionIndexStr = (await this.stt.startListening()).toLowerCase();
                    let selectedActionIndex = Number(selectedActionIndexStr) - 1;
                    // If the action selected is one of the proposed...
                    if (selectedActionIndex <= nextActions.length) {
                        this.setCardAsSelected(selectedActionIndex);
                        // Pepper asks if the action selected is the correct one
                        let confirmationQuestion = this.languageText.get("PEPPER_CONFIRM_STORY_ACTION").replace('%s', selectedActionIndexStr);
                        prp_title.innerText = confirmationQuestion;
                        await this.pepper.sayMove(
                            confirmationQuestion,
                            PepperClient.MOVE_NAMES.fancyRightArmCircle,
                            true
                        );
                        let confirmationResponse = await this.stt.startListening();
                        // Checking the YES/NO response
                        if (confirmationResponse.toLowerCase() == this.languageText.get("YES").toLowerCase()) {
                            actionChosen = selectedActionIndex;
                        }
                        else {
                            this.setCardAsUnselected(selectedActionIndex);
                        }
                    }
                    // ...otherwise:
                    else {
                        let notUnderstoodQuestion = this.languageText.get("PEPPER_ACTION_INDEX_NOT_UNDERSTOOD").replace('%s', selectedActionIndexStr)
                        prp_title.innerText = notUnderstoodQuestion
                        await this.pepper.sayMove(
                            notUnderstoodQuestion,
                            PepperClient.MOVE_NAMES.confused,
                            true
                        );
                    }
                }
                // If the robot does not hear
                catch (error) {
                    this.console.log("An error occurred (propbably no response)");
                    this.console.error(error);
                    prp_title.innerText = this.languageText.get("PEPPER_NO_HEAR");
                    await this.pepper.sayMove(
                        this.languageText.get("PEPPER_NO_HEAR"),
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    
                    // Counting how many times the user didn't respond
                    repeatCount++
                    if(repeatCount > maxRepeatCount){
                        actionChosen = 0

                        prp_title.innerText = this.languageText.get("PEPPER_ACTION_CHOSEN_BY_PEPPER");
                        await this.pepper.sayMove(
                            this.languageText.get("PEPPER_ACTION_CHOSEN_BY_PEPPER"),
                            PepperClient.MOVE_NAMES.fancyRightArmCircle,
                            true
                        );
                    }
                    else{
                        await this.sleep(1000); // TODO: check if necessary on tablet
                    }
                }

            }
            // Action selected, go on...
            this.setCardAsConfirmed(actionChosen);
            await this.storyTellingManager.executeAction(actionChosen);
        }

        return true;
    }

    // Story card functions
    addCardToContainer(content) {
        let card = document.createElement("labels")
        card.classList.add("card")
        card.innerText = content
        story_card_container.appendChild(card)
    }
    clearContainer() {
        story_card_container.innerHTML = ""
    }
    setCardAsUnselected(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
    }
    setCardAsSelected(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
        cards[index].classList.add("card-chosen");
    }
    setCardAsConfirmed(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
        cards[index].classList.add("card-chosen-confirmation");
    }
    setCardAsOverage(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.add("card-overage");
    }

}

(() => {
    let app = new App({});
})();