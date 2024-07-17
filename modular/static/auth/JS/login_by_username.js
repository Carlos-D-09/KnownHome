$(document).ready(function(){
    login_button_pressed();
})

//Listener del buton de loggin
function login_button_pressed(){
    $('#login-button').click(function(){
        let username = $('#username').val();
        let password = $('#password').val();

        //Validación de inputs
        if (validate_empty_inputs(username,password) == false){
            return false;
        }

        //Petición de inicio de sesión.
        login_request(username, password).then(data=>{
            if (data['error'] == true){
                let text = $('#text-alert');
                text.text(data['message']);
                setTimeout(function (){
                    text.empty();
                }, 2000);
            }
            else{
                window.location.href = "/user"
            }
        }).catch(error => console.log(error));
    });
}

//Retorna true si la variable username y password no vacios; en caso contrario retorna false.
function validate_empty_inputs(username, password){
    if(username == '' || password == ''){
        let text = $('#text-alert');
        text.text('Todos los campos son requeridos');
        setTimeout(function (){
            text.empty();
        }, 2000);
        return false;
    }
    return true;
}

//Petición al servidor para iniciar sesión. 
function login_request(username, password){
    return new Promise((resolve, reject) => {
        let url = "/auth/login_by_username";
        let inputs = {
            "username": username, 
            "password": password
        }
        $.post(url,inputs,function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
         });
    });
}