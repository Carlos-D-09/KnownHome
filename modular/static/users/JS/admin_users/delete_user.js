import { show_alert } from "../utils.js";
import { print_users } from "./utils.js";
import { get_users } from "./requests.js";
import { delete_user_request} from "./requests.js";

//Make request to delete user
export function delete_user(user_id){
    delete_user_request(user_id).then(data=>{
        let floating_dialog_delete = $('#floating-dialog-delete');
        if(data['error']==false){
            floating_dialog_delete.remove();
            show_alert(false, data['message']);
            get_users().then(data=>{
                print_users(data['users'])
            }).catch(error=>{
                console.log(error);
            })
        }else{
            show_alert(true, data['message']);
        }
    })
}