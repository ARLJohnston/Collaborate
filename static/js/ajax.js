$(document).ready(function() {
	$('#like_btn').click(function() {
		var catepageIdVar;
		catepageIdVar = $(this).attr('data-pageid');

		$.get('/rango/like_page/',
			{'page_id': catepageIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
				})
	});
});
