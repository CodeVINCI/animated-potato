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

$('.box').on('click', "button.social-like", function(event)
{
event.preventDefault();
var id =$(this).next('meta').data().postid;
var ur =("/post/like/").concat(id);
alert(ur);
});

$('.box').on('click', "button.social-dislike", function(event)
{
event.preventDefault();
var id =$(this).prev('meta').data().postid;
var ur =("/post/dislike/").concat(id);
alert(ur);
});
});
