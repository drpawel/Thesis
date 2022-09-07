const progressBar = document.getElementById('progress_bar');
const title = document.getElementById('title');

window.onload = function() {
  getResult()
      .then(response => response.json())
      .then(response => {
          printData(response);
  });
};

async function getResult(){
    return fetch('/results/' + measurementId, {
            headers: {
                'Accept': 'application/json',
            },
            method: 'GET'
        });
}

function printData(response){
    if(!response.isSuccess){
        title.innerText = "Matching has failed!";
        progressBar.value = 0;
    }else{
        title.innerText = response.probability + "%";
        progressBar.value = response.probability;
    }
}
