$(document).ready(function()
{
var valnow=$('#my-data').data().source;

$(function() {
    $("#subscriptions").val(valnow);
});

$('div.select-newspaper').on('click', ".btn.btn-secondary", function(event)
{
var target= document.getElementById("subscriptions").value;
var ur = ("/account/newspapers/").concat(target);
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

});
