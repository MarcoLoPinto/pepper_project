const cameraList = document.getElementById('camera-list');
const connectButton = document.getElementById('connect-button');
const video = document.getElementById('video');

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
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
});