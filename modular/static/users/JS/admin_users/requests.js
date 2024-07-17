//Get all the admin users registered on the platform
export function get_users(){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_users';
        $.get(url, function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
        });
    });
}

//Get x user info
export function get_user(user_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_user/'+user_id;
        $.get(url, function(data){
            resolve(data);
        }).fail(function (error) {
                reject(error);
        });
    })
}

//Search admin user by username or email
export function get_user_by_name_email(word){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_user/search';
        let inputs = {
            "search_term": word
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
        });
    });
}

//Request to edit x user (username, email, password)
export function edit_user_request(user_id, username, email, password){ 
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_user/edit/'+user_id;
        let inputs = {
            "username": username,
            "email": email,
            "password": password
        };
        $.ajax({
            url: url,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(inputs),
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    })
}

//Request to delete x user
export function delete_user_request(user_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_user/delete/'+user_id;
        $.ajax({
            url: url,
            type: 'DELETE',
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