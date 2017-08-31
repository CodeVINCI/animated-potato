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
 window.location.href = ur;
 return false;
});


$(document).on('click', "#readlater", function(event)
{
var id=$(this).parent().prev('p').attr('id');
var ur = ('/account/save/readlater/').concat(id);
$.ajax(
{
url:ur,
method:'get',
success:function(response)
{
 alert('Post is saved to your library');
}
});
});

//social like a post ajax request
$(document).on('click', "#like", function(event)
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

//social dislike a post ajax request
$(document).on('click', "#dislike", function(event)
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


//visit site counter ajax request
 $(document).on('click', '#visitbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/visitors/').concat(id);
$.get(ur);
return true;
});

//suggestions counter and generate suggest notification ajax request
$(document).on('click', '#suggestbutton', function(event)
{
var id=$(this).parent('p').attr('id');
var ur = ('/home/suggestion/').concat(id);
$.get(ur);
alert("This article has been suggested to your friends");
return false;
});

/*showing url on opening the modal*/
  //$(window.location.hash).modal('show');
 /*  $('#wrap').on('click', 'a[data-toggle="modal"]' ,function(event){
        window.location.hash = $(this).attr('data');
      var m = $(this).parent('p').nextAll('.modal').first().attr('id');
      m = ('#').concat(m);
      $(m).modal('show');
      //$(window.location.hash).modal('show');
        return false;
    });
    //m.modal('show');
    //$(window.location.hash).modal('show');

    function revertToOriginalURL() {
        var original = window.location.href.substr(0, window.location.href.indexOf('#'))
        history.replaceState({}, document.title, original);
    }

    $('#wrap').on('hidden.bs.modal','.modal', function () {
        revertToOriginalURL();
    });*/

/*handling comment form submission*/
$('#wrap').on('click','#comment_button', function(event){
    event.preventDefault();
    console.log("form submitted!")
     var id = $(this).prev('meta').data().pk// sanity check
    // AJAX for posting
    var ur = ('/home/make_comment/').concat(id,'/');
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

$("#post-comment").keyup(function(event){
    if(event.keyCode == 13){
        $("#comment_button").click();
    }
});


//javascript for comment delete button
$('#wrap').on('click','.comment_delete',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/remove_comment/".concat(id);
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

//javascript for comment like button
$('#wrap').on('click','.comment_like',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/like_comment/".concat(id);
var out = $(this);
alert(ur);
return false;
});

//javascript for comment reply button
$('#wrap').on('click','.comment_reply',function(event)
{
var id= $(this).attr('data-pk');
var ur= "/home/reply_comment/".concat(id);
var out = $(this);
alert(ur);
return false;
});

$('#wrap').on('click','#newcomparesave',function(event)
{
var title= $('#id_title').val();
var description = $('#id_description').val();
var id = $('#selectedpost').attr('data-pk')
var replace = '<a id="addpost" style="cursor:pointer;text-decoration:none;" data=""><p><span class="glyphicon glyphicon-grain"></span>&nbsp;'.concat(title,'<span style="float:right;">1</span></p></a>');
$.ajax(
{
url:'/account/newcompare',
method:'get',
data:{title:title,description:description,post:id},
dataType:'json',
success:function(response)
{
$('#oldcompare').prepend(replace);
$('#oldcompare').children('a[data=""]').attr('data',response.data);
}
});

});

$(document).on('click','#addtocompare',function(event)
{
var url = window.location.href;
var id = url.substring(url.lastIndexOf('/') + 1);
$('#selectedpost').attr('data-pk',id);

});

$('#wrap').on('click','#addpost',function(event)
{
alert('about to add');
var id = $('#selectedpost').attr('data-pk');
var comp = $(this).attr('data');
var out = $(this)
var count = $(this).find('span[style="float:right;"]').html();

if (count < 3)
{
$.ajax(
{
url:'/account/addposttocompare',
method:'get',
data:{compare:comp,post:id},
dataType:'json',
success:function(response)
{
out.find('span[style="float:right;"]').html(response.count);
}
});
}
else
{
alert('Max 3 can be added to any compare');
}

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


//final paranthesis
});

