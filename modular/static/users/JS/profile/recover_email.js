import { validate_email_format } from "../utils.js";
import { edit_email_request } from "./requests.js";

$(document).ready(function(){
    enviar_button_pressed();
    cancel_button_pressed();
});

//Listener del buton enviar
function enviar_button_pressed(){
    $('#edit-email-button').click(function(){
        let email = $('#email').val();
        let email_confirmation = $('#email-confirmation').val();
        
        if ( validate_empty_inputs(email, email_confirmation) == false || validate_email(email) == false || validate_emails_match(email, email_confirmation) == false){
            return false;
        }
        
        let alert_container = $('#alert-container');
        let text = $('#text-alert');
        let spinner = $('<div>').attr('id','spinner').addClass('spinner show');
        alert_container.prepend(spinner);
        edit_email_request(email, email_confirmation).then(data=>{
            handle_edit_email_request(text, spinner, data);
        })
    });
}

function handle_edit_email_request(text_alert, spinner, data){
    if(data['error'] == true){
        show_alert(text_alert, data['message'], spinner, false);
    }else{
        show_alert(text_alert, data['message'], spinner, true, true)
    }
}

//Retorna true si la variable email y password no vacios; en caso contrario retorna false.
function validate_empty_inputs(value1, value2){
    if(value1 == '' || value2 == ''){
         //Validar inputs
        let text = $('#text-alert');
        show_alert(text, 'Todos los campos son requeridos', null, false);
        return false;
    }
    return true;
}

//Retorna true si el correo introducido tiene un formato valido; en caso contrario, retorna false
function validate_email(email){
    let format_result = validate_email_format(email);
    if (format_result.error == false){
        return true;
    }else{
        let text = $('#text-alert');
        show_alert(text, format_result.message, null, false);
        return false;
    }
}

//Retorna true si las cadenas pasadas en los argumento coinciden, en caso contario retorna true
function validate_emails_match(email, email_confirmation){
    if(email != email_confirmation){
        let text = $('#text-alert');
        show_alert(text, 'Los correos no coinciden', null, false);
        return false;
    }
    return true;   
}

function cancel_button_pressed(){
    $('#cancel-button').click(function(){
        window.location.href = "/user/validate_email";
    });
}

function show_alert(text_alert, message, spinner, successClass, redirect_user=false){
    // Limpiar las posibles clases del contendor de alerta
    text_alert.removeClass('text-danger-bold text-success-verification-code remove');
    
    //Determinar el estilo de la alerta si es exitosa o erronea
    if(successClass == true){
        text_alert.addClass('text-success-verification-code')
    }else{
        text_alert.addClass('text-danger-bold')
    }

    if(redirect_user == false){ //En caso de que no se reediriga al usuario fuera de su sesión
        if(spinner != null){ //Remover el spinner si existe y mostrar el mensaje
            spinner.removeClass('show').addClass('remove');
            setTimeout(function(){
                spinner.remove();
    
                //Mostrar la alerat
                text_alert.addClass('show').empty().text(message);
                setTimeout(function(){
                    
                    //Remover la alerta 
                    text_alert.removeClass('show').addClass('remove');
                    setTimeout(function(){
                        text_alert.empty();
                        text_alert.removeClass('text-success-verification-code text-danger-bold');
                    },1000);
                },5000);
            }, 1000);
        }else{ //Mostrar el mensaje directamente
            text_alert.addClass('show').empty().text(message);
            setTimeout(function(){
                
                //Remover la alerta 
                text_alert.removeClass('show').addClass('remove');
                setTimeout(function(){
                    text_alert.empty();
                    text_alert.removeClass('text-success-verification-code text-danger-bold');
                },1000);
            },5000);
        }
    }else{ //En caso de que se diriga al usuario a su página principal
        console.log('correo validado');
        text_alert.addClass('show').append(message);
        setTimeout(function(){
            window.location.href = "/auth/logout";
        },5000);
    }
}