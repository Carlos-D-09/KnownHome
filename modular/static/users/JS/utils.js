//Return true if the username is not valid and a message with the error. 
export function validate_username_format(username){
    if (username == ''){
        return {'error': true, 'message':'El nombre de usuario no puede estar vacío'};
    }
    if (username.length > 50){
        return {'error': true, 'message':'El nombre de usuario no puede ser mayor a 50 caracteres ¿'};
    }

    return {'error': false, 'message':'Formato del nombre de usuario valido'}
}

////Return true if the username is not valid and a message with the error. 
export function validate_email_format(email){
    const correoValido =   /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,6}$/;
    if(email.length == ''){
        return {'error':true, 'message': 'El correo electrónico no puede estar vacío'};
    }

    if (!correoValido.test(email)){
        return {'error':true, 'message':'Porfavor introduce un correo valido'};
    }

    return {'error':false, 'message': 'Formato de correo electrónico valido'}; 
}

//Return true if the password is not valid and a message with the error. 
export function validate_password_format(password){
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    const symbols = '!@#$%^&*()_-+={}[]|:;"<>,.?/';

    if(password.length < 8){
        return {'error':true, 'message': 'La contraseña debe de ser al menos de 8 caracteres de largo'};
    }

    // La expresión [...password] convierte la cadena en un array de caracteres para que puedas usar el método some.
    const lower = [...password].some(char => lowercase.includes(char));
    const upper = [...password].some(char => uppercase.includes(char));
    const digit = [...password].some(char => digits.includes(char));
    const symbol = [...password].some(char => symbols.includes(char));

    if (!lower || !upper || !digit || !symbol){
        return {'error':true, 'message': 'La contraseña debe contener al menos una mayúscula, una minúscula, un número y un símbolo'}; 
    }

    return {'error':false, 'message': 'Formato de contraseña valido'};
}

//Show floating alert
export function show_alert(danger, message){
    let alertClass = null;
    let icon = null;

    if (danger == true){
        alertClass = 'text-danger';
        icon = $('<i>').addClass('fa-solid fa-circle-exclamation fa-2x');
    }else{
        alertClass = 'text-success';
        icon = $('<i>').addClass('fa-regular fa-circle-check fa-2x');
    }
    
    let dialog = $('<dialog open>').addClass('floating-alert show '+ alertClass).attr('id','floating-dialog-alert');
    let content = $('<div>').addClass('floating-alert-content');
    let text = $('<p>').text(message)
    
    content.append(icon, text);
    dialog.append(content);
    
    $('body').append(dialog);
    
    position_floating_dialog(dialog);
    
    setTimeout(function(){
        dialog.removeClass('show').addClass('remove');
        setTimeout(function(){
            dialog.remove();
        }, 1000);
    }, 2000);
}

//Adjust floating dialog position
export function position_floating_dialog(dialog){
    const DIALOG_WIDTH = dialog.width();
    const DIALOG_HEIGHT = dialog.height();
    const PADDING_SIZE = 20;
    const NAVBAR_SIZE = 80;
    let navbar = $('#nav-bar');
    let floating_dialog = $(dialog);
    if(floating_dialog.length !== 0){
        let width = window.innerWidth;
        let translateX = window.innerWidth/2 - DIALOG_WIDTH/2;
        let translateY = window.innerHeight/2 - DIALOG_HEIGHT/2;
        
        if(width > 768){
            navbar.hasClass('hidden-text') ? translateX+PADDING_SIZE : translateX += NAVBAR_SIZE;
        }else{
            translateX-=PADDING_SIZE;
        }
        floating_dialog.css('transform', 'translate('+translateX+'px, '+translateY+'px)')
    }
}
