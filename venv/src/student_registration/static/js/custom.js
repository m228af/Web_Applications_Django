$(document).ready(function(){
  $(".dateinput").datepicker({
      changeYear: true,
      changeMonth: true,
      dateFormat: 'yy-mm-dd' // Set the desired date format
  });
});


function updateClock() {
  var now = new Date();
  var clock = document.getElementById('clock');
  var date = document.getElementById('date');
  clock.textContent = now.toLocaleTimeString();
  date.textContent = now.toDateString();
}

setInterval(updateClock, 1000);
updateClock(); // Call it once to initialize the time

