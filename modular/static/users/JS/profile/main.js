import { username_select, username_unselect, validate_username } from "./profile_username.js";
import { correo_select, correo_unselect, validate_email } from "./profile_email.js";
import { password_select, remove_floating_password_form, validate_password } from "./profile_password.js";

window.username_unselect = username_unselect;
window.correo_unselect = correo_unselect;
window.remove_floating_password_form = remove_floating_password_form;
window.validate_username = validate_username;
window.validate_email = validate_email;
window.validate_password = validate_password;

$(document).ready(function(){

    //Listeners
    username_select();
    correo_select();
    password_select();
});