$(document).ready(function() {
    $("#card-title-search-button").click(function(e) {
        e.preventDefault();
        $.getJSON(
            "fake_search2.json",
            null,
            function(json) {
                var result = "";
                
                for (var key in json) {
                    if (json.hasOwnProperty(key)) {
                        result += key + " -> " + json[key] + "\n";
                        $('#card-search-results:last-child').append(
                            '<tr><td>' + key + '</td><td>' + json[key] + '</td></tr>');
                    }
                }
            });
    });
});

