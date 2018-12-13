$(document).ready(function () {

  $('#sidebarLeftCollapse').on('click', function () {
    $('#sidebar_left').toggleClass('active');

    if ($('#sidebar_left')[0].classList.contains('active')) {
      $(this).text("Show left sidebar");
    } else {
      $(this).text("Hide left sidebar");
    }
  });

  $('#sidebarRightCollapse').on('click', function () {
    $('#sidebar_right').toggleClass('active');

    if ($('#sidebar_right')[0].classList.contains('active')) {
      $('#sidebarRightCollapse').text("Show right sidebar");
    } else {
      $('#sidebarRightCollapse').text("Hide right sidebar");
    }
  });

});
