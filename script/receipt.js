var loadFile = function(event) {
    this.parseImg(event.target.files);

    var input = document.getElementById('input');
    input.hidden = true;
    
    var remove = document.getElementById('remove');
    remove.hidden = false;

    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
};

var remove = function(event) {
    var input = document.getElementById('input');
    input.value='';
    input.hidden = false;

    var remove = document.getElementById('remove');
    remove.hidden = true;

    var output = document.getElementById('output');
    output.removeAttribute('src');
}

var parseImg = async function(files){
    fetch("http://localhost:5000/parseImg", {method: 'POST', body: JSON.stringify(files[0])}).then(res => {
        console.log(res);
    })
}
