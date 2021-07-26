$(document).ready(function() {

    $("#country-select").on("change", function() {

        $.ajax({
            url: '',
            type: 'get',
            data: {
                country_choice: $(this).val(),
            },
            success: function(response) {
                var region_select = $("#region-select");
                region_select.empty();


                $("#city-select").empty();
                $("#city-select").append('<option disabled selected value> -- select an option -- </option>');

                region_select.append('<option disabled selected value> -- select an option -- </option>');

                for (var i = 0; i < response.regions.length; i++) {
                    region_select.append('<option value="' + response.regions[i] + '">' + response.regions[i] + '</option>')
                }
            }
        });
    });


    $("#region-select").on("change", function() {
        $.ajax({
            url: '',
            type: 'get',
            data: {
                region_choice: $(this).val(),
            },
            success: function(response) {
                var city_select = $("#city-select");
                city_select.empty();

                city_select.append('<option disabled selected value> -- select an option -- </option>');

                for (var i = 0; i < response.cities.length; i++) {
                    city_select.append('<option value="' + response.cities[i] + '">' + response.cities[i] + '</option>')
                }
            }
        });
    });

});