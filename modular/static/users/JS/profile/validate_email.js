$(document).ready(function(){
    verifcar_button_pressed();
    resend_email_pressed();
    wrong_email_pressed();

})

//Listener para el buton verificar
function verifcar_button_pressed(){
    $('#verificar-button').click(function(){
        //Validar inputs
        let alert_container = $('#alert-container');
        let text = $('#text-alert');
        let result = validate_empty_inputs();
        let spinner = $('<div>').attr('id','spinner').addClass('spinner show');
        if (result.full == true){
            alert_container.prepend(spinner);
            verification_code_request(result.code).then(data=>{
                handle_verification_code_response(text, spinner, data);
            });
        }else{
            let message = 'No se permiten enviar códigos incompletos';
            show_alert(text, message,null, false, false);
        }
    })
}

//Retorna False y null en caso de que alguno de los inputs esten vacios, en caso contrario retorna True y el código que se forma juntando todos los inputs.
function validate_empty_inputs(){
    let code = '';
    for (let i = 1; i < 7; i++){
        let input = $(`#${i}`);
        if (input.val() == ''){
            return {'full':false,'code':null};
        }else{
            code = code + input.val();   
        }
    }
    code = code.toUpperCase()
    return {'full':true,'code':code};
}

function handle_verification_code_response(text_alert, spinner, data){
    if(data['error'] == true){
        setTimeout(function(){
            show_alert(text_alert, data['message'], spinner, false);
        },1000)
    }else{
        show_alert(text_alert, data['message'] + '. Reedirecionando al perfil del usuario.', spinner, true, true);
    }
}

//Función para convertir a mayuscular el caracter introducido por el usuario y mover el focus al previo o siguiente input vacio. 
function handle_next_input(e){
    let input_index = parseInt(e.id);
    let previous_input = $(`#${input_index - 1}`);
    let next_input = $(`#${input_index + 1}`);

    e.value = e.value.toUpperCase();

    if (e.value != "") {
        if (previous_input.length == 0 && next_input.length != 0 && next_input.val()=="") { // Primer input
            next_input.focus();
        } else if (previous_input.length != 0 && next_input.length == 0 && previous_input.val() == "") { // Último input
            previous_input.focus();
        } else{ // Inputs intermedios
            let free_input = evaluate_empty_input(input_index);
            if (free_input) {
                free_input.focus();
            }
        }
    }
}

function evaluate_empty_input(current_input_index){
    for (let i = current_input_index-1; i > 0; i--) {
        let input = $(`#${i}`);
        if(input.val() == ""){
            return input;
        }
    }
    for (let i = current_input_index+1; i <= 6; i++){
        let input = $(`#${i}`);;
        if(input.val() == ""){
            return input;
        }
    }

    return null;
}

    
//Listener para el vinculo de reenvio de correo electrónico
function resend_email_pressed(){
    $('#reenviar-codigo').click(function(){
        let alert_container = $('#alert-container');
        let text = $('#text-alert');
        let spinner = $('<div>').attr('id','spinner').addClass('spinner show');
        alert_container.append(spinner);
        resend_email_request().then(data => {            
            setTimeout(function() {
                handle_resend_response(text, spinner, data);
            }, 1000);
        });
    })
}

//Manejar la respuesta del servidor
function handle_resend_response(text_alert, spinner, data){
    if(data['error'] == true){
        show_alert(text_alert, data['message'], spinner, false);
    }else{
        show_alert(text_alert, data['message'], spinner, true);
    }
}

//Listener para reedirigir al formulario para alterar el correo eletrónico introducido por el usuario
function wrong_email_pressed(){
    $('#correo-erroneo').click(function(){ 
        window.location.href = "/user/recover_email_not_validated"
    })
}

//Mostrar el mensaje de alerta
function show_alert(text_alert, message, spinner, successClass, redirect_user = false){
    // Limpiar las posibles clases del contendor de alerta
    text_alert.removeClass('text-danger-bold text-success-verification-code remove');
    
    //Determinar el estilo de la alerta si es exitosa o erronea
    if(successClass == true){
        text_alert.addClass('text-success-verification-code')
    }else{
        text_alert.addClass('text-danger-bold')
    }

    if(redirect_user == false){ //En caso de que no se reediriga al usuario a su página principal
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
            window.location.href = "/user";
        },5000);
    }
}


//Peticiones

//Peticion para solicitar al servidor reenviar el correo electrónico
function resend_email_request(){
    return new Promise((resolve, reject) => {
        let url = "/user/resend_verification_code";
        $.ajax({
            url: url,
            type: 'PUT',
            contentType: 'application/json',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    })
}

//Petición para revisar el codigo de verificación introducido
function verification_code_request(code){
    return new Promise((resolve, reject) => {
        let url = "/user/validate_email";
        let input = {
            "codigo": code
        };
        $.ajax({
            url: url,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(input),
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}
