(function ($) {
    $(document).ready(function () {
        $('.place-autocomplete').on('input', function () {
            var query = $(this).val();
            $.get('/place/place-autocomplete/', { query: query }, function (data) {
                var resultsDiv = $('#place-autocomplete-results');
                resultsDiv.empty();
                console.log(data['results'])
                data.results.forEach(function (result) {
                    console.log(result)
                    resultsDiv.append('<div><a href="#" data-id="' + result.id + '">' + result.place_name + '</a></div>');
                });
            });
        });

        $('#place-autocomplete-results').on('click', 'a', function (e) {
            e.preventDefault();
            var placeId = $(this).data('id');
            var placeName = $(this).text();
            $('.place-autocomplete').val(placeName);
            $('#id_place').val(placeId);
        });
    });
})(django.jQuery);
