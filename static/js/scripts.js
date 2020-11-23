//jquery equivalent of dom content loaded
$(document).ready(function () {

  
    var modal = document.getElementById('loginForm');

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

    initMap()


  });

function openNav() {
  console.log("I opened");
  document.getElementById("mySidenav").style.width = "95%";
}

function closeNav() {
  console.log("I closed");
  document.getElementById("mySidenav").style.width = "0";
}

function initMap() {
  // The location of Uluru
  const uluru = { lat: -25.344, lng: 131.036 };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: uluru,
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}
