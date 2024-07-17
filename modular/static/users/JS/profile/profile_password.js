import { validate_password_format, position_floating_dialog } from "../utils.js";
import { edit_password } from "./requests.js";
import { bloquear_username, bloquear_correo, desbloquear_username, desbloquear_correo} from "./utils.js";

//Module asociated to all the password edit operations

//Start DOM manipulation

    // passwrod_select(): Listener to detect when the user wants to edit the password
    // display_floating_password_form(): Method to build and show a floating dialog to edit the password
    // positiong_floating_dialog(): Method to determine in what position display the floating dialog
    // remove_floating_password_dialog(): Method called when the user cancel the password edit operation
    // show_alert_password(danger, text, logout): Show in screent the content in the variable text. The parameter danger expects a boolean value. If it is true, the method set the text class as text-danger, in other case, 
    //                                            set the text class ass text-succss. The parameter logout determine if is neccesary redirect to loguot

    export function password_select(){
        $(document).on('click', '#password-icon', function(){
            display_floating_password_form();
            bloquear_username();
            bloquear_correo();
        })
    }

    function display_floating_password_form(){
        //Inputs
        let label = $('<label>').attr('for','password').text('Contraseña:');
        let input = $('<input>').attr({'id':'password', 'placeholder': 'Contraseña', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'password'});
        
        let label_2 = $('<label>').attr('for','new_password').text('Nueva contraseña:');
        let input_2 = $('<input>').attr({'id':'new_password', 'placeholder': 'Nueva contraseña', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'password'});
        
        let label_3 = $('<label>').attr('for','confirm_password').text('Confirma nueva contraseña:');
        let input_3 = $('<input>').attr({'id':'confirm_password', 'placeholder': 'Confirma la nueva contraseña', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'password'});

        let div_1 = $('<div>').append(label,input).addClass('password-form-input');
        let div_2 = $('<div>').append(label_2,input_2).addClass('password-form-input');
        let div_3 = $('<div>').append(label_3,input_3).addClass('password-form-input');
        let div_inputs = $('<div>').append(div_1, div_2, div_3).addClass('password-form-inputs');
        
        //Alert
        let alert = $('<p>').text('Una vez cambiada la contraseña, se cerrara sesión').addClass('text-warning');

        //Buttons
        let button_edit = $('<div>').attr('onclick','validate_password()').addClass('button-info').text('Editar');
        let button_cancel = $('<div>').attr('onclick','remove_floating_password_form()').addClass('button-danger').text('Cancelar');

        //Build dialog
        let div_header = $('<div>').html('<h2>Formulario cambio de contraseña<\h2>').addClass('floating-dialog-header');
        let div_alert = $('<div>').attr('id','password_alert').append(alert).addClass('floating-dialog-alert');
        let div_content = $('<div>').append(div_inputs).addClass('floating-dialog-content');
        let div_buttons = $('<div>').append(button_edit, button_cancel).addClass('floating-dialog-buttons');

        let dialog = $('<dialog open>').addClass('floating-dialog').attr('id','floating-dialog');
        
        dialog.append(div_header, div_alert, div_content, div_buttons)
        $('body').append(dialog);
        
        position_floating_dialog(dialog);
    }

    export function remove_floating_password_form(){
        let dialog = $('#floating-dialog');
        if (dialog.length !== 0){
            dialog.remove();
            desbloquear_correo();
            desbloquear_username();
        }
    }

    function show_alert_password(danger = true, text, logout=false){
        let alert = $('#password_alert');
        let alert_text = $('<p>').text(text);
        let alertClass = null;
        
        if (danger == true){
            alertClass = 'text-danger';
        }else{
            alertClass = 'text-success';
        }

        alert.empty();
        alert.removeClass('text-warning').addClass(alertClass);
        alert.append(alert_text);
        setTimeout(function(){
            alert.empty();
            alert.removeClass(alertClass).addClass('text-warning');
            if(logout == true){
                window.location.href = "/auth/logout";
            }
        }, 3000);
    }
//End DOM manipulation

//Start validations and edit 
    //- validate_password(): Validations to check if is possible send the request to modify the password. In case of some error, it show in screen the error, in other hand,
    //                      calls the method modify_password to start the edit operatoin.
    //- validate_password_format(password): Returns true if the password passed as parameter has a valid format, in other case returns false.
    //- modify_passwords(password, new_password): Makes the request to modified the password. In case of exit, use the method show_alert_password with the parameter logout setted in true; in other case,
    //                                              just use the method show_alert_password.

    export function validate_password(){
        let password = $('#password').val();
        let new_password = $('#new_password').val();
        let confirm_password = $('#confirm_password').val();
        let format_result = validate_password_format(new_password);

        if (password == '' || new_password == '' || confirm_password == ''){
            show_alert_password(true, 'Todos los campos son requeridos');
        }
        else if(password == new_password){
            show_alert_password(true, 'La nueva contraseña no puede ser igual a la actual');
        }
        else if(format_result.error == true){
            show_alert_password(true, format_result.message);
        }
        else if (new_password != confirm_password){
            show_alert_password(true, 'La nueva contraseña no coincide con la confirmación');
        }
        else{
            modify_password(password, new_password);
        }
    }

    function modify_password(password, new_password){
        edit_password(password, new_password).then(data=>{
            if(data['error'] == false){
                show_alert_password(false,data['message'],true);
            }else{
                show_alert_password(true,data['message']);
            }
        }).catch(error=>{
            console.log(error);
        })
    }

//End validations and edit
