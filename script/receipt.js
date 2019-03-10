var loadFile = function (event) {
    console.log(event.target.files);
    this.parseImg(event.target.files);

    var input = document.getElementById('file_input');
    input.hidden = true;

    var remove = document.getElementById('remove');
    remove.hidden = false;

    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
};

var remove = function (event) {
    var input = document.getElementById('file_input');
    input.value = '';
    input.hidden = false;

    var remove = document.getElementById('remove');
    remove.hidden = true;

    var output = document.getElementById('output');
    output.removeAttribute('src');

    document.getElementById('add-receit-button').hidden = true;
    this.jsonres = "";
}

var jsonres = "";
var parseImg = async function (files) {
    fetch("http://localhost:5000/parseImg",
        {
            method: "POST",
            body: files[0]
        }).then(res => {
            return res.json();
        }).then(data => {
            if (data.success) {
                this.jsonres = JSON.stringify(data.data);
                // var colon = document.getElementById('item-colon');
                for (var key in data.data) {
                    console.log(data.data);
                    if (data.data[key]["item"].includes("PLOMMER")) {

                        let item_name = "Plommer 0.100kg x kr 49,00";
                        var text = `
                            <div class="card suggestion-cards bg-light" style="width: 18rem;">
                                <div class="card-body">
                                    <h5 class="card-title">${item_name}</h5>
                                    <p class="card-text">Nok ${data.data[key]['size']}</p>
                                </div>
                            </div>
                            `
                    } else {
                        var text = `
                            <div class="card suggestion-cards bg-light" style="width: 18rem;">
                                <div class="card-body">
                                    <h5 class="card-title">${data.data[key]['item']}</h5>
                                    <p class="card-text">Nok ${data.data[key]['size']}</p>
                                </div>
                            </div>
                            `
                    }
                    $("#item-card-container").append(text);
                    document.getElementById('add-receit-button').hidden = false;
                }
            }
        });
}

var returnJson = function () {
    if (this.jsonres !== "") {
        fetch("http://localhost:5000/saveJson",
            {
                method: "POST",
                body: this.jsonres
            }).then(res => {
                return res.json();
            }).then(res => {
                console.log(res);
                if (res.success) {
                    window.location.href = 'index.html';
                }
            });
    }
}

const goToIndex = () => {
    window.location.href = "index.html";
}
