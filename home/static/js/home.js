$(document).ready(function()
{
var valnow=$('#my-data').data().filter;
$(function() {
    $("#filters").val(valnow);
});
$('div.select_filters').on('click', ".btn.btn-secondary", function(event)
{
event.preventDefault();
var target= document.getElementById("filters").value;
var ur = ("/home/").concat(target);
window.location.href = ur;

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
//this is ajax of comment sectioon do something to it so that it will work
/*handling comment form submission*/
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    post_comment();
    // AJAX for posting
    function post_comment() {
    console.log("create post is working!") // sanity check

    $.ajax({
       url : "#exampleModalLong{{post.0.pk}}/",//the endpoint
       type : "POST",
       data :{ the_post : $('#post-comment').val()},
       //handle a successful response
       success : function(json){
          $('#post-comment').val('');//remove the value from the input
          console.log(json);//log the returned json to the console
          $("#talk").prepend("<li><strong>"+json.text+"</strong>-<em>"+json.user+"</em> - <span>"+json.created_on+"</span></li>"
          );
          console.log("success");

       },
       //handle a non-successful response
       error : function(xhr,errmsg,err){
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          "<a href='#' class='close'>&times;</a></div>");//add the error to the dom
          console.log(xhr.status + ": "+xhr.responseText);//provide a bit more info about the error to the console
       }
    });
};
});




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

