$(document).ready(function()
{
var valnow=$('#my-data').data().filter;
$(function() {
    $("#filters").val(valnow);
});


var ready=true;
function yHandler()
{
var str="";
$('.thumbnail').each(function()
{
 str +=($(this).attr("id").concat(" "));
});
if ($(window).scrollTop() == ($(document).height() - $(window).height()))
{
ready=false;
$.ajax(
{
url:'/home/scroll/loadcontent/home',
method:'get',
data:{posts:str},
dataType:'json',
success:function(response)
{

  $("#col1").children('#tilescol1').append(response.col1);
  $("#col1").children('#tilescol1').append(response.col4);
  $("#col2").children('#tilescol2').append(response.col2);
  $("#col2").children('#tilescol2').append(response.col5);
  $("#col3").children('#tilescol3').append(response.col3);
  $("#col3").children('#tilescol3').append(response.col6);
}
}).always(function(){
                ready = true; //Reset the flag here
            });
}
}
window.onscroll=yHandler;
/*$(".testing").on('click','#data',function(event)
{
 var wrap = document.getElementById('tiles')
 var h= wrap.offsetHeight;
 alert(h);
});*/

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

$('div.select_filters').on('click', ".btn.btn-secondary", function(event)
{
event.preventDefault();
var target= document.getElementById("filters").value;
var ur = ("/home/").concat(target);
window.location.href = ur;

});

$('#wrap').on('click', "#readlater", function(event)
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

//social like a post ajax request
$('#wrap').on('click', "#like", function(event)
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

//social dislike a post ajax request
$('#wrap').on('click', "#dislike", function(event)
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


//visit site counter ajax request
 $('#wrap').on('click', '#visitbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/visitors/').concat(id);
$.get(ur);
return true;
});

//suggestions counter and generate suggest notification ajax request
$('#wrap').on('click', '#suggestbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/suggestion/').concat(id);
$.get(ur);
alert("This article has been suggested to your friends");
return false;
});

/*showing url on opening the modal*/
  //$(window.location.hash).modal('show');
   $('#wrap').on('click', 'a[data-toggle="modal"]' ,function(event){
        window.location.hash = $(this).attr('data');
      var m = $(this).parent('p').nextAll('.modal').first().attr('id');
      m = ('#').concat(m);
      $(m).modal('show');
      //$(window.location.hash).modal('show');
        return false;
    });
    //m.modal('show');
    //$(window.location.hash).modal('show');

    function revertToOriginalURL() {
        var original = window.location.href.substr(0, window.location.href.indexOf('#'))
        history.replaceState({}, document.title, original);
    }

    $('#wrap').on('hidden.bs.modal','.modal', function () {
        revertToOriginalURL();
    });

/*handling comment form submission*/
$('#wrap').on('click','#comment_button', function(event){
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

//javascript for comment like button
$('#wrap').on('click','.comment_like',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/like_comment/".concat(id);
var out = $(this);
alert(ur);
return false;
});

//javascript for comment reply button
$('#wrap').on('click','.comment_reply',function(event)
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

