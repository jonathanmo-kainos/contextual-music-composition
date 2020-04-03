$(document).ready(function() {
	MIDIjs.player_callback = displayTime;
	function displayTime(playerEvent) {
		var timeToDisplay;
		var currentTime = Math.floor(playerEvent.time);
		if (currentTime < 10) {
			timeToDisplay = '00:0' + currentTime;
		} else {
			timeToDisplay = '00:' + currentTime;
		}
		$('#current-time').text(timeToDisplay);
	};
});

var userInput = '';
var instrumentNumber = 0;
var blackWithWhite = false;
var noteCertainty = 99.9;
var noteLength = 50;
var tempo = 1;
var sliderValues = [];

$('#generate-button').one('click', function() {
	userInput = $('#user-input').val();

	MIDIjs.stop();

	console.log('userInput: ', userInput);

    $.get('/generateRandomMusic', {userInput: userInput}, function(data) {
        console.log('data: ', data);
        setSliderValues(data);

//		MIDIjs.play('../outputs/live/livesong.mid');
//		MIDIjs.get_duration('../outputs/live/livesong.mid', function(seconds) {
//			var totalTime = Math.round(seconds);
//			var totalTimeToDisplay = ' / 00:' + totalTime;
//			$('#total-time').text(totalTimeToDisplay);
//		});
		MIDIjs.play('http://127.0.0.1:8887/livesong.mid');
		MIDIjs.get_duration('http://127.0.0.1:8887/livesong.mid', function(seconds) {
			var totalTime = Math.round(seconds);
			var totalTimeToDisplay = ' / 00:' + totalTime;
			$('#total-time').text(totalTimeToDisplay);
		});
    }).then(function() {
		generateRandomName();
		updateBarImages();
    });;
    $('#generate-button').prop('id', 'generate-button-clicked');
    return false;
});

$(document).on('click', '#generate-button-clicked', function() {
	userInput = $('#user-input').val();
	noteCertainty = (100 - $('#density-slider').val());
	noteLength = $('#length-slider').val();
	tempo = $('#tempo-slider').val();
	blackWithWhite = $('#image-colour-toggle').is(":checked");
	sliderValues = getSliderValues();

	MIDIjs.stop();

	console.log('userInput: ', userInput);
	console.log('instrumentNumber: ', instrumentNumber);
	console.log('blackWithWhite: ', blackWithWhite);
	console.log('noteCertainty: ', noteCertainty);
	console.log('noteLength: ', noteLength);
	console.log('tempo: ', tempo);

    $.get('/generateSpecifiedMusic', {
            userInput: userInput,
            instrumentNumber: instrumentNumber,
            blackWithWhite: blackWithWhite,
            noteCertainty: noteCertainty,
            noteLength: noteLength,
            tempo: tempo,
            sliderValues: sliderValues}, function(data) {
        console.log('data: ', data);

//		MIDIjs.play('../outputs/live/livesong.mid');
//		MIDIjs.get_duration('../outputs/live/livesong.mid', function(seconds) {
//			var totalTime = Math.round(seconds);
//			var totalTimeToDisplay = ' / 00:' + totalTime;
//			$('#total-time').text(totalTimeToDisplay);
//		});
		MIDIjs.play('http://127.0.0.1:8887/livesong.mid');
		MIDIjs.get_duration('http://127.0.0.1:8887/livesong.mid', function(seconds) {
			var totalTime = Math.round(seconds);
			var totalTimeToDisplay = ' / 00:' + totalTime;
			$('#total-time').text(totalTimeToDisplay);
		});
    }).then(function() {
		generateRandomName();
		updateBarImages();
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

$(".play-pause-button").click(function() {
    $(".play-pause-button").toggleClass("playing");
    if ($(".play-pause-button").hasClass("playing")) {
		MIDIjs.resume();
    } else {
		MIDIjs.pause();
    }
});

function generateRandomName() {
	var name = generateName();
	var exclamation = generateExclamation();

    $('#song-name').text(name);
    $('#song-exclamation').text(exclamation);
}

function updateBarImages() {
	d = new Date();
	for(i = 1; i < 17; i++) {
		$("#bar-" + i).attr("src","http://127.0.0.1:8887/" + (i-1) + ".png?"+d.getTime());
//		$("#bar-" + i).attr("src","../outputs/live/" + (i-1) + ".png?"+d.getTime());
	}
}