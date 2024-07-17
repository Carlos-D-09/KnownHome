import { button_register_pressed } from "./register.js";


$(document).ready(function(){
    //functions and methods
    select_registrar_usuarios_nav_bar()

    //Listeners
    button_register_pressed();
});

//Change the class for the option-1 (usuarios) in the navbar to add the selected effect
function select_registrar_usuarios_nav_bar(){
    let current_selected = $('#option-5');
    current_selected.addClass('selected');
}