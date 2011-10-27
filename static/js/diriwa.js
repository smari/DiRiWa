

$(function() {
	$(".lexp").delay(1500).animate({width:43}, 1500);
});

$(window).unload(function() {
	$(".lexp").animate({width:0}, 500);
});