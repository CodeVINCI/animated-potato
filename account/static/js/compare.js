$(document).ready(function()
{

$('.carousel').carousel({ interval: 5000 });

$(document).on('click','.comparetitle',function(event)
{
var target = $($(this).attr('data-target'));

var imgbox = target.find('.imgbox');
var da = target.find('.conatiner');
var urllist = [da.attr('data-img1'),da.attr('data-img2'),da.attr('data-img3')];



});

});
