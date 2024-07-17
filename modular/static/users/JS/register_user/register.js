import { show_alert, validate_email_format, validate_password_format, validate_username_format } from "../utils.js";
import { register_user } from "./requests.js";

//Listener to detect when the register button is pressed
export function button_register_pressed(){
    $(document).on('click', '#button_register', function(){
        let username = $('#username').val();
        let email = $('#email').val();
        let password = $('#password').val();
        let rol = $('#user_type option:selected').val();

        if(validate_inputs(username, email, password) == true){
            register_user(username, email, password, rol).then(data=>{
                if(data['error'] == true){
                    show_alert(true, data['message']);
                }else{
                    show_alert(false, data['message']);
                    $('#username').val(''); 
                    $('#password').val('');
                    $('#email').val('');
                }
            }).catch(error=>{
                console.log(error);
            })
        }
    });
}

//Return false if username or email or password are not valid. Return true if the three are valids
function validate_inputs(username, email, password){
    let valid_username = validate_username_format(username);
    let valid_email = validate_email_format(email);
    let valid_password = validate_password_format(password);

    if(valid_username.error == true){
        show_alert(true, valid_username.message);
        return false;
    }
    if(valid_email.error == true){
        show_alert(true, valid_email.message);   
        return false;
    }
    if (valid_password.error == true){
        show_alert(true,valid_password.message);
        return false;
    }

    return true;
}