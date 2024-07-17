import { handle_search_input, button_search_pressed } from "./search.js";
import { edit_teacher, show_edit_form } from "./edit_teacher.js";
import { remove_floating_edit_form,show_alert_delete, remove_delete_alert } from "./utils.js";
import { delete_teacher } from "./delete_teacher.js";

//Functions in the global scope
window.show_edit_form = show_edit_form;
window.remove_floating_edit_form = remove_floating_edit_form;
window.edit_teacher = edit_teacher;
window.show_alert_delete = show_alert_delete;
window.remove_delete_alert = remove_delete_alert;
window.delete_teacher = delete_teacher;


$(document).ready(function(){ 
    //functions and methods
    select_maestros_nav_bar();

    //Listeners
    handle_search_input();
    button_search_pressed();
});

//Change the class for the option-1 (usuarios) in the navbar to add the selected effect
function select_maestros_nav_bar(){
    let current_selected = $('#option-3');
    current_selected.addClass('selected');
}