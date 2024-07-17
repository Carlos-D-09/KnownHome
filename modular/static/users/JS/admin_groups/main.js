import { show_students, remove_student, button_add_students_pressed, add_student, remove_floating_students_list, handle_search_enrolled_students_input, button_search_enrolled_students_pressed, handle_search_students_for_enroll_input, button_search_students_for_enroll_pressed } from "./students.js";
import { modify_group, show_edit_form, show_groups, remove_group, button_search_group_pressed, handle_search_input } from "./group.js";
import { remove_delete_alert, remove_edit_form, show_alert_delete } from "./utils.js";

//Functions in the global scope
window.show_students = show_students;
window.show_groups = show_groups;
window.remove_student = remove_student;
window.remove_floating_students_list = remove_floating_students_list;
window.add_student = add_student;
window.show_edit_form = show_edit_form;
window.remove_edit_form = remove_edit_form;
window.modify_group = modify_group;
window.show_alert_delete = show_alert_delete;
window.remove_delete_alert = remove_delete_alert;
window.remove_group = remove_group;

$(document).ready(function(){
    select_grupos_nav_bar();

    //Add students
    button_add_students_pressed();
    
    //Search groups
    handle_search_input();
    button_search_group_pressed();

    //Search enrolled students
    handle_search_enrolled_students_input();
    button_search_enrolled_students_pressed();

    //Search studetns for enroll
    handle_search_students_for_enroll_input();
    button_search_students_for_enroll_pressed();
})

function select_grupos_nav_bar(){

    let current_selected = $('#option-4');
    current_selected.addClass('selected');
}