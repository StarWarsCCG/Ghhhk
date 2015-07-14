function doSearch() {
    $.getJSON(
        "/api/cards/search",
        {"title":$("#card-title-search").val()},
        function(json) {
            $('#card-search-results').empty();
            
            for (var key in json) {
                if (json.hasOwnProperty(key)) {
                    $('#card-search-results:last-child').append(
                        '<tr><td>' + key + '</td><td>' + json[key] + '</td><td></td></tr>');
                }
            }
        });
}

$(document).ready(function() {
    $("#card-title-search-button").click(function(e) {
        e.preventDefault();
        doSearch();
    });
    
    $("#card-title-search").keydown(function(e) {
        if (e.keyCode == 13) {
            doSearch();
        }
    });
});

