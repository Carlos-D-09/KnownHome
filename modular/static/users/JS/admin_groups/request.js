//Request to get enrolled students into x group
export function get_enrolled_students(group_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups/'+group_id+'/students';
        $.get(url, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}

//Request to add x student to y group
export function add_student_group(student, group){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups/'+group+'/add_student'
        let inputs = {
            'student': student
        }
        $.post(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        })
    });
}

//Request to get not enrolled students into x group
export function get_not_enrolled_students(group_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups/'+group_id+'/add_student'
        $.get(url, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        })
    });
}

//Request to get group details
export function get_group(group_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups/'+group_id;
        $.get(url,function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}

//Request to get all the groups owned by the teacher registerd by the current user logged
export function get_groups(){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups';
        $.get(url,function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}

//Request to edit x group
export function edit_group(group_id, name, desc){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_groups/'+group_id+'/edit';
        let inputs = {
            name: name,
            desc: desc
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
    });
}

//Request to delete a group
export function delete_group(group_id){
    return new Promise((resolve, reject) => {
        let url = '/user/api/admin_groups/'+group_id+'/delete';
        $.ajax({
            url: url,
            type: 'DELETE',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        })
    });
}

//Request to remove a student from x group
export function remove_student_from_group(group_id, student_id){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_groups/'+ group_id + '/remove_student/'+student_id;
        $.ajax({
            url: url,
            type: 'DELETE',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

//Request to search a group by name
export function search_group(term){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_groups/search';
        let inputs = {
            term: term
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}

//Request to search enrolled students into x group by username
export function search_enrolled_students(group, word){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_groups/'+group+'/students/search';
        let inputs = {
            term: word
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    })
}

//Request to search not enrolled students in x group by username
export function search_not_enrolled_students(group, word){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_groups/'+group+'/add_students/search';
        let inputs = {
            term: word
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    })
}
