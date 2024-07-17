import { get_teachers } from "./requests.js";
import { position_floating_dialog } from "../utils.js";

//Build table to show teachers
export function print_teachers(teachers){
    let table = $('#table-teachers');
    table.empty();
    
    let header = build_header();
    table.append(header)

    teachers.forEach(teacher => {
        let row = build_row(teacher);
        table.append(row);
    });
}

//Build table teacher header
function build_header(){
    let row = $('<tr>');
    let username = $('<th>').addClass('rigth-border').text('Nombre de usuario');
    let email = $('<th>').addClass('rigth-border').text('Fecha de registro');
    let date = $('<th>').addClass('rigth-border').text('Grupos totales');
    let email_verified = $('<th>').addClass('rigth-border').text('Alumnos registrados');
    let options = $('<th>').text('Opciones');

    row.append(username, email, date, email_verified, options);

    return row;
}

//Build table teacher row 
function build_row(teacher){
    let row = $('<tr>');
    let username = $('<td>').addClass('top-border rigth-border').text(teacher.username);
    let date = $('<td>').addClass('top-border rigth-border').text(teacher.created_at);
    let grupos = $('<td>').addClass('top-border rigth-border').text(teacher.grupos_creados);
    let alumnos = $('<td>').addClass('top-border rigth-border').text(teacher.alumnos_registrados);
    
    let options = $('<td>').addClass('top-border');
    let div_options = $('<div>').addClass('options-container');
    
    let button_info_icon = $('<i>').addClass('fa-solid fa-user-pen');
    let button_info = $('<button>').addClass('button-info').attr({'onclick':'show_edit_form('+teacher.id+')'}).append(button_info_icon);
    
    let button_delete_icon = $('<i>').addClass('fa-solid fa-trash');
    let button_delete = $('<button>').addClass('button-danger').attr({'onclick':'show_alert_delete('+teacher.id+')','value':teacher.id}).append(button_delete_icon);
    
    div_options.append(button_info, button_delete);
    options.append(div_options);

    row.append(username, date, grupos, alumnos, options);

    return row;
}

//Remove dialog with edit form
export function remove_floating_edit_form(){
    get_teachers().then(data=>{
        if(data['error']==false){
            let teachers = data['teachers'];
            print_teachers(teachers);
        }
    }).catch(error=>{
        console.log(error);
    })
    $('#floating-dialog').remove();

}

//Build dialog to show edit form 
export function display_floating_edit_form(teacher){
    //Inputs
    let label = $('<label>').attr('for','username').text('Nombre de usuario:');
    let input = $('<input>').attr({'id':'username', 'placeholder': 'Nombre de usuario', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'text', 'value':teacher.username});
    
    let label_2 = $('<label>').attr('for','password').text('Contraseña:');
    let input_2 = $('<input>').attr({'id':'password', 'placeholder': 'Nueva contraseña', 'class':'input-border-bottom-white', 'autocomplete':'off', 'type': 'password'});
    

    let div_1 = $('<div>').append(label,input).addClass('edit-form-input');
    let div_2 = $('<div>').append(label_2,input_2).addClass('edit-form-input');
    let div_inputs = $('<div>').append(div_1, div_2).addClass('edit-form-inputs');
    
    //Alert
    let alert = $('<p>').addClass('text-warning').attr('id','edit-alert');

    //Buttons
    let button_edit = $('<div>').attr('onclick','edit_teacher('+teacher.id+')').addClass('button-info').text('Editar');
    let button_cancel = $('<div>').attr('onclick','remove_floating_edit_form()').addClass('button-danger').text('Cancelar');

    //Build dialog
    let div_header = $('<div>').html('<h2>Formulario edición de maestro<\h2>').addClass('floating-dialog-header');
    let div_alert = $('<div>').attr('id','password_alert').append(alert).addClass('floating-dialog-alert');
    let div_content = $('<div>').append(div_inputs).addClass('floating-dialog-content');
    let div_buttons = $('<div>').append(button_edit, button_cancel).addClass('floating-dialog-buttons');

    let dialog = $('<dialog open>').addClass('floating-dialog').attr('id','floating-dialog');
    dialog.append(div_header, div_alert, div_content, div_buttons)
    
    $('body').append(dialog);
    
    position_floating_dialog(dialog);    
}

//Build a dialog to request a confirmation to delete user. 
export function show_alert_delete(teacher_id){
    let div_text = $('<div>').attr('id','delete-alert-text').addClass('delete-alert-text');
    let text_alert = $('<p>').addClass('text-danger').text('La acción que vas a realizar es irreversible y eliminara todos los grupos asociados al maestro, ¿Estas seguro que deseas continuar?');
    
    div_text.append(text_alert);

    let div_button = $('<div>').attr('id','delete-buttons').addClass('floating-dialog-buttons');
    let button_cofirm = $('<button>').attr('onclick','delete_teacher('+teacher_id+')').addClass('button-success').text('Confirmar');
    let button_cancel = $('<button>').attr('onclick','remove_delete_alert()').addClass('button-danger').text('Cancelar');

    div_button.append(button_cofirm, button_cancel);


    let dialog = $('<dialog open>').addClass('floating-dialog-delete show').attr('id','floating-dialog-delete');
    
    dialog.append(div_text, div_button);
    
    $('body').append(dialog);
    
    position_floating_dialog(dialog);    
}

//Remove confirmation dialog 
export function remove_delete_alert(reload=false){
    if(reload == true){
        get_teachers().then(data=>{
            if(data['error']==false){
                let teachers = data['teachers'];
                print_teachers(teachers);
            }
        }).catch(error=>{
            console.log(error);
        })
    }
    
    $('#floating-dialog-delete').removeClass('show').addClass('remove');
    setTimeout(function(){
        $('#floating-dialog-delete').remove();
    },1000)
}