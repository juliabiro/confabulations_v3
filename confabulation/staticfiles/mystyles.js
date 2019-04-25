$(document).ready(function () {

  $('#sidebar_left_button').on('change', function () {
    $('#sidebar_left').toggleClass('active');
  });
  $('#sidebar_right_button').on('change', function () {
    $('#sidebar_right').toggleClass('active');
  });

  $('.theme-dropdown').on('click', function(){
    var themeID = $(this).attr('id');

    $('.'+themeID).toggleClass('highlight');
  });
});
