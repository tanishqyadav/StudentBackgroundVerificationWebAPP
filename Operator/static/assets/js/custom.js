(function($) {
    var defaults={
        sm : 540,
        md : 720,
        lg : 960,
        xl : 1140,
        navbar_expand: 'lg',
        animation: true,
        animateIn: 'fadeIn',
    };
    $.fn.bootnavbar = function(options) {

        var screen_width = $(document).width();
        settings = $.extend(defaults, options);

        if(screen_width >= settings.lg){
            $(this).find('.dropdown').hover(function() {
                $(this).addClass('show');
                $(this).find('.dropdown-menu').first().addClass('show');
                if(settings.animation){
                    $(this).find('.dropdown-menu').first().addClass('animated ' + settings.animateIn);
                }
            }, function() {
                $(this).removeClass('show');
                $(this).find('.dropdown-menu').first().removeClass('show');
            });
        }

        $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
          if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
          }
          var $subMenu = $(this).next(".dropdown-menu");
          $subMenu.toggleClass('show');

          $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
            $('.dropdown-submenu .show').removeClass("show");
          });

          return false;
        });
    };
})(jQuery);
        $(function () {
  $('#main_navbar').bootnavbar();
})
$(function() {
    $("#mud").DataTable({
        "responsive": true,
        "lengthChange": false,
        "autoWidth": false,
        "scrollX": true,
        "buttons": ["csv", "print"]
    }).buttons().container().appendTo('#mud_wrapper .col-md-6:eq(0)');
    $('#mud1').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
    });
});


// hide and show data button
var dglow=document.getElementById("dglow");

function myFunction(){
    var style=dglow.style.display;
        if(style=='block')
        	{
            dglow.style.display='none';
        	}
    	else{
            dglow.style.display='block';
        	}    			
    }


    $(document).ready(function() {
        $("#button2").click(function() {
            $("#sNames").attr('disabled', !$("#sNames").attr('enabled'));
        });
    
    });


    $(document).ready(function() {
        $("#button1").click(function() {
            $("#sName").attr('disabled', !$("#sName").attr('enabled'));
        });
    
    });

    $("#btnShow").click(function() {

        $(".alert").hide().show('medium');
    });
    // Data Picker Initialization
$('#inputDate').datepicker({});