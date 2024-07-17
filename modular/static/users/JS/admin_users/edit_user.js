import { validate_email_format, validate_password_format, show_alert } from "../utils.js";
import { edit_user_request, get_user } from "./requests.js";
import { display_floating_edit_form } from "./utils.js"

//Display edit form for admin user
export function show_edit_form(user_id){
    get_user(user_id).then(data=>{
        if(data['error'] == false){
            display_floating_edit_form(data['user']);
        }else{
            console.log(data['message']);
        }
    }).catch(error=>{
        console.log(error);
    })
}

//Validate inputs and make request to edit admin user
export function edit_user(user_id){
    let username = $('#username').val();
    let email = $('#email').val();
    let password = $('#password').val();

    if (validate_inputs(username, email, password) == true){
        edit_user_request(user_id, username, email, password).then(data=>{
            if(data['error'] == true){
                show_alert(true,data['message']);
                console.log(data['exception']);
            }else{
                show_alert(false,data['message']);
            }
        }).catch(error => {
            console.log(error);
        })
    }
}

//Return false if username or email or password aren't valid. Return true if the three are valid
function validate_inputs(username, email, password){
    if (username == ''){
        show_alert(true, 'El nombre de usuario no puede estar vacío');
        return false;
    }

    if(email == ''){
        show_alert(true, 'El correo electŕonico no puede estar vacío');
        return false;
    }else{
        let format_result = validate_email_format(email);
        if(format_result.error == true){
            show_alert(true, format_result.message);
            return false;
        }
    }

    if (password != ''){
        let format_result = validate_password_format(password);
        if(format_result.error == true){
            show_alert(true, format_result.message);
        }
    }

    return true
}