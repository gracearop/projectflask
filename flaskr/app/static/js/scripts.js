document.addEventListener('DOMContentLoaded', () => {
    const recordBtn = document.getElementById('recordBtn');
    const audioPlayback = document.getElementById('audioPlayback');

    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    recordBtn.addEventListener('click', async () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });

    async function startRecording() {
        try {
            recordBtn.innerHTML = '<span class="material-symbols-outlined">stop</span>';
            isRecording = true;

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                await uploadAudio(audioBlob);
                
                audioChunks = [];
                isRecording = false;
                recordBtn.innerHTML = '<span class="material-symbols-outlined">mic</span>';
            };

            mediaRecorder.start();
        } catch (error) {
            console.error('Error accessing media devices:', error.message);
            alert('Error accessing media devices: ' + error.message);
            isRecording = false;
            recordBtn.innerHTML = '<span class="material-symbols-outlined">mic</span>';
        }
    }

    function stopRecording() {
        mediaRecorder.stop();
    }

    async function uploadAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.mp3');

        try {
            const response = await fetch('/upload_audio', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                console.log('File uploaded successfully:', data.message);
                console.log('Predicted Intent:', data.predicted_intent);
            } else {
                console.error('Error uploading file:', data.error);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }
    
    // Other code remains the same...
});



// document.addEventListener('DOMContentLoaded', () => {
//     const recordBtn = document.getElementById('recordBtn');
//     const audioPlayback = document.getElementById('audioPlayback');
    
//     let mediaRecorder;
//     let audioChunks = [];
//     let isRecording = false;

//     recordBtn.addEventListener('click', async () => {
//         if (!isRecording) {
//             // Start recording
//             recordBtn.innerHTML = '<span class="material-symbols-outlined">stop</span>';
//             isRecording = true;

//             try {
//                 const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//                 mediaRecorder = new MediaRecorder(stream);

//                 mediaRecorder.ondataavailable = (event) => {
//                     audioChunks.push(event.data);
//                 };

//                 mediaRecorder.onstop = async () => {
//                     const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
//                     const audioUrl = URL.createObjectURL(audioBlob);
//                     audioPlayback.src = audioUrl;

//                     // Automatically upload the audio
//                     const formData = new FormData();
//                     formData.append('audio', audioBlob, 'recording.mp3');

//                     try {
//                         const response = await fetch('/upload_audio', {
//                             method: 'POST',
//                             body: formData
//                         });

//                         const data = await response.json();
//                         if (response.ok) {
//                             console.log('File uploaded successfully:', data.filepath);
//                         } else {
//                             console.error('Error uploading file:', data.error);
//                         }
//                     } catch (error) {
//                         console.error('Error uploading file:', error);
//                     }

//                     audioChunks = [];
//                     isRecording = false;
//                     recordBtn.innerHTML = '<span class="material-symbols-outlined">mic</span>';
//                 };

//                 mediaRecorder.start();
//             } catch (error) {
//                 console.error('Error accessing media devices:', error.message);
//                 alert('Error accessing media devices: ' + error.message);
//                 isRecording = false;
//                 recordBtn.innerHTML = '<span class="material-symbols-outlined">mic</span>';
//             }
//         } else {
//             // Stop recording
//             mediaRecorder.stop();
//         }
//     });

//     navigator.permissions.query({ name: 'microphone' }).then((permissionStatus) => {
//         if (permissionStatus.state !== 'granted') {
//             alert('Microphone access is not granted.');
//         }
//     });

//     navigator.mediaDevices.enumerateDevices().then(devices => {
//         devices.forEach(device => {
//             console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
//         });
//     }).catch(err => {
//         console.error('Error enumerating devices:', err);
//     });

//     navigator.mediaDevices.enumerateDevices().then(devices => {
//         let hasAudioInput = devices.some(device => device.kind === 'audioinput');
//         if (hasAudioInput) {
//             return navigator.mediaDevices.getUserMedia({ audio: true });
//         } else {
//             throw new Error('No audio input devices found');
//         }
//     }).then(stream => {
//         console.log('Microphone accessed successfully');
//     }).catch(err => {
//         console.error('Error accessing media devices:', err);
//     });
// });
