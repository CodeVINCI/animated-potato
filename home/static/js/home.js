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
