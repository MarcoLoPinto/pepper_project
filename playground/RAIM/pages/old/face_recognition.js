const cameraList = document.getElementById('camera-list');
const connectButton = document.getElementById('connect-button');
const video = document.getElementById('video');
const debugOutput = document.getElementById('debug');

// Get a list of available video devices
navigator.mediaDevices.getUserMedia({audio: true, video: true})
    .then(()=> {
        navigator.mediaDevices.enumerateDevices()
            .then(devices => {
                console.log(devices)
                // Filter the list to include only video devices
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                // Populate the drop-down menu with the names of the video devices
                videoDevices.forEach(device => {
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label || `Camera ${cameraList.options.length + 1}`;
                    cameraList.add(option);
                });
            })
            .catch(error => {
                console.error('Error enumerating devices:', error);
            })
    })


// Add a click event listener to the "Connect" button
connectButton.addEventListener('click', () => {
    // Get the ID of the selected camera
    const selectedCameraId = cameraList.value;
    console.log(cameraList)
    if (!selectedCameraId) {
        console.error('No camera selected');
        return;
    }
    // Request access to the selected camera
    navigator.mediaDevices.getUserMedia({ video: { deviceId: selectedCameraId } })
        .then(stream => {
            // Display the video stream in the <video> element
            video.srcObject = stream;
            sendFrame()

        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
});

function sendFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    // Send using websocket
    let command = new RAIMClient.Command({
        data:{
            img: imageData,
            id: "face_recognition_detect",
        },
        to_client_id: "face_recognition"
    })
    RAIMClient.dispatchCommand(command)
}

const MIN_MILLISECONDS_INTERVAL = 500;
let lastFrameTime = Date.now();
function frameReceivedResponse(command) {
    let deltaTime = Date.now() - lastFrameTime;
    if(deltaTime < MIN_MILLISECONDS_INTERVAL) deltaTime = MIN_MILLISECONDS_INTERVAL;
    else deltaTime = 1;
    if(command.from_client_id !== "face_recognition") return;
    if(["known_faces", "cropped_unknown_faces"].every(key => command.data.hasOwnProperty(key))){
        console.log(
            "known:",
            command.data["known_faces"], 
            "unknown number:",
            Object.keys(command.data["cropped_unknown_faces"]).length
        )
        debugOutput.innerText = "known faces: " + Object.keys(command.data["known_faces"]).join(', ') + " | unknown n°: " + Object.keys(command.data["cropped_unknown_faces"]).length
    }
    else {
        console.log("???", command.data)
        debugOutput.innerText = "Other..."
    }
    
    setTimeout(()=>{
        lastFrameTime = Date.now();
        sendFrame();
    }, deltaTime);
}

RAIMClient.setCommandListener(frameReceivedResponse)