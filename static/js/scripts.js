//jquery equivalent of dom content loaded
$(document).ready(function () {

  
    var modal = document.getElementById('loginForm');
    var menu = false;

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    $("#Menu").click(function(){
      openNav();
    }); 

    $("#closebtn").click(function(){
      closeNav();
    }); 


  });

function openNav() {
  console.log("I opened");
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  console.log("I closed");
  document.getElementById("mySidenav").style.width = "0";
}
