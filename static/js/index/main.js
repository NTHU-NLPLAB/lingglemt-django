var timeoutId = '';
var trans_socket;
var default_sent = 'Some packed food we considered safe may contain ingredients harmful to humans.'

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

    $('.ui.dropdown').dropdown();

    $('#trans_menu > a.item').on('click', function() {
        $(this).addClass('active').siblings().removeClass('active');
        var option = $(this).text().toLowerCase();
        $('#result_area .result[alt="' + option + '"]').addClass('active').siblings('.result').removeClass('active');
    });

    init_trans_socket();

    timeoutId = setTimeout(function() {
        $('#search_input').val(default_sent).select();
    }, 1000);

});

function init_trans_socket() {
      // init translation socket
      trans_socket = new WebSocket("ws://" + window.location.host + "/translate/");
      trans_socket.onmessage = function(message) {
          data = JSON.parse(message.data);
          if(data.type == 'status') {
              console.log('status: '+data.content);
              $('#result_area div.ui.text.loader').text(data.content);
          } else if(data.type == 'result') {
              renderTranslationResult(data.content);
              var option = $('#trans_menu .item.active').text().toLowerCase();
              $('#result_area .result[alt="' + option + '"]').addClass('active').siblings('.result').removeClass('active');
          }
      }
      trans_socket.onopen = function(message) {
          search();
          $('#search_input').on('input', function() {
              $('#search_bar').addClass('loading');
              $('#result_area > div.ui.dimmer').addClass('active')
                .children('.loader').addClass('indeterminate').text('Waiting user input...');
              clearTimeout(timeoutId);
              timeoutId = setTimeout(search, 1000);
          });
      }
      trans_socket.onclose = function(message) {
          setTimeout(function(){init_trans_socket();}, 5000);
      }
}

function search() {
    var query = $('#search_input').val().trim();
    if (query !== '') {
        $('#result_area > div.ui.dimmer').addClass('active')
          .children('.loader').removeClass('indeterminate').text('Sending translation request...');
        // $('#result_area').addClass("loading");
        trans_socket.send(JSON.stringify({'text': query}));
    }
    // $.ajax({
    //     url: '/translate',
    //     type: 'POST',
    //     contentType: "application/json; charset=utf-8",
    //     data: JSON.stringify({'text': query}),
    //     dataType: 'json',
    // }).done(renderTranslationResult);
}

function renderTranslationResult(data) {
    console.log(data);
    $('#result_area .result').each(function() {
        type = $(this).attr('alt');
        $(this).text(data[type]);
    });
    // htmlFrag = '';
    // for(type in data) {
    //     htmlFrag += '<tr><td>' + escapeHtml(data[type]) + '</td><td>' + escapeHtml(type) + '</td></tr>';
    // }
    // $('tbody#search-result').html(htmlFrag);
    $('#search_bar').removeClass("loading");
    $('#result_area > div.ui.dimmer').removeClass("active");
    // $('#result_area').removeClass("loading");
};
