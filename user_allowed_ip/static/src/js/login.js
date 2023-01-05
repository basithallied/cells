
$(document).ready(function () {

    $('.oe_login_form').each(function () {

        //set I relate Information
        $.getJSON('https://ipapi.co/json', function(data) {
            document.getElementById("ip").value = data['ip'];
        }); 

    });

});
