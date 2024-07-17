import { previous_images, next_images } from "./select_images.js";

$(document).ready(function(){
    select_imagenes_nav_bar();
    
    //Listeners
    previous_images();
    next_images();
})

function select_imagenes_nav_bar(){
    let current_selected = $('#option-2');
    current_selected.addClass('selected');
}