$(document).ready(function () {

	$(".cat-btn").click(function (event) {
		event.preventDefault();
		var selectedButton = $(this);
		var selectedCategory = selectedButton.data("category");
		$(".cat-btn").each(function () {
			var currentButton = $(this);
			if (
				currentButton.hasClass("btn-primary") &&
				currentButton.data("category") !== selectedCategory
			) {
				currentButton
					.removeClass("btn-primary")
					.addClass("btn-outline-primary")
					.text("Select");
			}
		});
		selectedButton
			.removeClass("btn-outline-primary")
			.addClass("btn-primary")
			.text("Selected");
		$("#category").val(selectedCategory);
	});

	$("#eventform").submit(function (event) {
		event.preventDefault();
		if ($("#category").val()) {
			var formData = new FormData($(this)[0]);
			var actionUrl = $(this).attr("action");
			var fMethod = $(this).attr("method");
			clearForm();
			submitForm("eventform", formData, actionUrl+`?category=${$("#category").val()}`, fMethod);
		} else {
			createToast(
				"Error",
				"Please pick a category to proceed",
				"warning"
			);
		}
	});

	$("#categoryform").submit(function (event) {
		event.preventDefault();
		var formData = new FormData($(this)[0]);
		var actionUrl = $(this).attr("action");
		var fMethod = $(this).attr("method");
		clearForm();
		submitForm("categoryform", formData, actionUrl, fMethod);
	});
});

function clearForm() {
	var formErrors = document.querySelectorAll(".invalid-feedback");
	formErrors.forEach((element) => {
		element.remove();
	});
}
function submitForm(currId, formData, actionUrl, fMethod) {
	$.ajax({
		type: fMethod,
		url: actionUrl,
		data: formData,
		contentType: false,
		processData: false,
		success: function (response) {
			if (response.status == "error") {
				for (var key in response.errors) {
					if (currId === "eventform") {
						if (key === "__all__") {
							createToast(
								"Error",
								response.errors[key],
								response.status
							);
						} else {
							var input = $("#event_" + key);
							input.addClass("is-invalid");
							input.after(
								"<div class='invalid-feedback'>" +
									response.errors[key] +
									"</div>"
							);
						}
					} else if (currId === "categoryform") {
						if (key === "__all__") {
							createToast(
								"Error",
								response.errors[key],
								response.status
							);
						} else {
							var input = $("#category_" + key);
							input.addClass("is-invalid");
							input.after(
								"<div class='invalid-feedback'>" +
									response.errors[key] +
									"</div>"
							);
						}
					}
				}
			} else if (response.status == "success") {
				if (currId === "categoryform") {
					createToast(
						"Success",
						"Category added successfully",
						response.status
					);
					window.location.reload();
				} else {
					createToast(
						"Success",
						"Event has been added successfully",
						response.status
					);
					redirectTo(response.url);
				}
			} else {
				createToast(
					"Error",
					"Something went wrong, please try again",
					"warning"
				);
			}
		},
		error: function (error) {
			createToast(
				"Error",
				"Something went wrong, please try again",
				"warning"
			);
		},
	});
}

function createToast(heading, text, icon) {
	$.toast({
		text: text,
		heading: heading,
		showHideTransition: "slide",
		icon: icon,
	});
}

function redirectTo(url) {
	setTimeout(() => (window.location.href = url), 3000);
}
