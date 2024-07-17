$(document).ready(function(){
    login_button_pressed();
})

//Listener del buton de loggin
function login_button_pressed(){
    $('#login-button').click(function(){
        let email = $('#email').val();
        let password = $('#password').val();

        //Validación de inputs
        if (validate_empty_inputs(email,password) == false || validate_email(email) == false){
            return false;
        }

        //Petición de inicio de sesión.
        login_request(email, password).then(data=>{
            if (data['error'] == true){
                let text = $('#text-alert');
                text.text(data['message']);
                setTimeout(function (){
                    text.empty();
                }, 3000);
            }
            else{
                window.location.href = "/user";
            }
        }).catch(error => console.log(error));
    });
}

//Retorna true si la variable email y password no vacios; en caso contrario retorna false.
function validate_empty_inputs(value1, value2){
    if(value1 == '' || value2 == ''){
        let text = $('#text-alert');
        text.text('Todos los campos son requeridos');
        setTimeout(function (){
            text.empty();
        }, 3000);
        return false;
    }
    return true;
}

//Retorna true si el correo introducido tiene un formato valido; en caso contrario, retorna false
function validate_email(email){
    const correoValido =   /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,6}$/;
    if (correoValido.test(email)){
        return true;
    }else{
        let text = $('#text-alert');
        text.text('Introduce un correo valido');
        setTimeout(function (){
            text.empty();
        }, 3000);
        return false;
    }
}

//Petición al servidor para iniciar sesión. 
function login_request(email, password){
    return new Promise((resolve, reject) => {
        let url = "/auth/login";
        let inputs = {
            "email": email, 
            "password": password
        }
        $.post(url,inputs,function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
         });
    });
}