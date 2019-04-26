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

$(document).bind("contextmenu", function (event) {
  event.preventDefault();

  var ae= this.activeElement;
  if(ae.tagName == 'A'){
    $("<a href='"+ae.href+"' class='custom-menu' target='_blank'>Open link in new tab</a>")
      .appendTo("body")
      .css({top: event.pageY + "px", left: event.pageX + "px"});
  }
}
                );

$(document).bind("click", function(event) {
  $("a.custom-menu").hide();
});

