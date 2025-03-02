$(document).ready(function () {
    let ticket = $('input#text')
    let scanner = new Instascan.Scanner({
        video: document.getElementById("preview"),
    });
    Instascan.Camera.getCameras()
        .then(function (cameras) {
            if (cameras.length > 0) {
                scanner.start(cameras[0]);
            } else {
                alert("No cameras found");
            }
        })
        .catch(function (e) {
            console.error(e);
        });

    scanner.addListener("scan", function (c) {
        ticket.val(c);
        $('button#submit').trigger('click');
    });    
});
