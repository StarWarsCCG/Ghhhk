$(document).ready(function() {
    $("#card-title-search-button").click(function(e) {
        e.preventDefault();
        $.getJSON(
            "fake_search2.json",
            null,
            function(json) {
                $('#card-search-results').empty();
                
                for (var key in json) {
                    if (json.hasOwnProperty(key)) {
                        $('#card-search-results:last-child').append(
                            '<tr><td>' + key + '</td><td>' + json[key] + '</td></tr>');
                    }
                }
            });
    });
});

