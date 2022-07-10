userId = document.getElementById('user');
passwordTextArea = document.getElementById('password');
passwordTextArea.addEventListener('keydown', keyDownTextField);
passwordTextArea.addEventListener('keyup', keyUpTextField);

submitButton = document.getElementById('submit');
submitButton.addEventListener('click', sendRequest);


function keyDownTextField(e) {
  console.log(e.keyCode + ' down at: ' + Date.now());
}

function keyUpTextField(e) {
  console.log(e.keyCode + ' up at: ' + Date.now());
}

function sendRequest(e){
  let request = new XMLHttpRequest();

  request.open('POST', '/add');
  request.send();
  console.log(userId + passwordTextArea.value);
}