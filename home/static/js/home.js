$(document).ready(function()
{
var valnow=$('#my-data').data().filter;
$(function() {
    $("#filters").val(valnow);
});
$('div.select_filters').on('click', ".btn.btn-secondary", function(event)
{
var target= document.getElementById("filters").value;
var ur = ("/home/").concat(target);
window.location.href = ur;

});

});
