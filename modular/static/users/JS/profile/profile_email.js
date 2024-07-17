import { validate_email_format, show_alert } from "../utils.js";
import { get_user, edit_email } from "./requests.js";
import { bloquear_username, bloquear_password, desbloquear_username, desbloquear_password} from "./utils.js";

//Module asociated to all the username edit operations


//Start DOM manipulation

    // corre_select(): Listener to detect when the user wants to edit the email
    // correo_unselect(): Method called when the user cancel the email edit operation
    // add_correo_input(): Remove the email text and chenge it for an input
    // remove_correo_input(): Remove the email input and chage it for text

    export function correo_select(){
        $(document).on('click', '#correo-icon', function(){
            get_user().then(data=>{
                if(data['error'] == false){
                    let usuario = data['user'];
                    add_correo_input(usuario.correo);
                    bloquear_username();
                    bloquear_password();
                }
            }).catch(error =>{
                console.log(error);
            })
        })
    }

    export function correo_unselect(){
        get_user().then(data=>{
            if(data['error'] == false){
                let usuario = data['user'];
                remove_correo_input(usuario.correo);
                desbloquear_username();
                desbloquear_password();
            }
        }).catch(error =>{
            console.log(error);
        })
    }

    function add_correo_input(correo){
        let container = $('#correo-container');
        let buttons_container = $('#buttons-container');
        let alert = $('#alert-content');
        let label = $('<b>').text('Correo:');
        let input = $('<input>').attr({'id':'correo','placeholder': 'Correo electrónico', 'class':'input-border-bottom-white', 'autocomplete':'off', 'value':correo});
        
        container.empty();
        alert.empty();
        alert.text('Al modificar tu correo electrónico se enviara un código de verificación al nuevo y se cerrara sesión');

        if(container.hasClass('icon-info')){
            container.removeClass('icon-info');
            container.addClass('input-info');
        }

        container.append(label,input);

        let edit_button = $('<button>').attr('onclick','validate_email()').addClass('button-info').text('Editar');
        let cancel_button = $('<button>').attr('onclick','correo_unselect()').addClass('button-danger').text('Cancelar');
        buttons_container.append(edit_button, cancel_button);
    }

    function remove_correo_input(correo){
        let buttons_container = $('#buttons-container');
        let container = $('#correo-container');
        let alert = $('#alert-content');
        let icon = $('<i>').addClass('fa-solid fa-pen-nib').attr('id','correo-icon');
        let label = $('<b>').text('Correo: ');
        let text = $('<p>').text(correo);
        
        container.empty();
        alert.empty();

        if(container.hasClass('input-info')){
            container.removeClass('input-info');
            container.addClass('icon-info');
        }

        container.append(icon, label, text);
        buttons_container.empty();
    }

//End DOM manipulation

//Start validation and edit 

    //- validate_email(): Validations for the email, in case it is valid. calls the method modify_email to start the edition process, in other case, it shows the error
    //- validate_email_format(): Returns true if the email has a valid formad, in other case, it returns false. 
    //- modify_username(): Makes the request to modified the email. In case of exit, use the method show_alert with the parameters email and logout setted in true; in other case,
    //                      just use the method show_alert with the parameter email setted in true

    export function validate_email(){
        let email = $('#correo').val();
        let format_result = validate_email_format(email);
        if(format_result.error == false){
            modify_email(email);
        }
        else{
            show_alert(true,format_result.message, true);
        }
    }

    function modify_email(email){
        edit_email(email).then(data => {
            if(data['error'] == false){
                show_alert(false,data['message'], true, true);
            }else{
                show_alert(true,data['message'], true, false);
            }
        }).catch(error => {
            console.log(error);
        });
    }

//End validation and edit