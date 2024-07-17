import { validate_password_format, validate_username_format, show_alert } from "../../../users/JS/utils.js";
import { register_master } from "./requests.js";

export function button_register_pressed(){
    $(document).on('click', '#button_register', function(){
        let username = $('#username').val();
        let password = $('#password').val();
        if(validate_inputs(username, password) == true){
            register_master(username, password).then(data=>{
                if(data['error'] == true){
                    show_alert(true, data['message']);
                }else{
                    show_alert(false, data['message']);
                    $('#username').val('');
                    $('#password').val('');
                }
            }).catch(error=>{
                console.log(error);
            })
        }
    });
}

function validate_inputs(username, password){
    let valid_username = validate_username_format(username);
    let valid_password = validate_password_format(password);

    if(valid_username.error == true){
        show_alert(true, valid_username.message);
        return false;
    }
    if (valid_password.error == true){
        show_alert(true,valid_password.message);
        return false;
    }
    return true;
}