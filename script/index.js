const fetch_change = () => {



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


