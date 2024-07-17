export function get_user(){
    return new Promise((resolve, reject) => {
        let url = '/user/api/profile';
        $.get(url, function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
        });
    });
}

export function edit_username(username){
    return new Promise((resolve, reject) => {
        let url = '/user/profile/edit_username';
        let input = {
            "username": username
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
    })
}

export function edit_email(email){
    return new Promise((resolve, reject) => {
        let url = '/user/profile/edit_email';
        let input = {
            "email": email
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
    })
}

export function edit_password(password, new_password){
    return new Promise((resolve, reject) => {
        let url = '/user/profile/edit_password';
        let input = {
            "password": password,
            "new_password": new_password
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
    })
}

//Request to change email not validated
export function edit_email_request(correo, email_confirmation){
    return new Promise((resolve, reject) => {
        let url = "/user/recover_email_not_validated";
        let input = {
            "correo": correo,
            "confirmacion_correo": email_confirmation
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