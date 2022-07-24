const userName = document.getElementById('user_name');
const submitButton = document.getElementById('submit_button');
const authenticateButton = document.getElementById('authenticate_button');
const state = {
    keydown: 'KEY_DOWN',
    keyup: 'KEY_UP'
}

let password = document.getElementById('password');
let keyEvents = [];

password.addEventListener('keydown', keyDownTextField);
password.addEventListener('keyup', keyUpTextField);
submitButton.addEventListener('click', validateAndSendTrainingRequest);
authenticateButton.addEventListener('click', validateAndSendRequest);
document.cookie = 'sessionId=' + uuidV4();

function keyDownTextField(e) {
    keyEvents.push({keyCode: e.key, timestamp: Date.now(), state: state.keydown})
    if(e.key === 'Enter'){
        submitButton.click()
    }
}

function keyUpTextField(e) {
    keyEvents.push({keyCode: e.key, timestamp: Date.now(), state: state.keyup})
}

function validateAndSendTrainingRequest(){
    if (!isPasswordValid(password.value) || !isMeasurementValid()) {
        return;
    }

    sendRequest(true).then(() => {
        clearPasswordData();
        alert('Training measurement send!')
    });
}

function validateAndSendRequest() {
    if (!isPasswordValid(password.value) || !isMeasurementValid()) {
        return;
    }

    sendRequest(false)
        .then(response => response.json())
        .then(response => document.location.replace('/analyze/' + response.id));
}

function sendRequest(isTraining) {
    return fetch('/measurements', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({userName: userName.value, isTraining: isTraining, keyEvents: keyEvents}),
        method: 'POST'
    });
}

function isPasswordValid(passwordValue){
    if(passwordValue !== '.tie5Roanl'){
        alert('Password is not valid!');
        clearPasswordData();
        return false;
    }
    return true;
}

function isMeasurementValid(){
    if(keyEvents.length < 22){
        alert('Measurement scheme is not valid!');
        clearPasswordData();
        return false;
    }
    return true;
}

function clearPasswordData() {
    keyEvents = [];
    password.value = '';
}

function uuidV4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}
