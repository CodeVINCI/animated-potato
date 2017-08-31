$(document).ready(function()
{

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

$('div.my-button').on('click', ".btn.btn-secondary", function(event)
{
 event.preventDefault();
 var href = $('#my-data').data();
 var possib = href.possibleaction;
 var pk = href.pk;
 var pre = "/account/connect/";
 var slash = "/"
 var ur = pre.concat(possib,slash,pk,slash);
 $.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  $('div.my-button').html(response.code);
 }
 });

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
