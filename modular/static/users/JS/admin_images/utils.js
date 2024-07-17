export function print_images(images, begin, end){
    let images_content = $('#images-container');
    
    images_content.addClass('remove');
    
    setTimeout(function(){
        images_content.empty();
        
        images.forEach(image => {
            images_content.append(build_image_container(image));
        });
        
        set_images_counter(begin, end);
        images_content.removeClass('remove').addClass('show');
    }, 1000);

}


function build_image_container(image){
    let image_card = $('<div>').addClass('image-card');

    let div_img = $('<div>').addClass('image-card-img');
    let img = $('<img>').attr({'src':image.ruta,'alt':''});

    div_img.append(img);

    let div_desc = $('<div>').addClass('image-card-desc');
    
    let group_leyend = $('<b>').text('Grupo: ')
    let group = $('<p>').append(group_leyend, image.group);

    let user_leyend = $('<b>').text('Usuario: ');
    let user = $('<p>').append(user_leyend);
    
    if(image.alumno == null || image.alumno == ''){
        user.append(image.maestro);
    }else{
        user.append(image.alumno);
    }

    let object_leyend = $('<b>').text('Objeto: ');
    let object = $('<p>').append(object_leyend, image.objeto);

    let classification_leyend = $('<b>').text('Clasificación: ').css('color','black');
    let classification = $('<p>').append(classification_leyend);

    if (image.clasificacion_correcta == true){
        classification.addClass('text-success').append('Correcta');
    }else if(image.clasificacion_correcta != null){
        classification.addClass('text-danger').append('Erronea');
    }

    let riesgo_leyend = $('<b>').text('Riesgo: ');
    let riesgo = $('<p>').append(riesgo_leyend, image.riesgo);

    div_desc.append(group, user, object, classification, riesgo);

    image_card.append(div_img, div_desc);

    return image_card;
}

function set_images_counter(start, finish){
    let begin = $('#begin');
    let end = $('#end');

    begin.empty();
    end.empty();

    begin.append(start);
    end.append(finish);

}