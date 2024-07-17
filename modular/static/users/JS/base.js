$(document).ready(function(){ 
    profile_image_pressed();
    extend_nav_bar_pressed();
});

//Display user menu (logout and check profile)
function profile_image_pressed(){
    $('#profile-image').click(function(){
        $('#dropdown-menu').toggle("slow");
    });
}

//Listener to detect when is clicked the button navbar toggle botton is pressed
function extend_nav_bar_pressed(){
    $('#button-collapse').click(function(){
        let icon_container = $('#button-collapse');
        let icon = $("#button-collapse-icon");
        let navbar = $('#nav-bar');
        let navbar_list = $('#nav-list');
        let content = $('#content');
        
        icon_container.addClass('disabled');
        
        let width = window.innerWidth;

        // On screens wider than 768px, the navbar is positioned on the left side and is expanded by default. 
        // When the toggle button is pressed, the navbar receives the 'active' CSS class and collapses.
        // Therefore, when the navbar has the 'active' class, it is collapsed; otherwise, it is expanded.
        
        // On screens narrower than 768px, the navbar is hidden, and the toggle button is located in the header. 
        // When the button is pressed, the navbar receives the 'active' class and the menu is displayed. 
        // In this case, when the navbar has the 'active' class, it is expanded; otherwise, it is collapsed.
        
        if (width > 768){
            if(navbar_list.hasClass('active')){ //Expand navbar
                
                navbar_list.removeClass('active'); 
                icon.removeClass('active');
                
                navbar.removeClass('hidden-text'); //Show Text
                justify_icon_to_left();

                //Smooth animations
                navbar.css({'animation':'nav-bar 1s ease-in-out','width':'200px'}); //Change navbar size
                content.css({'animation':'content 1s ease-in-out','padding-left':'200px'}); //Change content size
                
                setTimeout(function(){
                    icon_container.removeClass('disabled');
                    navbar.css('animation', '');
                    content.css('animation', '');
                },1000);
            
            }else{ //Collapse navbar
                navbar_list.addClass('active');
                icon.addClass('active'); 
                
                center_icon();
                
                //Smooth animations
                navbar.addClass('hidden-text').css({'animation':'nav-bar-collapse 1s ease-in-out','width':'80px'}); //Change navbar size
                content.css({'animation':'content-collapse 1s ease-in-out','padding-left':'80px'}); //Change navbar size
                
                setTimeout(function(){
                    icon_container.removeClass('disabled');
                    navbar.css('animation', '');
                    content.css('animation', '');
                },1000);
            }
        }else{
            if(navbar_list.hasClass('active')){ //Collapse navbar
                icon.removeClass('active');
                navbar_list.addClass('hide');
                setTimeout(function(){
                    navbar_list.removeClass('active hide');
                    icon_container.removeClass('disabled');
                    navbar.css('animation', '');
                    content.css('animation', '');
                }, 1000);
            }else{ //Expand navbar
                navbar_list.addClass('active');
                icon.addClass('active');
                setTimeout(function(){
                    icon_container.removeClass('disabled');
                    navbar.css('animation', '');
                    content.css('animation', '');
                }, 1000);
            }

        }
    });
}

//Justify navbar items to the left side 
function justify_icon_to_left(){
    let index = 0;
    while (true) {
        let link = $('#link-'+index);
        
        if(link.length === 0) return false;
        
        link.css('justify-content','flex-start');
        index+=1;
    }
}


//Justify navbar items to the center
function center_icon(){
    let index = 0;
    while (true) {
        let link = $('#link-'+index);
        
        if(link.length === 0) return false;
        
        
        link.css('justify-content','center');
        index+=1;
    }
}