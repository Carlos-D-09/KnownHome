import { delete_teacher_request} from "./requests.js";
import { remove_delete_alert } from "./utils.js"
import { show_alert } from "../utils.js";

//Make request to delete teacher
export function delete_teacher(user_id){
    delete_teacher_request(user_id).then(data=>{
        if(data['error']==false){
            remove_delete_alert(true);
            show_alert(false, data['message']);
        }else{
            show_alert(true, data['message']);
        }
    })
}