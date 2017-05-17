/*$('#post-form').on('submit', function(event){
     event.preventDefault();
     console.log("form submitted!")
     create_post();
});
function create_post(){
  console.log("create post is working!")
  $.ajax({
      url : "create_post/",
      type : "POST",
      data :{ the_post :$('#post-text').val()},

      success : function(json) {
         $('#post-text').val('');
         console.log(json);
         console.log("success");
      },
      error : function(xhr,errmsg,err){
         $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
         console.log(xhr.status +": "+xhr.responseTest);
      }

  });
};
*/


/*$('#like').click(function(){
     $.ajax({
               type:"POST",
               url: "{% url 'like' %}",
               data: {'slug':$(this).attr('name'),'csrfmiddlewaretoken':'{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                   alert(response.message);
                   alert('Post likes count is now' + response.likes_count);
               },
               error: function(rs, e){
                  alert(rs.responseText);
               }
     });*/

$(document).ready(function(){
    $('form').submit(function(event){
       event.preventDefault();
       $.ajax({
          url:'/create_comment',
          method:'post'
          data:$(this).serialize(),
          success:function(response){
              console.log(response);
          }
       })
    })

 })












