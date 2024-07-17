//Request the statistic for x object from admin view
export function get_object_statistic(id_object){
    return new Promise((resolve, reject) => {
        let url = '/user/api/statistic/'+id_object;
        $.get(url, function(data){
            resolve(data);
        }).fail(function(error){
            reject(error);
        });
    });
}