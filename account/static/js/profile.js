$(document).ready(function()
{
$(".navbar-form").on('click','#search_button',function(event)
{
var csrf= $(this).siblings('div').find('input').attr('value');
var search_term=$(this).siblings('div').find('#socrates-search').val();
var da={search_query:search_term, csrfmiddlewaretoken: csrf};
var ur= '/account/searchsocrates/';
 if (search_term.trim() ==="")
    {alert('Empty search');
    return 0;
    }

$.ajax(
{
 url:ur,
 type:'POST',
 data:da,
 dataType:'json',
 success:function(response)
 {
 window.location.href= ur;
 }
});
});
});
