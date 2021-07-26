$(document).ready(function() {

    $("#input-profile-picture").on("change", function() {
        console.log("Da");
        var form = $("#picture-change-form");
        form.append(this);
        form.submit();
    })
});