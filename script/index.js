const fetch_change = () => {
    


}




$(document).ready(
    () => {
        $("#saving-due-date").datepicker({
            showOtherMonths: true,
            selectOtherMonths: true
        });

        // fetch_index();
        draw_graph("http://localhost:5000");
    }
)


