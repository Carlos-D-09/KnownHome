//Request the next images to show
export function get_next_images(current_image){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_images/next_images';
        let inputs = {
            "current_image": current_image
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}

//Request the previouus images to show
export function get_previous_images(current_image){
    return new Promise((resolve,reject) => {
        let url = '/user/api/admin_images/previous_images';
        let inputs = {
            "current_image": current_image
        }
        $.get(url, inputs, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}