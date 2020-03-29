var userInput = '';
var instrumentNumber = 0;
var displaySheetMusic = false;
//var minorTonality = false;
var noteDensity = 99.9;
var tempo = 1;
var sliderValues = [];

$('#generate-button').bind('click', function() {
    MIDIjs.initAll();
	var userInput = $('#user-input').val();
	noteDensity = $('#density-slider').val();
	tempo = $('#tempo-slider').val();
	getSliderValues();

	console.log('userInput: ', userInput);
	console.log('instrumentNumber: ', instrumentNumber);
	console.log('displaySheetMusic: ', displaySheetMusic);
//	console.log('minorTonality: ', minorTonality);
	console.log('noteDensity: ', noteDensity);
	console.log('tempo: ', tempo);

    $.get('/generateRandomMusic', {
            userInput: userInput,
            instrumentNumber: instrumentNumber,
            displaySheetMusic: displaySheetMusic,
//            minorTonality: minorTonality,
            noteDensity: noteDensity,
            tempo: tempo,
            sliderValues: sliderValues}, function(data) {
        console.log('data: ', data);
        setSliderValues(data);

		MIDIjs.play('../outputs/live/livesong.mid');
    });
    return false;
});

$('.mega-menu-column a').click(function() {
   instrumentNumber = $(this).attr('id');
   $("#instrument-dropdown-header").text('Instrument: ' + $(this).text());
   console.log(instrumentNumber);
});

$('#music-display-toggle').click(function() {
   displaySheetMusic = $(this).is(":checked");
   console.log(displaySheetMusic);
});

function getSliderValues() {
	for(i = 1; i < 11; i++) {
		sliderValues[i-1] = $('#slider-' + i).val();
	}
	console.log('sliderValues: ', sliderValues);
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

//$('#tonality-toggle').click(function() {
//   minorTonality = $(this).is(":checked");
//   console.log(minorTonality);
//});