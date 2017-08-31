$(document).ready(function()
{
 $("#subscription-list ul").on('click',".btn.btn-secondary",function(event)
 {
 event.preventDefault();
 var action= $(this).closest('li').text().replace(/\s\s+/g, '/');
 var ur = ('/account/subscription/').concat(action,'/');
 var li = $(this).closest('li')
li.fadeOut('slow', function() { li.remove(); });
var hr =li.next('hr')
hr.fadeOut('slow',function() { hr.remove(); });
 $.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  $('#subscribe-options-list ul').append(response.code);
 }
});
 });


 $("#subscribe-options-list ul").on('click',".btn.btn-secondary",function(event)
 {
 event.preventDefault();
 var action= $(this).closest('li').text().replace(/\s\s+/g, '/');
 var ur = ('/account/subscription/').concat(action,'/');
 var li = $(this).closest('li')
li.fadeOut('slow', function() { li.remove(); });
 var hr =li.next('hr')
hr.fadeOut('slow',function() { hr.remove(); });
 $.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  $('#subscription-list ul').append(response.code);
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
