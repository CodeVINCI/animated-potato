$(document).ready(function()
{
$(".navbar-form").on('click','#searchsubmit',function(event)
{
//var csrf= $(this).siblings('div').find('input').attr('value');
//var search_term=$(this).siblings('div').find('#socrates-search').val();
//var ur= '/account/searchsocrates/'.concat(search_term);
 //if (search_term.trim() ==="")
   // {alert('Empty search');
    //return 0;
    //}
 //window.location.href= ur;
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
