$(document).ready(function () {
	$(window).on("scroll", function () {
		if ($(window).scrollTop() > $("#cover").height()) {
			$("nav.navbar").css({
				"background-color": "white",
				"box-shadow": "4px 4px 4px #771414e1",
			});
		} else {
			$("nav.navbar").css({
				"background-color": "transparent",
				"box-shadow": "0 0 0 #771414e1",
			});
		}
	});

	const svg = document.querySelector(".scroll-down svg");

	svg.onmouseover = function () {
		svg.style.webkitFilter = "drop-shadow(0 0 5px #fff)";
		svg.style.filter = "drop-shadow(0 0 5px #fff)";
	};

	svg.onmouseout = function () {
		svg.style.webkitFilter = "none";
		svg.style.filter = "none";
	};
	$(".owl-carousel").owlCarousel({
		items: 3,
		loop: false,
		autoplay: true,
		autoplayTimeout: 6000,
		dots: true,
		nav: false,
		responsive: {
			0: {
				items: 1,
			},
			992: {
				items: 3,
			},
		},
	});
	
});
