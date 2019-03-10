const add_cards = () =>{
    const cat = "Food";
    const amount = -200;
    let text = `
    <div class="card suggestion-cards bg-light" style="width: 18rem;">
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
    }
)


