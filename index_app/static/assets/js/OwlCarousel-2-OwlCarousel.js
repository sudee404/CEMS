$(function () {
	var owl = $(".owl-carousel"),
		owlOptions = {
			autoplay: true,
			lazyLoad: true,
			loop: false,
			margin: 20,
			/*
            animateOut: 'fadeOut',
            animateIn: 'fadeIn',
            */
			responsiveClass: true,
			autoHeight: true,
			autoplayTimeout: 7000,
			smartSpeed: 800,
			nav: false,
			responsive: {
				0: {
					items: 1,
				},

				600: {
					items: 2,
				},

				1024: {
					items: 3,
				},

				1366: {
					items: 3,
				},
			},
		};

	var owlActive = owl.owlCarousel(owlOptions);

	$(window).resize(function () {
		if ($(".owl-carousel").hasClass("off")) {
			var owlActive = owl.owlCarousel(owlOptions);
			owl.removeClass("off");
		}
	});
});
