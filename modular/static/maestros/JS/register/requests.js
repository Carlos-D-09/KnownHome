export function register_master(username, password){
    return new Promise((resolve, reject) => {
        let url = '/maestro/register';
        let inputs = {
            username: username,
            password: password
        }
        $.post(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        })
    });
}