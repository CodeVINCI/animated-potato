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

});
