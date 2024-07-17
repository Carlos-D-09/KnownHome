import { set_groups_container, print_groups, print_edit_form, validate_group_edit_inputs, show_edit_form_alert, remove_delete_alert,} from "./utils.js";
import { get_groups, get_group, edit_group, delete_group, search_group } from "./request.js";
import { show_alert } from "../utils.js";

//Get groups availables to edit by the current user and print it
export function show_groups(){
    set_groups_container();
    get_groups().then(data=>{
        let groups = data['groups'];
        print_groups(groups);
    }).catch(error=>{
        console.log(error);
    });
}

//Get x group info and show form to edit it
export function show_edit_form(group_id){
    get_group(group_id).then(data=>{
        let group = data['group'];
        print_edit_form(group);
    }).catch(error=>{
        console.log(error);
    });
}

//Get inputs from edit form, validate it and make request to edita a group
export function modify_group(group_id){
    let validation = validate_group_edit_inputs();
    if(validation['error'] == false){
        let name = $('#name').val();
        let desc = $('#desc').val();
        edit_group(group_id,name, desc).then(data=>{
            if(data['error']==false){
                show_alert(false, data['message']);
                show_groups();
            }else{
                show_edit_form_alert(data['message']);
            }
        }).catch(error=>{
            console.log(error);
        });
    }else{
        show_edit_form_alert(validation.message);
    }
}

//Make request to delete a group
export function remove_group(group_id){
    delete_group(group_id).then(data=>{
        if(data['error'] == false){
            show_alert(false, data['message']);
            remove_delete_alert(true);
        }else{
            show_alert(true, data['message']);
        }
    })
}

//Listener to detect when the search group input have changed and able or disabled search button
export function handle_search_input(){
    $(document).on("input","#search", function(){
        let word = $("#search").val();
        if(word.length == 0){
            $('#search-button').prop('disabled',true).addClass('button-disabled');
            show_groups();
        }else{
            $('#search-button').removeAttr('disabled').removeClass('button-disabled');
        }
    });
}

//Listener to detect when the button search group is pressed and make search request
export function button_search_group_pressed(){
    $(document).on("click", "#search-button", function(){
        $('#search').prop('disabled', true);
        let word = $('#search').val();
        search_group(word).then(data => {
            if(data['error'] == false){
                let groups = data['groups'];
                print_groups(groups);
                setTimeout(function(){
                    $('#search').removeAttr('disabled');
                }, 1000);
            }else{
                show_alert(true, data['message']);
            }
        }).catch(error=>{
            console.log(error);
        })
    });
}