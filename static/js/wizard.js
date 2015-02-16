"use strict";
$(document).ready(function() {
    $(document).on('click', '.add-to-list', function(e) {
        var movie_id = $(this).data('movie-id');
        var status = $(this).data('status');
        var container = $(this).closest('div.movie-item');
        container.find('div.movie-actions').find('a').each(function() {
            $(this).attr('disabled', true);
        });
        var button = $(this);
        button.button('loading');
        $.ajax({
            type: 'POST',
            url: '/api/v1/add_to_list/' + movie_id + '/' + status + '/',
            success: function(data) {
                container.fadeOut(300, function() {
                    container.html('<div style="width: 50%; margin: 0 auto; margin-top: 12%;"><i class="icon-spinner icon-spin icon-large"></i> Loading another...</div>');
                    container.fadeIn(300, function() {
                        var shown_ids = $('.add-to-list.add-to-watched').map(function() { return $(this).data('movie-id'); }).get().join(',');
                        $.ajax({
                            type: 'POST',
                            url: '/api/v1/suggest_another_movie/' + movie_id + '/' + status + '/',
                            data: {
                                'shown_ids': shown_ids
                            },
                            success: function(data) {
                               container.html(data);
                            },
                            error: function(xhr) {
                                console.log(xhr.responseText);
                            }
                        });
                    });
                });
                button.button('reset');
            },
            error: function(data) {
                container.find('div.movie-actions a').each(function() {
                    $(this).attr('disabled', false);
                });
                button.button('reset');
            }
        });
        e.preventDefault();
        return false;
    });
});
