//File with re-used functions into the profile folder

export function bloquear_username(){
    let password_icon = $('#username-icon');
    password_icon.prop('disabled',true).css('cursor','not-allowed');
}

export function desbloquear_username(){
    let password_icon = $('#username-icon');
    password_icon.prop('disabled',false).css('cursor','pointer');
}

export function bloquear_correo(){
    let correo_icon = $('#correo-icon');
    correo_icon.prop('disabled',true).css('cursor','not-allowed');
}

export function desbloquear_correo(){
    let password_icon = $('#correo-icon');
    password_icon.prop('disabled',false).css('cursor','pointer');
}

export function bloquear_password(){
    let password_icon = $('#password-icon');
    password_icon.prop('disabled',true).css('cursor','not-allowed');
}

export function desbloquear_password(){
    let password_icon = $('#password-icon');
    password_icon.prop('disabled',false).css('cursor','pointer');
}