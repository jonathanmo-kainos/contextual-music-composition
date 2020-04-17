// Generate Music Button Activate
function fadeControlsIn() {
	var homeToMain = new TimelineMax({});

	$('.wrapper').removeClass('translucent')
	$('#spinner').addClass('invisible');
	$(":input").attr("disabled", false);

	// Hide
	homeToMain.to($('.text-wrap'), 1, {yPercent: -30, ease: Power2.easeInOut}, 0),

	// Background down
	homeToMain.to($('.wave-container'), 1, {yPercent: 40, ease: Power2.easeInOut}, 0)

	// Show controls
	homeToMain.fromTo($('#controls'), 0.8, {opacity: 0, yPercent: 10, display: 'none', x: 0},
										{opacity: 1, x: 0, yPercent: 0, display: 'flex', ease: Power2.easeInOut}, 1)
}

function fadeControlsOut() {
	$('.wrapper').addClass('translucent');
	$('#spinner').removeClass('invisible');
	$(":input").attr("disabled", true);
}

// Dropdown Menu Fade
jQuery(document).ready(function() {
    $(".dropdown").hover(
        function() { $('.dropdown-menu', this).fadeIn("fast");
        },
        function() { $('.dropdown-menu', this).fadeOut("fast");
    });
});