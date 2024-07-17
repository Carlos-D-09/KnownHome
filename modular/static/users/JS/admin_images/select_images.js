import { get_next_images, get_previous_images } from "./request.js";
import { print_images } from "./utils.js";

export function previous_images(){
    $(document).on("click","#previous-images",function(){
        let current_image = Number($('#begin').text());
        get_previous_images(current_image).then(data=>{
            if(data['error']==false){
                let images = data['images'];
                print_images(images, data['begin'], data['end']);
            }else{
                console.log(data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    });
}

export function next_images(){
    $(document).on("click","#next-images",function(){
        let current_image = Number($('#end').text());
        get_next_images(current_image).then(data=>{
            if(data['error']==false){
                let images = data['images'];
                print_images(images, data['begin'], data['end']);
            }else{
                console.group(data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    });
}