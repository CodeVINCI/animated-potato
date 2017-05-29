$(document).ready(function()
{
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
 })

})

})
