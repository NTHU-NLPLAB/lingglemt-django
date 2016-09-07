var timeoutId = '';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    // set up ajax csrf-token
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrftoken }
    });

    $('#search_input').on('input', function() {
        var query = this.value.trim();
        if (query !== '') {
            resetAutoSearchTimer(1000, query);
        }
    });
    $('.ui.dropdown').dropdown();
});

function resetAutoSearchTimer(ms, query) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function() {
        $('#search_bar').addClass("loading");
        $.ajax({
            url: '/translate',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'text': query}),
            dataType: 'json',
        }).done(renderTranslationResult);
    }, ms);
};

function renderTranslationResult(data) {
    console.log(data);
    htmlFrag = '';
    for(type in data) {
        htmlFrag += '<tr><td>' + escapeHtml(data[type]) + '</td><td>' + escapeHtml(type) + '</td></tr>';
    }
    $('tbody#search-result').html(htmlFrag);
    $('#search_bar').removeClass("loading");
};
