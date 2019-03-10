const add_cards = (cat, amount) =>{
    let text = `
    <div class="card suggestion-cards bg-light" style="width: 15rem;">
        <div class="card-body">
            <h5 class="card-title">${cat}</h5>
            <p class="card-text">${amount}</p>
        </div>
    </div>
    `
    $("#suggestion-colon").append(text);

}




$(document).ready(
    () => {
        $("#saving-due-date").datepicker({
            showOtherMonths: true,
            selectOtherMonths: true
        });

        
        draw_graph("http://localhost:5000");
        
        $("#calc-button").click(
            () => {
                let saving_amount = $("#saving-amount").val();
                let saving_due_date = $("#saving-due-date").val();
                fetch(`http://localhost:5000/saving?amount=${saving_amount}&date=${saving_due_date}`).then(
                    res => {
                        return res.json()
                    }
                )
                .then(
                    data => {
                        for (let index = 0; index < data.length; index++) {
                            const cat = data[index];
                            for (const key in cat["children"]) {
                                let element = cat["children"][key];
                                let amount = element["size"];
                                if(amount > 0){
                                    let name = element["name"];
                                    add_cards(name, amount);
                                }
                            }
                        }
                    }
                )
            }
        )
    
    }
)


