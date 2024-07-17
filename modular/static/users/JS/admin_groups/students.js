import { get_group, get_not_enrolled_students, add_student_group, get_enrolled_students, remove_student_from_group, search_enrolled_students, search_not_enrolled_students } from "./request.js";
import { set_group_students_container, print_students, show_available_students, remove_student_from_list_for_enroll, print_students_for_enroll } from "./utils.js";
import { show_alert } from "../utils.js";

//Listener to detect when is clicked the button add student, get not enrolled students and print it 
export function button_add_students_pressed(){
    $(document).on('click', '#button-add-student', function(){
        let group_id = $('#button-add-student').attr('group');
        get_not_enrolled_students(group_id).then(data=>{
            if(data['error']==false){
                show_available_students(data['students'], group_id);
            }else{
                show_alert(true, data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    });
}

//Get enrolled students in a group and print it
export function show_students(group){    
    get_group(group).then(data=>{
        let group_details = data['group']
        get_enrolled_students(group).then(data=>{
            let students = data['students'];
            set_group_students_container(group_details);
            print_students(students, group_details);
        }).catch(error=>{
            console.log(error);
        })
    }).catch(error=>{
        console.log(error);
    })
    
}

//Make request to remove x student from y group
export function remove_student(student_id, group_id){
    remove_student_from_group(group_id, student_id).then(data=>{
        if(data['error'] == false){
            show_alert(false, data['message']);
            show_students(group_id);
        }else{
            show_alert(true, data['message']);
        }
    }).catch(error=>{
        console.log(error);
    });
}

//Make request to add x student to y group
export function add_student(student_id, group_id){
    add_student_group(student_id, group_id).then(data=>{
        if(data['error'] == false){
            show_alert(false, data['message']);
            setTimeout(function(){
                remove_student_from_list_for_enroll(student_id);
            }, 1000)
        }else{
            show_alert(true, data['message']);
            console.log(data['exception']);
        }
    }).catch(error=>{
        console.log(error);
    })
}

//Remove dialog with available sutdents to remove
export function remove_floating_students_list(group){
    let dialog = $('#floating-dialog-students');
    dialog.removeClass('show-alert').addClass('remove');
    setTimeout(function(){
        dialog.remove();
    }, 1000);

    show_students(group);
}

//Listener to detect when the search student enrolled input have changed and able or disabled search button
export function handle_search_enrolled_students_input(){
    $(document).on('input', '#search-enrolled-students', function(){
        let word = $('#search-enrolled-students').val();
        if(word.length == 0){
            let group = $('#search-enrolled-students-button').val();
            $('#search-enrolled-students-button').prop('disabled',true).addClass('button-disabled');
            show_students(group);
        }else{
            $('#search-enrolled-students-button').removeAttr('disabled').removeClass('button-disabled');
        }
    });
}

//Listener to detect when the button search enrolled students is pressed and make search request.
export function button_search_enrolled_students_pressed(){
    $(document).on("click", "#search-enrolled-students-button", function(){
        let group = $('#search-enrolled-students-button').val();
        $('#search-enrolled-students').prop('disabled', true);
        let word = $('#search-enrolled-students').val();
        search_enrolled_students(group, word).then(data => {
            if(data['error'] == false){
                let students = data['students'];
                print_students(students,group);
                $('#search-enrolled-students').removeAttr('disabled');
            }else{
                show_alert(true, data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    });
}

//Listener to detect when the search student not enrolled input have changed and able or disabled search button
export function handle_search_students_for_enroll_input(){
    $(document).on('input', '#search-students-for-enroll', function(){
        let word = $('#search-students-for-enroll').val();
        if(word.length == 0){
            let group = $('#search-students-for-enroll-button').val();
            $('#search-students-for-enroll-button').prop('disabled',true).addClass('button-disabled');
            get_not_enrolled_students(group).then(data=>{
                if(data['error'] == false){
                    print_students_for_enroll(data['students'], group, false);
                }else{
                    show_alert(true, data['message']);
                }
            }).catch(error=>{
                console.log(error);
            });
        }else{
            $('#search-students-for-enroll-button').removeAttr('disabled').removeClass('button-disabled');
        }
    });
}

//Listener to detect when the button search not enrolled students is pressed and make search request.
export function button_search_students_for_enroll_pressed(){
    $(document).on("click", "#search-students-for-enroll-button", function(){
        let group = $('#search-students-for-enroll-button').val();
        let word = $('#search-students-for-enroll').val();
        $('#search-students-for-enroll').prop('disabled', true);
        search_not_enrolled_students(group, word).then(data => {
            if(data['error'] == false){
                console.log(data['students']);
                print_students_for_enroll(data['students'],group, false);
                $('#search-students-for-enroll').removeAttr('disabled');
            }else{
                show_alert(true, data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    });
}