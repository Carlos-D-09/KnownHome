import { get_object_statistic } from "./requests.js";
import { show_alert } from "./utils.js";

$(document).ready(function(){ 
    //functions and methods 
    select_inicio_nav_bar();
    scanned_images_graph();
    scanned_images_by_object();

    //Listeners
    scanned_images_by_object_select_change();
});

//Change the class for the option-1 (usuarios) in the navbar to add the selected effect
function select_inicio_nav_bar(){
    let current_selected = $('#option-1');
    current_selected.addClass('selected');
}

//scanned-images graph
function scanned_images_graph(){
    const LABELS = ['Incorrectas', 'Correctas']; 
    const COLORS = ['#ffafaf', '#b8ffaf'];

    let graph = $('#scanned-images');
    let right_images = graph.data('right-images');
    let total_images = graph.data('total-images');

    const data = {
        labels: LABELS,
        datasets: [{
            label: "",
            data: [total_images-right_images, right_images ],
            backgroundColor: COLORS
        }]
    }
    const config = {
        type: 'pie',
        data: data,
    }
    const options = {
        responsive: true,
        maintainAspectRatio: true
    }
    
    new Chart(graph, config, options);
}

//Scanned images by object graph
function scanned_images_by_object(){
    let graph = $('#scanned-images-by-object');
    if (graph.length != 0){
        const LABELS = ['Incorrectas', 'Correctas']; 
        const COLORS = ['#ffafaf', '#b8ffaf'];
    
        let right_images = graph.data('right-images');
        let total_images = graph.data('total-images');
    
        const data = {
            labels: LABELS,
            datasets: [{
                label: "",
                data: [total_images-right_images, right_images],
                backgroundColor: COLORS
            }]
        }
        const config = {
            type: 'pie',
            data: data,
        }
        const options = {
            responsive: true,
            maintainAspectRatio: true
        }
        
        new Chart(graph, config, options);
    }
}

//Listener to detect when is changed the scanner object 
function scanned_images_by_object_select_change(){
    let select = $('#objects')
    select.on('change',()=>{
        let option_selected = select.find('option:selected');
        get_object_statistic(option_selected.val()).then(data=>{
            if(data['error'] == true){
                show_alert(true, data['message']);
            }else{
                let statistics = data['statistics'];
                let total_images = statistics.total_images;
                let right_images = statistics.right_images;
                
                if (total_images == 0){
                    set_images_by_object_tags(0, 0);
                    put_sad_face();
                    return;
                }

                if (total_images-right_images == 0 && total_images != 0){
                    set_images_by_object_tags(100, 0);
                    put_graph(total_images, right_images);
                    return;
                }
                
                if(right_images == 0 && total_images != 0){
                    set_images_by_object_tags(0, 100);
                    put_graph(total_images, right_images);
                    return;
                }
                
                let percent_right_images = Math.round(100 * right_images / total_images);
                let percent_wrong_images = Math.round(100 * (total_images-right_images) / total_images);
                set_images_by_object_tags(percent_right_images, percent_wrong_images);
                put_graph(total_images, right_images);
                return;
            }
        })
    });
}

function set_images_by_object_tags(percent_right, percent_wrong){
    let wrong_images = $('#wrong-images');
    let right_images = $('#right-images');
    wrong_images.text('Erróneas: '+percent_wrong+'%');
    right_images.text('Correctas: '+percent_right+'%');

}

function put_graph(total_images, right_images){
    $('#object-graph').empty();
    let graph = $('<canvas>').attr('id','scanned-images-by-object').data({'total-images':total_images,'right-images':right_images})
    $('#object-graph').append(graph);
    scanned_images_by_object();
}

function put_sad_face(){
    if ($('.no-images').length == 0){
        let container = $('<div>').addClass('no-images');
        let sad_face = $('<div>').addClass('sad-face');
        let left_eye = $('<div>').addClass('eye').append($('<span>'));
        let right_eye = $('<div>').addClass('eye').append($('<span>'), $('<span>'));
        let mouth = $('<div>').addClass('mouth').append($('<span>'), $('<span>'));
        let text = $('<p>').text('Todavía no se han escaneado imágenes con este objeto');
    
        sad_face.append(left_eye, right_eye, mouth);
        container.append(sad_face);
    
        $('#object-graph').empty();
        $('#object-graph').append(container, text);
    }

}