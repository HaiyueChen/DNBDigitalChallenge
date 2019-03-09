var loadFile = function(event) {
    console.log(event.target.files);
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

    document.getElementById('tablegroup').hidden = true;
    this.jsonres = "";
}

var jsonres = "";
var parseImg = async function(files){
    fetch("http://localhost:5000/parseImg", 
        {
            method: "POST", 
            body: files[0]
        }).then(res => {
            return res.json();
        }).then(data => {
            if(data.success){
                this.jsonres = JSON.stringify(data.data);
                var table = document.getElementById('table');
                var text = '<tr> <th>Item</th> <th>Price</th> </tr>'

                for (var key in data.data) {
                    if (data.data.hasOwnProperty(key)) {
                        text += '<tr>';
                        text += '<td>' + data.data[key]['item'] + '</td>';
                        text += '<td align=\"right\">' + data.data[key]['price'] + ' kr</td>';
                        text += '</tr>';
                    }
                }
                table.innerHTML = text;
                document.getElementById('tablegroup').hidden = false;
            }
        });
}

var returnJson = function(){
    if(this.jsonres !== ""){
        fetch("http://localhost:5000/saveJson", 
        {
            method: "POST", 
            body: this.jsonres
        }).then(res => {
            return res.json();
        }).then(res => {
            if(res.success){
                window.location.href = 'index.html';
            }
        });
    }
}
