$(document).ready(function()
{

$('.carousel').carousel({ interval: 5000 });


$(document).delegate('.comment_box','keypress',function(e){
    if(e.which === 13){
    //alert($(this).siblings('#comment_button').html());
        $(this).siblings("#comment_button").click();
        return false;
    }
});

$(document).on('click','#comment_button', function(event){
    event.preventDefault();
     var id = $(this).prev('meta').data().pk// sanity check
    // AJAX for posting
    var ur = ('/home/make_compare_comment/').concat(id,'/');
    var ht = $(this).siblings('#post-comment').val();
    var csrf=$(this).siblings('#post-comment').prev('input').attr('value');
    var out=$(this);
    var da={the_post:ht, pk:id, csrfmiddlewaretoken: csrf};

    if (ht.trim() ==="")
    {alert('Comment is empty');
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
       out.siblings('#post-comment').val('');
       out.parent().next("#talk").prepend(response.text);
      }
    });

});


//javascript for comment delete button
$(document).on('click','.comment_delete',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/remove_compare_comment/".concat(id);
var out = $(this)
$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
var li = out.closest('li');
li.fadeOut('slow', function() { li.remove(); });
}
});
return false;
});

$(document).on('click', '#suggestbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/suggestion_compare/').concat(id);
$.get(ur);
alert("This article has been suggested to your friends");
return false;
});

$(document).on('click', '.notify' ,function(event){
var notificationid = $(this).attr("data");
var ur= "/home/seennotification/".concat(notificationid);
var out = $(this)

$.ajax(
{
url:ur,
method:'get',
async: false,
});

});



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



});
