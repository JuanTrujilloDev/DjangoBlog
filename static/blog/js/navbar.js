$(function() {
    // Sidebar toggle behavior
    $('#sidebarCollapse').on('click', function() {
      $('#sidebar, #content, #mainContainer').toggleClass('active');

      
      
    });

    

    
   
  });

$(document).ready(function() {
    $('.datepicker').datepicker();
   
});

/*
var size = window.screen.width;

if(size < 1200){



if (jQuery('#mainContainer').hasClass('active')){
  document.getElementById('mainContainer').style.visibility="hidden";
  console.log("Has class active");
}else{
  document.getElementById('mainContainer').style.visibility="visible";
  console.log("Nevermind");
}
}
*/







