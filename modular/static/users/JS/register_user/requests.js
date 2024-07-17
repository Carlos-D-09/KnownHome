//Request to register a user
export function register_user(username, email, password, rol){
    return new Promise((resolve, reject) => {
        let url = '/user/register';
        let inputs = {
            username: username,
            email: email,
            password: password,
            rol: rol
        }
        $.post(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        })
    });
}