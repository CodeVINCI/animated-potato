$(document).ready(function()
{

$('#socrates-search').keypress(function(e){
    if(e.which === 13){
        $("#searchsubmit").click();
        return false;
    }
});


$(".navbar-form").on('click','#searchsubmit',function(event)
{
var search_term=$(this).siblings('div').find('#socrates-search').val();
var ur= ("/account/searchsocrates/").concat(search_term);
 if (search_term.trim() ==="")
    {alert('Empty search');
    return 0;
    }
 window.location.href= ur;
});

$('.thumbnail').on('click', "#readlater", function(event)
{
var id=$(this).parent().prev('p').attr('id');
var ur = ('/account/remove/readlater/').concat(id);
var li = $(this).closest('.thumbnail')

$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
li.fadeOut('slow', function() { li.remove(); });
}
});
});

$('.social_buttons').on('click', "#like", function(event)
{
event.preventDefault();
var id =$(this).children('meta').data().pk;
var action=$(this).children('meta').data().nextaction;
var ur =("/home/vote/").concat(action,'/',id);
var out = $(this)
$.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  out.parent('div').html(response.codeself);
 }
 });

});

$('.social_buttons').on('click', "#dislike", function(event)
{
event.preventDefault();
var id =$(this).children('meta').data().pk;
var action=$(this).children('meta').data().nextaction;
var ur =("/home/vote/").concat(action,'/',id);
var out = $(this)
$.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  out.parent('div').html(response.codeself);
 }
 });
 });

 $('.thumbnail').on('click', '#visitbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/visitors/').concat(id);
$.get(ur);
return true;
});

$('.thumbnail').on('click', '#suggestbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/suggestion/').concat(id);
$.get(ur);
return false;
});

/*showing url on opening the modal*/
  $(window.location.hash).modal('show');
    $('a[data-toggle="modal"]').click(function(){
        window.location.hash = $(this).attr('href');
    });

    function revertToOriginalURL() {
        var original = window.location.href.substr(0, window.location.href.indexOf('#'))
        history.replaceState({}, document.title, original);
    }

    $('.modal').on('hidden.bs.modal', function () {
        revertToOriginalURL();
    });

    $('#wrap').delegate('.comment_box','keypress',function(e){
    if(e.which === 13){
    //alert($(this).siblings('#comment_button').html());
        $(this).siblings("#comment_button").click();
        return false;
    }
});
//this is ajax of comment sectioon do something to it so that it will work
/*handling comment form submission*/
$('.thumbnail').on('click','#comment_button', function(event){
    event.preventDefault();
    console.log("form submitted!")
     var id = $(this).prev('meta').data().pk// sanity check
    // AJAX for posting
    var ur = ('/home/make_comment/').concat(id,'/');
    var ht = $(this).siblings('#post-comment').val();
    var csrf=$(this).siblings('#post-comment').prev('input').attr('value');
    var out=$(this);
    var da={the_post:ht, pk:id, csrfmiddlewaretoken: csrf};
    $.ajax(
    {
      url:ur,
      type:'POST',
      data:da,
      dataType:'json',
      success:function(response)
      {
       out.siblings('#post-comment').val('');
       out.parent().next("#talk").prepend(response.text);
      }
    });


});

$('#wrap').on('click','.comment_delete',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/remove_comment/".concat(id);
var out = $(this)
$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
var li = out.closest('li');
li.fadeOut('slow', function() { li.remove(); });
}
});
return false;
});



$(document).on('click', '.notify' ,function(event){
var notificationid = $(this).attr("data");
var ur= "/home/seennotification/".concat(notificationid);
var out = $(this)

$.ajax(
{
url:ur,
method:'get',
async: false,
});

});


});

