import { get_user_by_name_email, get_users } from "./requests.js";
import { print_users } from "./utils.js";

//Listener to detect when the input change. Disable the search button if the text is empty, in other case able it. 
//Also if the text is null, print again the users info.
export function handle_search_input(){
    $(document).on("input", "#search ", function() {
        let word = $("#search").val(); 
        if (word.length == 0){
            $('#search-button').prop('disabled',true).addClass('button-disabled');+
            get_users().then(data=>{
                if(data['error']==false){
                    let users = data['users'];
                    print_users(users);
                }
            }).catch(error=>{
                console.log(error);
            })
        }else{
            $('#search-button').removeAttr('disabled').removeClass('button-disabled');
        }
    });
}

//Listener to detect when the button search is pressed
export function button_search_pressed(){
    $(document).on("click",'#search-button', function(){
        $('#search').prop('disabled',true);
        let word = $('#search').val();
        get_user_by_name_email(word).then(data => {
            if(data['error'] == false){
                let users = data['users'];
                print_users(users);
                setTimeout(function(){
                    $('#search').removeAttr('disabled');
                }, 1000);
            }
        }).catch(error=>{
            console.log(error);
        })

    });
}