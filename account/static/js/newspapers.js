$(document).ready(function()
{
var valnow=$('#my-data').data().source;

$(function() {
    $("#subscriptions").val(valnow);
});

//javascript for selecting a particular newspaper
$('div.select-newspaper').on('click', ".btn.btn-secondary", function(event)
{
var target= document.getElementById("subscriptions").value;
var ur = ("/account/newspapers/").concat(target);
window.location.href = ur;
});

//Ajax request to save a post to dashboard
$('.thumbnail').on('click', "#readlater", function(event)
{
var id=$(this).parent().prev('p').attr('id');
var ur = ('/account/save/readlater/').concat(id);
$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
 alert('Post is saved to your library');
}
});
});

//Ajax for social-like a post
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

//Ajax for social-dislike a post
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

//Ajax for visit counter for each post
 $('.thumbnail').on('click', '#visitbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/visitors/').concat(id);
$.get(ur);
return true;
});

//Ajax for suggestion counter and generating suggest notifications
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

     if (ht.trim() ==="")
    {alert('Comment is empty');
    return 0;
    }

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

//javascript for comment delete button
$('.arguments').on('click','.comment_delete',function(event)
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

//javascript for comment like button
$('.arguments').on('click','.comment_like',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/like_comment/".concat(id);
var out = $(this);
alert(ur);
return false;
});

//javascript for comment reply button
$('.arguments').on('click','.comment_reply',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/reply_comment/".concat(id);
var out = $(this);
alert(ur);
return false;
});



//final paranthesis
});


//this is csrf_token in javascript don't remove it.
$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


});

