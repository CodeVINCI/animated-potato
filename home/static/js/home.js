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

$('#wrap').on('click', "button.social-like", function(event)
{
event.preventDefault();
var id =$(this).next('meta').data().postid;
var ur =("/post/like/").concat(id);
alert(ur);
});

$('#wrap').on('click', "button.social-dislike", function(event)
{
event.preventDefault();
var id =$(this).prev('meta').data().postid;
var ur =("/post/dislike/").concat(id);
alert(ur);
});

});
