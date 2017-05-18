$(document).ready(function()
{

$('div.select_filters').on('click', ".btn.btn-secondary", function(event)
{
var target= document.getElementById("filters").value;
var ur = ("/home/politics/").concat(target);
alert(ur)

});

});
