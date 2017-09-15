
$(document).ready(function()
{

$('#socrates-search').keypress(function(e){
    if(e.which === 13){
        $("#searchsubmit").click();
        return false;
    }
});

$(".navbar-form").on('click','#searchsubmit',function(event)
{
var search_term=$(this).siblings('div').find('#socrates-search').val();
var ur= ("/account/searchsocrates/").concat(search_term);
 if (search_term.trim() ==="")
    {alert('Empty search');
    return false;
    }
 window.location.href= ur;
 return false;
});

$(document).on('click', '#deactivate' ,function(event){
var r = confirm("Are you sure you want to deactivate account");
if (r == true) {
var ur= '/account/deactivate/';
$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
window.location.href="/account/signup"
}
});
}
});

});
