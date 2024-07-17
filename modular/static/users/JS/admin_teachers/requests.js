//Request to get the teachers registered by the current logged user
export function get_teachers(){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_teachers';
        $.get(url, function(data){
            resolve(data);
        }).fail(function (error) { 
            reject(error);
        });
    });
}

//Get details for x teacher
export function get_teacher(user_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_teacher/'+user_id;
        $.get(url, function(data){
            resolve(data);
        }).fail(function (error) {
                reject(error);
        });
    })
}

//Seearch teacher by username 
export function search_teacher(word){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_teacher/search';
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

//Request to edit x teacher
export function edit_teacher_request(user_id, username, password){ 
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_teacher/edit/'+user_id;
        let inputs = {
            "username": username,
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

//Request to delete x teacher
export function delete_teacher_request(teacher_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_teacher/delete/'+teacher_id;
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

