/* Use this js doc for all application specific JS */



 // JavaScript Document for story.asp
/**
 * Make pull quotes
 */

function makePullquote() {
  var spans = document.getElementsByTagName('span');
  for (i = 0; i < spans.length; i++) {
    if (spans[i].className == "pullme") {
      var pullquote = document.createElement('blockquote');
      pullquote.innerHTML = spans[i].innerHTML;
      spans[i].parentNode.insertBefore(pullquote, null);
      spans[i].innerHTML = ""
    } else if (spans[i].className == "pullalt") {
      var pullquote = document.createElement('blockquotealt');
      pullquote.innerHTML = spans[i].innerHTML;
      spans[i].parentNode.insertBefore(pullquote, null);
      spans[i].innerHTML = ""
    }
  }
}

if ((typeof jQuery) === 'undefined') { // in case something went wrong with jQuery,
  window.onload = makePullquote; // go oldschool
} else { // jQuery is good to go
  jQuery(function($) { // on document ready

    // call makePullquote from above
    makePullquote();

    /**
     * FancyBox
     *
     * All links with class 'lightbox' will open a lightbox when clicked,
     * with a caption grabbed from the link's 'title' attribute.
     * By default, this script groups all lightbox links together in a gallery
     * (meaning you can click the lightbox to see the 'next' and 'previous'
     * images). To prevent this behavior, specify a 'rel' attribute for <a>
     * tags that should be grouped separately.
     */

    $('a.lightbox').attr('rel', function() {
      if ((typeof $(this).attr('rel')) === 'undefined') { // no rel attribute?
        return 'gallery-default'; // give it a default rel
      } // otherwise keep the given rel
    }).fancybox({ // lightbox-ize all links with class 'lightbox'
      'titlePosition': 'inside',
      // simplest-looking caption style
      'hideOnContentClick': true,
      // clicking on the image closes the lightbox
      'showCloseButton': false,
      // not necessary with hideOnContentClick
      'speedIn': 200,
      // speed up the fade animations a little bit
      'speedOut': 200
    });

    /**
     * Crop photos vertically from center
     *
     * As of 11 July 2011, scaled images in a div#PhotoCrop have their top 18px
     * cut off, and a maximum of 270px below that is shown. This is all well
     * and good for photos that are 306px tall, but what about other sizes?
     * This script tries to ensure that an equal amount is trimmed off the top
     * and bottom of the photo.
     */

    $('#PhotoCrop img').load(function() {
      var $this = $(this);
      $this.css('margin-top', 0) // reset first before calculating height
      .css('margin-top', function() {
        return Math.floor(-0.5 * ($this.height() - $this.parent().innerHeight()));
      });
    }).each(function() {
      if (this.complete || this.complete == undefined) {
        // If the image is in cache, the 'load' event may never fire.
        // Changing the src attribute to a blank data URL and back forces it to.
        // Thanks to Paul Irish: https://gist.github.com/268257
        var src = this.src;
        this.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        this.src = src;
      }
    });
  });
}


$(function () {
  $('#myTab a:first').tab('show');
})
  
  
$(document).ready(function(){

  $(".simplenav>ul>li>a").bind("mouseenter",function(){
    hideAllNav();
    showChildNav(this);
  });
  
  $(".simplenav").bind("mouseleave",function(){
    hideAllNav();
    showCurrentNav();
  });

});

function hideAllNav(menu){
  $(".simplenav ul ul").removeClass("on fix");
  $(".simplenav ul ul").addClass("off");
}

function showChildNav(actOnMe){
  $(".simplenav li").removeClass("MenuVisible");
  $(actOnMe).parent("li").find("ul").removeClass("off");
  $(actOnMe).parent("li").find("ul").addClass("on fix");
  $(actOnMe).parent("li").not($("li.here")).find("ul").bind("mouseenter",function(){
    $(this).parent("li").addClass("MenuVisible");
    
  }).bind("mouseleave",function(){
    $(this).parent("li").removeClass("MenuVisible");
  });
}

function showCurrentNav(){
  //only do this if it is currently hidden
  if($(".simplenav li.here ul").hasClass("off")){
    $(".simplenav li.here ul").removeClass("off");
    $(".simplenav li.here ul").addClass("on fix");
  }
}

    
function tick(){
  $('#ticker li:first').slideUp( function () { $(this).appendTo($('#ticker')).slideDown(); });
}
setInterval(function(){ tick () }, 6000);
setInterval(function(){ cycle () }, 15000);


$(function (){ 
  $("#example").popover();  
});  
   
   
$(function() {

  $('.impressions').height($('.impressions').height());
  var hidden = $('.impressions-head h5, .vids').hide();
  var loading = $('<p>').text('Loading. Please wait...').appendTo('.impressions-head');

  $('.vid').fancybox({
  width: 720,
  height: 405,
  overlayColor: '#000',
  overlayOpacity: 0.3,
  titleShow: false,
  type: 'swf',
  speedIn: 200,
  speedOut: 200,
  onStart: function(selectedArray, selectedIndex, selectedOpts) { // whenever a lightbox is opened
    if('object' === typeof _gaq) { // Google Analytics has been loaded
    _gaq.push(['_trackEvent', 'Videos', 'Play', $(selectedArray[0]).attr('title')]);
    }
  }
  });
  
  loading.fadeOut(400, function() {
  $(this).remove();
  hidden.fadeIn(400);
  });

});


$(document).ready(function() {
    $('.carousel').carousel({interval: 15000});
  });