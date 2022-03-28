$(document).ready(function() {
	$('#like_btn').click(function() {
		var catepageIdVar;
		catepageIdVar = $(this).attr('data-pageid');

		$.get('/collab_app/like_page/',
			{'page_id': catepageIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
				})
	});
});

$(document).ready(function() {
	$('#like_btn_comment').click(function() {
		var catecommentIdVar;
		catecommentIdVar = $(this).attr('data-commentid');

		$.get('/collab_app/like_comment/',
			{'comment_id': catecommentIdVar},
			function(data) {
				$('#comment_like_count').html(data);
				$('#comment_like_btn').hide();
				})
	});
});
