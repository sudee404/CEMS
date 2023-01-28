$(document).ready(function () {
    var navbtn = $(".nav-link");
    var headline = $("#headline");
    navbtn.mouseenter(function () {
        $(this).addClass("text-warning");
        $(this).mouseleave(function () {
            $(this).removeClass("text-warning");
        });
    });
    
});
$(function () {
    $(".owl-carousel").owlCarousel({
        loop: true,
        rewind:true,
        dots: true,
        margin: 20,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1,
            },
            700: {
                items: 2,
            },
            1220: {
                items: 2,
            },
        },
    });
    var owl = $(".owl-carousel");
    owl.owlCarousel();
    // Go to the next item
    $(".owl-next").click(function () {
        owl.trigger("next.owl.carousel");
    });
    // Go to the previous item
    $(".owl-prev").click(function () {
        // With optional speed parameter
        // Parameters has to be in square bracket '[]'
        owl.trigger("prev.owl.carousel", [300]);
    });
    
});
