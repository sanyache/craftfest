/* ==========================================================================
   Dropdown Menus
   ========================================================================== */
  $(".dropdown").hover(
    function () {
      $(this).addClass('open');
    }, 
    function () {
      $(this).removeClass('open');
    }
  );

  /* $('.navbar-right').click(function(e){
    e.preventDefault();
    parentLi = e.target.parentElement;
    var menuList = this.querySelectorAll('ul > li');
    menuList.forEach(el => {
      if(el === parentLi) { 
        el.classList.add('active');
      }
      if(el.classList.contains('active') && el !== parentLi) {
        el.classList.remove('active');
      }
    });
    window.location.href = e.target;
  }); */

  jQuery(function($) {
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $('.navbar ul li a').each(function() {
     if (this.href === path) {
      $(this).closest('li').addClass('active');
     }
    });
  });
/* ==========================================================================
   countdown timer
   ========================================================================== */
 jQuery('#clock').countdown($('.time-count').data('time'),function(event){
  var $this=jQuery(this).html(event.strftime(''
  +'<div class="time-entry days"><span>%-D</span> Days</div> '
  +'<div class="time-entry hours"><span>%H</span> Hours</div> '
  +'<div class="time-entry minutes"><span>%M</span> Minutes</div> '
  +'<div class="time-entry seconds"><span>%S</span> Seconds</div> '));
});

/* ==========================================================================
   WOW Scroll Spy
   ========================================================================== */
   var wow = new WOW({
    //disabled for mobile
	    mobile: false
	});
	wow.init();

/* ==========================================================================
   Nivo Lightbox
   ========================================================================== */
   $('.lightbox').nivoLightbox({
    effect: 'fadeScale',
    keyboardNav: true,
    errorMessage: 'The requested content cannot be loaded. Please try again later.'
  });

/* ==========================================================================
   Contact From
   ========================================================================== */	
	
	$('.input').blur(function(){
	    if( $(this).val() ) {
	        $(this).parent('.label-line').addClass('active checked');
	    } else {
		    $(this).parent('.label-line').removeClass('active checked');
	    }
	});

	$('.label-line').click(function(){
		$(this).addClass('active');
		if ($('.label-line').hasClass('checked')){}
		else{
			$('.label-line').removeClass('checked');
		}
	});	

/* ==========================================================================
   Back Top Link
   ========================================================================== */
  var offset = 200;
  var duration = 500;
  $(window).scroll(function() {
    if ($(this).scrollTop() > offset) {
      $('.back-to-top').fadeIn(400);
    } else {
      $('.back-to-top').fadeOut(400);
    }
  });
  $('.back-to-top').click(function(event) {
    event.preventDefault();
    $('html, body').animate({
      scrollTop: 0
    }, 600);
    return false;
  })

   // Projects Carousel
  $("#post-carousel").owlCarousel({
    navigation : false,
    pagination: true,
    slideSpeed : 400,
    stopOnHover: true,
    autoPlay: 3000,
    items :1,
  });
/* ==========================================================================
   Slick Nav 
   ========================================================================== */
    $('.wpb-mobile-menu').slicknav({
      prependTo: '.navbar-header',
      parentTag: 'span',
      allowParentLinks: true,
      duplicate: false,
      label: '',
      closedSymbol: '<i class="fa fa-angle-right"></i>',
      openedSymbol: '<i class="fa fa-angle-down"></i>',
    });
/* ==========================================================================
   Shedule
   ========================================================================== */
    $(document).on('click','.schedule li a', function(e){
      e.preventDefault();
      var days = document.getElementsByClassName('tab-pane');
      [...days].forEach(element => {
        if (element.classList.contains('active')) {
          element.classList.remove('active');
        }
      });
      var idDay = $(this).attr("href");
      var day = document.getElementById(idDay);
      day.classList.add('active');
  });
  

    $(document).on('click','a.next',function(event){
        event.preventDefault();
        var link = location.href;
        var num_pages = $('#time').data('pages');
        var page = $('#time').data('page');
        page += 1;
        if( page <= num_pages){
            link =  link+"?page="+ page;
                $.ajax({
                'url': link,
                'dataType': 'html',
                'type': 'get',
                'success': function(data, status, xhr){ 
                    html = $(data).find('.items');
                    $('.pages').html(html);
                
                }
            });
        } 
    });

    $(document).on('click','a.previous',function(event){
      event.preventDefault();
      var link = location.href;
      var num_pages = $('#time').data('pages');
      var page = $('#time').data('page');
      page -= 1;
      if( page >= 1){
          link =  link+"?page="+ page;
              $.ajax({
              'url': link,
              'dataType': 'html',
              'type': 'get',
              'success': function(data, status, xhr){ 
                  html = $(data).find('.items');
                  $('.pages').html(html);
              
              }
          });
      } 
  });
  $(document).on('click', 'a.load-more',function(event){
    event.preventDefault();
    var link = location.href;
    var num_pages = $('#load-more').data('pages');
    var page = $('#load-more').data('page');
    page += 1;
    $('#load-more').data('page', page);
    if( page <= num_pages){
        link =  link+"?page="+ page;
            $.ajax({
            'url': link,
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){ 
                html = $(data).find('.items');
                $('.pages').append(html);
            
            }
        });
    }
    if( page == num_pages ){
      $(this).hide();
  }
});
$(document).on('click', 'a.load-more-product',function(event){
  event.preventDefault();
  var category = $('#category').data('category');
  var link = '/product_by_category/' + category + '?page=';
  var num_pages = $('#load-more-product').data('pages');
  var page = $('#load-more-product').data('page');
  page += 1;
  $('#load-more-product').data('page', page);
  if( page <= num_pages){
      link =  link+ page;
          $.ajax({
          'url': link,
          'dataType': 'json',
          'type': 'get',
          'success': function(data, status, xhr){ 
              html = $(data.html_form).find('.card');
              $('.items').append(html);
          
          }
      });
  }
  if( page == num_pages ){
    $(this).hide();
}
});
$(document).on('click', 'a.load-page', function(event){
  event.preventDefault();
  var link = $(this).attr('href');
  $.ajax({
    'url': link,
    'dataType': 'json',
    'type': 'get',
    'success': function(data, status, xhr){
      $('#product_list').html(data.html_form);  
    }
  });
});

    