const userId = document.getElementById('user');
const checkbox = document.getElementById('checkbox');
const submitButton = document.getElementById('submit');
const uuid = uuidV4();
const state = {
    keydown: 'KEY_DOWN',
    keyup: 'KEY_UP'
}

let password = document.getElementById('password');
let measurements = [];

password.addEventListener('keydown', keyDownTextField);
password.addEventListener('keyup', keyUpTextField);
submitButton.addEventListener('click', validateAndSendRequest);
document.cookie = 'sessionId=' + uuid;

function keyDownTextField(e) {
    measurements.push({keycode: e.keyCode, timestamp: Date.now(), state: state.keydown})
}

function keyUpTextField(e) {
    measurements.push({keycode: e.keyCode, timestamp: Date.now(), state: state.keyup})
}

function validateAndSendRequest() {
    if (password.value !== '.tie5Roanl.') {
        alert('Password is not valid.');
        clearPasswordData();
        return;
    }

    const response = sendRequest();

    response.then(response => response.json())
        .then(() => {
            if (!checkbox.checked) {
                document.location.replace('/result')
            } else {
                alert('Training measurement send!')
                clearPasswordData();
            }
        });
}

function sendRequest() {
    return fetch('/measurement', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({userId: userId.value, isTraining: checkbox.checked, measurements: measurements}),
        method: 'POST'
    });
}


function clearPasswordData() {
    measurements = [];
    password.value = '';
}

// TODO change it
function uuidV4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}