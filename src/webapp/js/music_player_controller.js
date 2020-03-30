$(document).ready(function() {
    MIDIjs.initAll();
});

var userInput = '';
var instrumentNumber = 0;
var displaySheetMusic = false;
var noteDensity = 99.9;
var tempo = 1;
var sliderValues = [];

$('#generate-button').one('click', function() {
	userInput = $('#user-input').val();

	console.log('userInput: ', userInput);

    $.get('/generateRandomMusic', {userInput: userInput}, function(data) {
        console.log('data: ', data);
        setSliderValues(data);

		MIDIjs.play('../outputs/live/livesong.mid');
    });
    $('#generate-button').prop('id', 'generate-button-clicked');
    return false;
});

$(document).on('click', '#generate-button-clicked', function() {
	userInput = $('#user-input').val();
	noteDensity = $('#density-slider').val();
	tempo = $('#tempo-slider').val();
	displaySheetMusic = $('#music-display-toggle').is(":checked");
	sliderValues = getSliderValues();

	console.log('userInput: ', userInput);
	console.log('instrumentNumber: ', instrumentNumber);
	console.log('displaySheetMusic: ', displaySheetMusic);
	console.log('noteDensity: ', noteDensity);
	console.log('tempo: ', tempo);

    $.get('/generateSpecifiedMusic', {
            userInput: userInput,
            instrumentNumber: instrumentNumber,
            displaySheetMusic: displaySheetMusic,
            noteDensity: noteDensity,
            tempo: tempo,
            sliderValues: sliderValues}, function(data) {
        console.log('data: ', data);

		MIDIjs.play('../outputs/live/livesong.mid');
    });
    return false;
});

// WATCHERS
$('.mega-menu-column a').click(function() {
   instrumentNumber = $(this).attr('id');
   $("#instrument-dropdown-header").text('Instrument: ' + $(this).text());
   console.log(instrumentNumber);
});

function getSliderValues() {
	sliderValues = [];
	for(i = 1; i < 11; i++) {
		sliderValues.push($('#slider-' + i).val());
	}
	console.log('sliderValues: ', sliderValues);
	return JSON.stringify(sliderValues);
}

function setSliderValues(valuesArray) {
	for(i = 1; i < 11; i++) {
		$('#slider-' + i).val(valuesArray[i-1].randomNumber);
		$('#slider-' + i).prop('min', valuesArray[i-1].bottomLimit);
		$('#slider-' + i).prop('max', valuesArray[i-1].topLimit);
		$('#slider-' + i).prop('step', valuesArray[i-1].incrementValue);
	}
	console.log('valuesArray: ', valuesArray);
}