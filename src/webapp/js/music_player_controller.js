$(document).ready(function() {
});

var totalTime = 0;
var currentTime = 0;
var isSongFinished = false;
var loopSong = true;
var playbackStopped = false;

// USER INPUTS
var userInput = '';
var instrumentNumber = 0;
var blackWithWhite = false;
var noteCertainty = 99.9;
var noteLength = 50;
var playbackSpeed = 1;
var sliderValues = [];

$('#generate-button').one('click', function() {
	userInput = $('#user-input').val();
	console.log('userInput: ', userInput);

	stopPlayback();

    $.get('/generateRandomMusic', {userInput: userInput}, function(data) {
        console.log('data: ', data);
        setSliderValues(data);
    }).then(function() {
		playSongFromUrl();
		setSongDuration();
        setupMidiJsTimeCounting();
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
	playbackSpeed = $('#playback-speed-slider').val();
	blackWithWhite = $('#image-colour-toggle').is(':checked');
	sliderValues = getSliderValues();

	console.log('userInput: ', userInput);
	console.log('instrumentNumber: ', instrumentNumber);
	console.log('blackWithWhite: ', blackWithWhite);
	console.log('noteCertainty: ', noteCertainty);
	console.log('noteLength: ', noteLength);
	console.log('playbackSpeed: ', playbackSpeed);

	stopPlayback();

    $.get('/generateSpecifiedMusic', {
            userInput: userInput,
            instrumentNumber: instrumentNumber,
            blackWithWhite: blackWithWhite,
            noteCertainty: noteCertainty,
            noteLength: noteLength,
            playbackSpeed: playbackSpeed,
            sliderValues: sliderValues}, function(data) {
        console.log('data: ', data);
    }).then(function() {
		playSongFromUrl();
		setSongDuration();
        setupMidiJsTimeCounting();
		generateRandomName();
		updateBarImages();
    });
    return false;
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

function generateRandomName() {
	var name = generateName();
	var exclamation = generateExclamation();

    $('#song-name').text(name);
    $('#song-exclamation').text(exclamation);
}

function updateBarImages() {
	d = new Date();
	for(i = 1; i < 17; i++) {
//		$('#bar-' + i).attr('src','../outputs/live/' + (i-1) + '.png?'+d.getTime());
		$('#bar-' + i).attr('src','http://127.0.0.1:8887/' + (i-1) + '.png?'+d.getTime());
	}
}

// MUSIC CONTROL FUNCTIONS
function setSongDuration() {
//	MIDIjs.get_duration('../outputs/live/livesong.mid', function(seconds) {
	MIDIjs.get_duration('http://127.0.0.1:8887/livesong.mid', function(seconds) {
		totalTime = Math.round(seconds);
		$('#total-time').text(' / ' + convertSecondsToMinutes(totalTime));
	});
}

function playSongFromUrl() {
//	MIDIjs.play('../outputs/live/livesong.mid');
	MIDIjs.play('http://127.0.0.1:8887/livesong.mid');
    $('.play-pause-button').addClass('playing');
    isSongFinished = false;
    playbackStopped = false;
}

function stopPlayback() {
	MIDIjs.stop();
	playbackStopped = true;
    $('.play-pause-button').removeClass('playing');
    console.log('loopssong: ', loopSong);
    console.log('songifniishd: ', isSongFinished);
	if (isSongFinished && loopSong) {
		console.log('looping');
		playSongFromUrl();
	}
}

function setupMidiJsTimeCounting() {
	MIDIjs.player_callback = displayTime;
	function displayTime(playerEvent) {
	console.log('displaytime');
		currentTime = Math.floor(playerEvent.time);
		if (currentTime == totalTime && !isSongFinished) {
			currentTime = 0;
			isSongFinished = true;
		}
		$('#current-time').text(convertSecondsToMinutes(currentTime));
		if (isSongFinished && !playbackStopped) {
			stopPlayback();
		}
	}
}

// WATCHERS
$('.mega-menu-column a').click(function() {
   instrumentNumber = $(this).attr('id');
   $('#instrument-dropdown-header').text('Instrument: ' + $(this).text());
   console.log(instrumentNumber);
});

$('.play-pause-button').click(function() {
    $('.play-pause-button').toggleClass('playing');
    if ($('.play-pause-button').hasClass('playing')) {
        if (isSongFinished) {
            playSongFromUrl();
            isSongFinished = false;
        } else {
			MIDIjs.resume();
		}
    } else {
		MIDIjs.pause();
    }
});

$('#loop-song').click(function() {
    $('#loop-song').toggleClass('looping');
    loopSong = $('#loop-song').hasClass('looping');
    console.log('loopsong: ', loopSong);
});

// HELPER METHODS
function convertSecondsToMinutes(currentTimeInSeconds) {
	var timeToDisplay = '';
	var hours = Math.floor(currentTimeInSeconds / 3600);
	if (hours > 0) {
		timeToDisplay = hours + ':';
	}
    currentTimeInSeconds -= hours * 3600;
    var minutes = Math.floor(currentTimeInSeconds / 60);
    currentTimeInSeconds -= minutes * 60;
    return timeToDisplay + (minutes < 10 ? '0' + minutes : minutes) + ':' + (currentTimeInSeconds < 10 ? '0' + currentTimeInSeconds : currentTimeInSeconds);
}