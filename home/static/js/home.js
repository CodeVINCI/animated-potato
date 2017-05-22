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
$.get(ur)
return true;
});

});
