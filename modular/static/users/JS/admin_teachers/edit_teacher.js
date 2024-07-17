import { validate_password_format, show_alert } from "../utils.js";
import { edit_teacher_request, get_teacher } from "./requests.js";
import { display_floating_edit_form } from "./utils.js"

//Get x teacher info and show edit form
export function show_edit_form(user_id){
    get_teacher(user_id).then(data=>{
        if(data['error'] == false){
            display_floating_edit_form(data['teacher']);
        }else{
            console.log(data['message']);
        }
    }).catch(error=>{
        console.log(error);
    })
}

//Make edit request
export function edit_teacher(teacher_id){
    let username = $('#username').val();
    let password = $('#password').val();

    if (validate_inputs(username, password) == true){
        edit_teacher_request(teacher_id, username, password).then(data=>{
            if(data['error'] == true){
                show_alert(true,data['message']);
                console.log(data['exception'])
            }else{
                show_alert(false,data['message']);
            }
        }).catch(error => {
            console.log(error);
        })
    }
}

//Validate username and password 
function validate_inputs(username, password){
    if (username == ''){
        show_alert(true, 'El nombre de usuario no puede estar vacío');
        return false;
    }

    if (password != ''){
        let format_result = validate_password_format(password);
        if(format_result.error == true){
            show_alert(true, format_result.message);
            return false;
        }
    }
    return true
}