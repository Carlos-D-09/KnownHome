import { get_users } from "./requests.js";
import { position_floating_dialog } from "../utils.js";

//Build table with admin users
export function print_users(users){
    let table = $('#table-users');
    table.empty();
    
    let header = build_header();
    table.append(header)

    users.forEach(user => {
        let row = build_row(user);
        table.append(row);
    });
}

//Build table admin users header
function build_header(){
    let row = $('<tr>');
    let username = $('<th>').addClass('rigth-border').text('Nombre de usuario');
    let email = $('<th>').addClass('rigth-border').text('Correo electrónico');
    let date = $('<th>').addClass('rigth-border').text('Fecha de registro');
    let email_verified = $('<th>').addClass('rigth-border').text('Correo verificado');
    let options = $('<th>').text('Opciones');

    row.append(username, email, date, email_verified, options);

    return row;
}

//Build table admin users row
function build_row(user){
    let row = $('<tr>');
    let username = $('<td>').addClass('top-border rigth-border').text(user.username);
    let email = $('<td>').addClass('top-border rigth-border').text(user.correo);
    let date = $('<td>').addClass('top-border rigth-border').text(user.created_at);
    
    let email_verified_text = $('<p>');
    if (user.verified == true){
        email_verified_text.addClass('text-success').text('Verificado');
    }else{
        email_verified_text.addClass('text-danger').text('No verificado');
    }
    let email_verified = $('<td>').addClass('top-border rigth-border').append(email_verified_text);
    
    let options = $('<td>').addClass('top-border');
    let div_options = $('<div>').addClass('options-container');
    
    let button_info_icon = $('<i>').addClass('fa-solid fa-user-pen');
    let button_info = $('<button>').addClass('button-info').attr({'onclick':'show_edit_form('+user.id+')'}).append(button_info_icon);
    
    let button_delete_icon = $('<i>').addClass('fa-solid fa-trash');
    let button_delete = $('<button>').addClass('button-danger').attr({'onclick':'show_alert_delete('+user.id+')','value':user.id}).append(button_delete_icon);
    
    div_options.append(button_info, button_delete);
    options.append(div_options);

    row.append(username, email, date, email_verified, options);

    return row;
}

//Remove edit form and reprint admin users
export function remove_floating_edit_form(){
    get_users().then(data=>{
        if(data['error']==false){
            let users = data['users'];
            print_users(users);
        }
    }).catch(error=>{
        console.log(error);
    })
    $('#floating-dialog').remove();

}

//Show edit form for admin user
export function display_floating_edit_form(user){
    //Inputs
    let label = $('<label>').attr('for','username').text('Nombre de usuario:');
    let input = $('<input>').attr({'id':'username', 'placeholder': 'Nombre de usuario', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'text', 'value':user.username});
    
    let label_2 = $('<label>').attr('for','email').text('Correo electrónico:');
    let input_2 = $('<input>').attr({'id':'email', 'placeholder': 'Correo electrónico', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'text', 'value':user.correo});
    
    let label_3 = $('<label>').attr('for','password').text('Contraseña:');
    let input_3 = $('<input>').attr({'id':'password', 'placeholder': 'Nueva contraseña', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'password'});
    

    let div_1 = $('<div>').append(label,input).addClass('edit-form-input');
    let div_2 = $('<div>').append(label_2,input_2).addClass('edit-form-input');
    let div_3 = $('<div>').append(label_3, input_3).addClass('edit-form-input');
    let div_inputs = $('<div>').append(div_1, div_2, div_3).addClass('edit-form-inputs');
    
    //Alert
    let alert = $('<p>').addClass('text-warning').attr('id','edit-alert');

    //Buttons
    let button_edit = $('<div>').attr('onclick','edit_user('+user.id+')').addClass('button-info').text('Editar');
    let button_cancel = $('<div>').attr('onclick','remove_floating_edit_form()').addClass('button-danger').text('Cancelar');

    //Build dialog
    let div_header = $('<div>').html('<h2>Formulario edición de usuario administrador<\h2>').addClass('floating-dialog-header');
    let div_alert = $('<div>').attr('id','password_alert').append(alert).addClass('floating-dialog-alert');
    let div_content = $('<div>').append(div_inputs).addClass('floating-dialog-content');
    let div_buttons = $('<div>').append(button_edit, button_cancel).addClass('floating-dialog-buttons');

    let dialog = $('<dialog open>').addClass('floating-dialog').attr('id','floating-dialog');
    
    dialog.append(div_header, div_alert, div_content, div_buttons)
    
    $('body').append(dialog);
    
    position_floating_dialog(dialog);    
    

}

//Show alert to request to the use confirm admin user delete
export function show_alert_delete(user_id){
    let div_text = $('<div>').attr('id','delete-alert-text').addClass('delete-alert-text');
    let text_alert = $('<p>').addClass('text-danger').text('La acción que vas a realizar es irreversible, ¿Estas seguro que deseas continuar?');
    
    div_text.append(text_alert);

    let div_button = $('<div>').attr('id','delete-buttons').addClass('floating-dialog-buttons');
    let button_cofirm = $('<button>').attr('onclick','delete_user('+user_id+')').addClass('button-success').text('Confirmar');
    let button_cancel = $('<button>').attr('onclick','remove_delete_alert()').addClass('button-danger').text('Cancelar');

    div_button.append(button_cofirm, button_cancel);


    let dialog = $('<dialog open>').addClass('floating-dialog-delete show').attr('id','floating-dialog-delete');
    
    dialog.append(div_text, div_button);
    $('body').append(dialog);
    
    position_floating_dialog(dialog);    
}

//Remove alert to confirm admin user delete
export function remove_delete_alert(){
    get_users().then(data=>{
        if(data['error']==false){
            let users = data['users'];
            print_users(users);
        }
    }).catch(error=>{
        console.log(error);
    })
    $('#floating-dialog-delete').removeClass('show').addClass('remove');
    setTimeout(function(){
        $('#floating-dialog-delete').remove();
    }, 1000)
}