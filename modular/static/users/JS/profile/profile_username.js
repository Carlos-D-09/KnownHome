import { validate_username_format, show_alert } from "../utils.js";
import { get_user, edit_username } from "./requests.js";
import { bloquear_correo, bloquear_password, desbloquear_correo, desbloquear_password} from "./utils.js";

//Module asociated to all the username edit operations

// Start DOM operations
    //- username_select(): Listener to detect when the user wants to edit the username
    //- username_unselect(): Method called when the user cancel the username edit operation
    //- add_username_input(): Remove the username text and change it for an input
    //- remove_username_input(): Remove the username input and change it for text
    

    export function username_select(){
        $(document).on('click', '#username-icon', function(){
            get_user().then(data=>{
                if(data['error'] == false){
                    let usuario = data['user'];
                    add_username_input(usuario.username);
                    bloquear_correo();
                    bloquear_password();
                }
            }).catch(error =>{
                console.log(error);
            })
        })
    }

    export function username_unselect(){
        get_user().then(data=>{
            if(data['error'] == false){
                let usuario = data['user'];
                remove_username_input(usuario.username);
                desbloquear_correo();
                desbloquear_password();
            }
        }).catch(error =>{
            console.log(error);
        })
    }

    function add_username_input(username){
        let container = $('#username-container');
        let buttons_container = $('#buttons-container');
        let label = $('<b>').text('Username:');
        let input = $('<input>').attr({'id':'username', 'placeholder': 'Username', 'class':'input-border-bottom-white', 'autocomplete':'off', 'value':username});

        container.empty();

        if(container.hasClass('icon-info')){
            container.removeClass('icon-info');
            container.addClass('input-info');
        }

        container.append(label,input);

        let edit_button = $('<button>').attr('onclick','validate_username()').addClass('button-info').text('Editar');
        let cancel_button = $('<button>').attr('onclick','username_unselect()').addClass('button-danger').text('Cancelar');
        buttons_container.append(edit_button, cancel_button);
    }

    function remove_username_input(username){
        let buttons_container = $('#buttons-container');
        let container = $('#username-container');
        let icon = $('<i>').addClass('fa-solid fa-pen-nib').attr('id','username-icon');
        let label = $('<b>').text('Username: ');
        let text = $('<p>').text(username);
        
        container.empty();

        if(container.hasClass('input-info')){
            container.removeClass('input-info');
            container.addClass('icon-info');
        }

        container.append(icon, label, text);
        buttons_container.empty();
    }

//End DOM manipulation

//Start validation and edit

    //- validate_username(): Calls the validation for the username. In case it is valid, calls the method modify_email to start the edition process, in other case, it shows the error
    //- modify_username(): Makes the request to modified the username. In case of exit, calls the method username_unselect and show the succesfull message; in other hand,
    //                      show in screen the error

    export function validate_username(){
        let username = $('#username').val();
        let result = validate_username_format(username);
        if (result.error){
            show_alert(true,result.message)
        }else{
            modify_username(username);
        }
    }

    function modify_username(username){
        edit_username(username).then(data => {
            if(data['error'] == false){
                show_alert(false,data['message']);
                username_unselect();
            }else{
                show_alert(true,data['message']);
            }
        }).catch(error => {
            console.log(error);
        });
    }
//End validation and edit