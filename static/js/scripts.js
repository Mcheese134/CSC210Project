//jquery equivalent of dom content loaded
$(document).ready(function () {
    var modal = document.getElementById('loginForm');

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
  });

  