$(document).ready(function () {

  $('#sidebarLeftCollapse').on('click', function () {
    $('#sidebar_left_bitton').toggleClass('active');
    $('#sidebar_left').toggleClass('active');

    if ($('#sidebar_left_button')[0].classList.contains('active')) {
      $(this).text("Show left sidebar");
    } else {
      $(this).text("Hide left sidebar");
    }
  });

  $('#sidebarRightCollapse').on('click', function () {
    $('#sidebar_right_button').toggleClass('active');
    $('#sidebar_right').toggleClass('active');

    if ($('#sidebar_right_button')[0].classList.contains('active')) {
      $('#sidebarRightCollapse').text("Show right sidebar");
    } else {
      $('#sidebarRightCollapse').text("Hide right sidebar");
    }
  });

});
