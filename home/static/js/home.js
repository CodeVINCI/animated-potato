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

$('#wrap').on('click', "#like", function(event)
{
event.preventDefault();
var id =$(this).next('meta').data().postid;
var action =$(this).closest('p #like').attr('class');
var q = $(this).closest('p #like').html();
var ur =("/home/vote/").concat(action,"/",id);
if (action=='social-like'){
$(this).closest('p #like').attr('class','social-unlike');
$(this).nextAll("button").first().attr('class','social-dislike');
}
else
{
$(this).closest('p #like').attr('class','social-like');
}
var out =$(this)
$.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  out.closest('p #like').replaceWith(response.code);
 }
 });

});

$('#wrap').on('click', "#dislike", function(event)
{
event.preventDefault();
var id =$(this).prev('meta').data().postid;
var action =$(this).closest('p #dislike').attr('class');
var ur =("/home/vote/").concat(action,'/',id);
var ht = $(this).closest('p #dislike').html();
if (action=='social-dislike'){
$(this).closest('p #dislike').attr('class','social-undislike');
$(this).prevAll("button").first().attr('class','social-like');
}
else
{
$(this).closest('p #dislike').attr('class','social-dislike');
}
var out =$(this)
$.ajax(
 {
 url:ur,
 method:'get',
 success:function(response)
 {
  out.closest('p #dislike').replaceWith(response.code);
 }
 });

});

});
