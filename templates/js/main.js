$(".upvote, .downvote").click(function() {
        var entry_id = $(this).attr('id');
        var entry = $(this);
        var vote_type = $(this).attr('class');

        if (entry.hasClass('selected')){
            <!--oyu geri alma işlemi-->
            $.post('http://localhost:8000/ajax/',{
                csrfmiddlewaretoken: '{{ csrf_token }}',
                entry_id:entry_id,
                vote_action: 'return',
                vote_type: vote_type
                    },
                    function(data){
                        entry.removeClass('selected');
                        entry.html(data);

            });
        } else {
            $.post('http://localhost:8000/ajax/',{
                csrfmiddlewaretoken: '{{ csrf_token }}',
                entry_id:entry_id,
                vote_action: 'vote',
                vote_type: vote_type
                    },
                    function(data){
                        entry.addClass('selected');
                        entry.html(data);



            })
        }
    });