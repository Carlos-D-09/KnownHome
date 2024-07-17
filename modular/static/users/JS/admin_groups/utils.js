import { position_floating_dialog } from "../utils.js"
import { get_groups } from "./request.js"

//Build container to show groups
export function set_groups_container(){
    let table_container = $('#table-container');
    table_container.empty();

    let table_header = $('<div>').addClass('table-header');
    let table_filter = $('<div>').addClass('table-filters');
    let table_content = $('<div>').addClass('table-content');

    let header = $('<h2>').text('Grupos de mis maestros');
    table_header.append(header);

    let search_container = $('<div>').addClass('search-container');
    let search_input = $('<input>').attr({'type':'text', 'id':'search', 'placeholder':'Grupo', 'autocomplete':'off'});
    let button_search = $('<button>').attr('id','search-button').addClass('button-info button-disabled').prop('disabled',true);
    let button_search_icon = $('<i>').addClass('fa-brands fa-searchengin');
    button_search.append(button_search_icon);
    
    search_container.append(search_input);
    table_filter.append(search_container, button_search);

    table_container.append(table_header, table_filter, table_content);
}

//Print table with the groups
export function print_groups(groups){
    let table_content = $('.table-content');
    table_content.empty();
    let table = $('<table>').attr('id', 'table-groups').addClass('table-style');
    let th_row = build_group_header(); 
    table.append(th_row);

    groups.forEach(group => {
        let tr = build_group_row(group);
        table.append(tr);
    });

    table_content.append(table);
}

//Build table groups header
function build_group_header(){
    let th_row = $('<tr>'); 
    let name = $('<th>').addClass('right-border').text('Nombre del grupo');
    let desc = $('<th>').addClass('right-border').text('Descripción');
    let teacher = $('<th>').addClass('right-border').text('Maestro');
    let students = $('<th>').addClass('right-border').text('Número de alumnos');
    let date = $('<th>').addClass('right-border').text('Fecha de creación');
    let options = $('<th>').text('Opciones');
    th_row.append(name, desc, teacher, students, date, options);

    return th_row;
}


//Build table group row 
function build_group_row(group){
    let tr = $('<tr>');
    let name = $('<td>').addClass('top-border right-border').text(group.nombre);
    let desc = $('<td>').addClass('top-border right-border').text(group.descripcion);
    let teacher = $('<td>').addClass('top-border right-border').text(group.nombre_maestro);
    
    let students = $('<td>').addClass('top-border right-border students');
    let students_text = $('<p>').text(group.num_alumnos);
    let students_hypervincule = $('<a>').attr({'onclick':"show_students("+group.id+")", 'href':'#'})
    let students_icon = $('<i>').addClass('fa-solid fa-eye');
    students_hypervincule.append(students_icon);
    students.append(students_text, students_hypervincule);
    
    let date = $('<td>').addClass('top-border right-border').text(group.created_at);
    
    let options = $('<td>').addClass('top-border');
    let div_options = $('<div>').addClass('options-container');
    
    let edit_button = $('<button>').addClass('button-info').attr({'onclick':'show_edit_form('+group.id+')'});
    let edit_icon = $('<i>').addClass('fa-solid fa-pen');
    edit_button.append(edit_icon);
    
    let delete_button = $('<button>').addClass('button-danger').attr({'onclick':'show_alert_delete('+ group.id +')'});
    let delete_icon = $('<i>').addClass('fa-solid fa-trash');
    delete_button.append(delete_icon);

    div_options.append(edit_button, delete_button);
    options.append(div_options);

    tr.append(name, desc, teacher, students, date, options);
    return tr;
}

//Build container to show students
export function set_group_students_container(group){
    let table_container = $('#table-container');
    table_container.empty();

    let table_header = $('<div>').addClass('table-header');
    let table_filter = $('<div>').addClass('table-students-filters');
    let table_content = $('<div>').addClass('table-content');

    let header = $('<h2>').text(group.nombre);
    table_header.append(header);
    
    let back_container = $('<div>').addClass('back-container');
    let button_back_icon = $('<i>').addClass('fa-solid fa-arrow-left fa-2x').attr('onclick','show_groups()');
    back_container.append(button_back_icon);
    
    let search_container = $('<div>').addClass('search-students-container');
    let search_input = $('<input>').attr({'type':'text', 'id':'search-enrolled-students', 'placeholder':'Alumno', 'autocomplete':'off'});
    
    let button_search = $('<button>').attr({'id':'search-enrolled-students-button','value':group.id}).addClass('button-info button-disabled').prop('disabled',true);
    let button_search_icon = $('<i>').addClass('fa-brands fa-searchengin');
    button_search.append(button_search_icon);    
    
    let button_add = $('<button>').addClass('button-success circle-2h').attr({'group':group.id, 'id':'button-add-student'});
    let add_icon = $('<i>').addClass('fa-solid fa-user-plus');
    button_add.append(add_icon)

    search_container.append(button_add, search_input, button_search);
    table_filter.append(back_container, search_container);

    table_container.append(table_header, table_filter, table_content);
}

//Print table with the students
export function print_students(students, group){
    let table_content = $('.table-content');
    table_content.empty();
    let table = $('<table>').attr('id', 'table-groups').addClass('table-style-no-horizontal-overflow');
    let th_row = build_students_header(); 
    table.append(th_row);

    students.forEach(student => {
        let tr = build_student_row(student, group.id);
        table.append(tr);
    });

    table_content.append(table);
}

//Build table students header
function build_students_header(){
    let th_row = $('<tr>'); 
    let name = $('<th>').addClass('right-border').text('Estudiante');
    let options = $('<th>').text('Opciones');
    th_row.append(name, options);

    return th_row;
}

//Build table students row 
function build_student_row(student, group_id){
    let tr = $('<tr>'); 
    let name = $('<td>').addClass('top-border right-border').text(student.student_username);
    let div_options = $('<div>').addClass('options-container');
    let options = $('<td>').addClass('top-border');
    
    let delete_button = $('<button>').addClass('button-danger circle').attr('onclick','remove_student('+student.student_id+','+group_id+')');
    let delete_icon = $('<i>').addClass('fa-solid fa-minus');
    delete_button.append(delete_icon);
    div_options.append(delete_button)

    options.append(div_options);

    tr.append(name, options);

    return tr;
}

//Set dialog to show available students to enroll
export function show_available_students(students, group){
    let dialog = $('<dialog open>').addClass('floating-students-list show').attr('id','floating-dialog-students');
    let header = $('<div>').addClass('floating-students-list-header');
    let content = $('<div>').addClass('floating-students-list-content');
    let footer = $('<div>').addClass('floating-students-list-footer');

    let div_header_title = $('<div>').addClass('floating-students-list-header-title');
    let title = $('<h2>').text('Estudiantes disponibles');
    div_header_title.append(title);

    let div_header_search = $('<div>').addClass('floating-students-list-header-search');
    let search_input = $('<input>').attr({'type':'text', 'placeholder':'Estudiante','id':'search-students-for-enroll'});
    let search_button = $('<button>').addClass('button-info button-disabled').attr({'id':'search-students-for-enroll-button','value':group}).prop('disabled',true);
    let search_icon = $('<i>').addClass('fa-brands fa-searchengin');
    search_button.append(search_icon);
    div_header_search.append(search_input, search_button);

    header.append(div_header_title, div_header_search);

    let cancel_button = $('<button>').addClass('button-danger').attr('onclick','remove_floating_students_list('+group+')').text('Cancelar');
    footer.append(cancel_button)

    dialog.append(header, content, footer)

    $('body').append(dialog);
    position_floating_dialog(dialog);
    
    print_students_for_enroll(students, group);
}

//Create table with students to enroll
export function print_students_for_enroll(students, group, message=true){
    let container = $('.floating-students-list-content');
    container.empty();
    let table_container = $('<div>').addClass('floating-students-list-content-table');
    if (students.length != 0){
        let table = $('<table>').attr('id', 'table-students-for-enroll').addClass('table-style');
        let th_row = build_students_for_enroll_header(); 
        table.append(th_row);
    
        students.forEach(student => {
            let tr = build_students_for_enroll_row(student, group);
            table.append(tr);
        });
        table_container.append(table);
        container.append(table_container);
    }else if (students.lent == 0 && message==false){
        let advice = $('<p>').addClass('text-info').text('Todos los alumnos posibles ya han sido registrados'); 
        container.append(advice);
    }
}

//Create header for the table with students to enroll 
function build_students_for_enroll_header(){
    let th_row = $('<tr>'); 
    let name = $('<th>').addClass('right-border').text('Estudiante');
    let options = $('<th>').text('Opciones');
    th_row.append(name, options);

    return th_row;
}

//Create row for the table with students to enroll 
function build_students_for_enroll_row(student, group_id){
    let th_row = $('<tr>').attr('id','student-'+student.id); 
    let name = $('<td>').addClass('top-border right-border').text(student.username);
    
    let div_options = $('<div>').addClass('options-container');
    let options = $('<td>').addClass('top-border');
    
    let delete_button = $('<button>').addClass('button-success circle').attr('onclick','add_student('+student.id+','+group_id+')');
    let delete_icon = $('<i>').addClass('fa-solid fa-plus');
    delete_button.append(delete_icon);
    div_options.append(delete_button)

    options.append(div_options);

    th_row.append(name, options);

    return th_row;
}

//Remove student from the table of available students
export function remove_student_from_list_for_enroll(student){
    $('#student-'+student).addClass('remove');
    setTimeout(function(){
        $('#student-'+student).remove();
    },1000)
}

//Shoe edit form for a group
export function print_edit_form(group){
    let dialog = $('<dialog open>').addClass('floating-group-form show').attr('id','floating-group-form');
    let content = $('<div>').addClass('floating-group-form-content');
    let footer = $('<div>').addClass('floating-group-form-footer');
    let header = $('<div>').addClass('floating-group-form-header');
    
    //Header
    let title = $('<h2>').text('Formulario edición de grupos');
    header.append(title);
    
    //Content
    let alert = $('<div>').addClass('floating-group-form-content-alert');

    //Content-name
    let name_div = $('<div>').addClass('floating-group-form-content-name');
    let name_label = $('<label>').attr({'for':'name'}).text('Nombre del grupo:')
    let name_input = $('<input>').addClass('input-border-bottom-white').attr({'id':'name', 'value':group.nombre, 'autocomplete':false});
    name_div.append(name_label, name_input);
    
    //Content-date
    let date_div = $('<div>').addClass('floating-group-form-content-date');
    let date_text = $('<b>').text('Fecha de creación:')
    let date = $('<p>').text(group.created_at);
    date_div.append(date_text, date);
    
    //Content-teacher
    let teacher_div = $('<div>').addClass('floating-group-form-content-teacher');
    let teacher_text = $('<b>').text('Maestro:')
    let teacher = $('<p>').text(group.maestro);
    teacher_div.append(teacher_text, teacher);

    //Content-description
    let desc_div = $('<div>').addClass('floating-group-form-content-desc');
    let desc_label = $('<label>').attr({'for':'desc'}).text('Descripción:')
    let desc = $('<textarea>').addClass('textarea-border-inner').attr({'id':'desc','max-length':'250','rows':'5'}).text(group.descripcion);
    desc_div.append(desc_label, desc);

    content.append(alert, teacher_div, date_div, name_div, desc_div);

    //Footer
    let edit_button = $('<button>').addClass('button-info').attr('onclick','modify_group('+group.id+')').text('Editar')
    let cancel_button = $('<button>').addClass('button-danger').attr('onclick','remove_edit_form()').text('Cancelar');
    footer.append(edit_button,cancel_button)

    dialog.append(header, content, footer)

    $('body').append(dialog);
    position_floating_dialog(dialog);
}

//Remove edit form for a group
export function remove_edit_form(){
    let dialog = $('#floating-group-form').removeClass('show').addClass('remove');
    setTimeout(function(){
        dialog.remove();
    },1000)
}

//Return a json lik {error:'', message: ''}. Return error true if name or desc aren't valid. Return error false, if are valid
export function validate_group_edit_inputs(){
    let name = $('#name').val();
    let desc = $('#desc').val();
    if(name.length == 0 || desc.length == 0){
        return {error: 'true', message: 'Ambos campos son requeridos'};
    }
    if(name.length > 50){
        return {error: 'true', message: 'El nombre no puede ser mayor a 50 caracteres'};
    }
    if(desc.length > 250){
        return {error: 'true', message: 'La descripción no puede ser mayor a 250 caracteres'};
    }  

    return {error: false, message:null}
}

export function show_edit_form_alert(message){
    let alert = $('.floating-group-form-content-alert');
    let alert_text = $('<p>').addClass('text-danger show').text(message);
    alert.append(alert_text);
    setTimeout(function(){
        alert.empty();
    },4000);
}

//Build a dialog to request a confirmation to delete group. 
export function show_alert_delete(group_id){
    let div_text = $('<div>').attr('id','delete-alert-text').addClass('delete-alert-text');
    let text_alert = $('<p>').addClass('text-danger').text('La acción que vas a realizar es irreversible y eliminara el grupo, ¿Estas seguro que deseas continuar?');
    
    div_text.append(text_alert);

    let div_button = $('<div>').attr('id','delete-buttons').addClass('floating-dialog-buttons');
    let button_cofirm = $('<button>').attr('onclick','remove_group('+group_id+')').addClass('button-success').text('Confirmar');
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
        get_groups().then(data=>{
            if(data['error']==false){
                set_groups_container();
                let groups = data['groups'];
                print_groups(groups);
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