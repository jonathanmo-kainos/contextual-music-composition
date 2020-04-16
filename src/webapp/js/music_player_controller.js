/*jshint esversion: 6 */

var functions = {
	convertSecondsToTime: convertSecondsToTime,
	generateUUID: generateUUID
};

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
var volume = 63;
var randomiseOnScreenSliders = true;
var randomiseOffScreenSliders = true;
var pcaSliderComponents = [];
var currentUUID = '';
var previousUUID = '';

var liveOutputDirectoryFilepath = 'http://127.0.0.1:8887/';
//var liveOutputDirectoryFilepath = '../outputs/live/';

$('#generate-button').one('click', function() {
	userInput = $('#user-input').val();
	updateUUIDs();

	stopPlayback();

    $.post('/generateRandomMusic', {userInput: userInput, currentUUID: currentUUID, previousUUID: previousUUID}, function(data) {
        var input = JSON.parse(data);
        setSliderValues(input.pca_slider_components);
        setNoteDensity(input.note_certainty);
        setNoteLength(input.note_length);
        setSpeed(input.playback_speed);
    }).then(function() {
		playSongFromUrl();
		setSongDuration();
        setupMidiJsTimeCounting();
		generateRandomName();
		updateBarImages();
    });
    $('#generate-button').prop('id', 'generate-button-clicked');
    return false;
});

$(document).on('click', '#generate-button-clicked', function() {
	userInput = $('#user-input').val();
	blackWithWhite = $('#image-colour-toggle').is(':checked');
	noteCertainty = (100 - $('#density-slider').val());
	noteLength = $('#length-slider').val();
	playbackSpeed = $('#speed-slider').val();
	volume = $('#volume-slider').val();
	randomiseOnScreenSliders = $('#randomise-on-screen-sliders').is(':checked');
	randomiseOffScreenSliders = $('#randomise-off-screen-sliders').is(':checked');
	pcaSliderComponents = getPcaSliderComponents();
	updateUUIDs();

	stopPlayback();

    $.post('/generateSpecifiedMusic', {
            userInput: userInput,
            currentUUID: currentUUID,
            previousUUID: previousUUID,
            blackWithWhite: blackWithWhite,
            noteCertainty: noteCertainty,
            noteLength: noteLength,
            playbackSpeed: playbackSpeed,
            volume: volume,
            instrumentNumber: instrumentNumber,
            randomiseOnScreenSliders: randomiseOnScreenSliders,
            randomiseOffScreenSliders: randomiseOffScreenSliders,
            pcaSliderComponents: pcaSliderComponents}, function(data) {
        setSliderValues(data);
    }).then(function() {
		playSongFromUrl();
		setSongDuration();
        setupMidiJsTimeCounting();
		generateRandomName();
		updateBarImages();
    });
    return false;
});

function getPcaSliderComponents() {
	for (i = 1; i <= 10; i++) {
		pcaSliderComponents[i-1].number = parseFloat($('#slider-' + i).val());
	}
	return JSON.stringify(pcaSliderComponents);
}

function updateBarImages() {
	d = new Date();
	for(i = 1; i < 17; i++) {
		$('#bar-' + i).prop('src', liveOutputDirectoryFilepath + (i-1) + '.png?' + d.getTime());
	}
}

// MUSIC CONTROL FUNCTIONS
function playSongFromUrl() {
	MIDIjs.play(liveOutputDirectoryFilepath + 'livesong.mid');
    $('.play-pause-button').addClass('playing');
    isSongFinished = false;
    playbackStopped = false;
}

function stopPlayback() {
	MIDIjs.stop();
	playbackStopped = true;
    $('.play-pause-button').removeClass('playing');
	if (isSongFinished && loopSong) {
		playSongFromUrl();
	}
}

function setupMidiJsTimeCounting() {
	MIDIjs.player_callback = displayTime;
	function displayTime(playerEvent) {
		currentTime = Math.floor(playerEvent.time);
		if (currentTime == totalTime && !isSongFinished) {
			currentTime = 0;
			isSongFinished = true;
		}
		$('#current-time').text(convertSecondsToTime(currentTime));
		if (isSongFinished && !playbackStopped) {
			stopPlayback();
		}
	}
}

// SETTERS FOR CONFIGS
function setSliderValues(sliderComponents) {
	pcaSliderComponents = sliderComponents;
	for (i = 1; i <= 10; i++) {
		$('#slider-' + i).val(sliderComponents[i-1].number);
		$('#slider-' + i).prop('min', sliderComponents[i-1].bottomLimit);
		$('#slider-' + i).prop('max', sliderComponents[i-1].topLimit);
		$('#slider-' + i).prop('step', sliderComponents[i-1].incrementValue);
	}
}

function setNoteDensity(noteCertainty) {
	$('#density-slider').val(100 - noteCertainty);
}

function setNoteLength(noteLength) {
	$('#length-slider').val(noteLength);
}

function setSpeed(speed) {
	$('#speed-slider').val(speed);
}

function setSongDuration() {
	MIDIjs.get_duration(liveOutputDirectoryFilepath + 'livesong.mid', function(seconds) {
		totalTime = Math.round(seconds);
		$('#total-time').text(' / ' + convertSecondsToTime(totalTime));
	});
}

// WATCHERS
$('.mega-menu-column a').click(function() {
   instrumentNumber = $(this).prop('id');
   $('#instrument-dropdown-header').text('Instrument: ' + $(this).text());
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
});

$('.music-control-slider').click(function() {
    $('#randomise-on-screen-sliders').prop('checked', false);
    randomiseOnScreenSliders = false;
});

// HELPER METHODS
function convertSecondsToTime(currentTimeInSeconds) {
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

function generateUUID() { // Public Domain/MIT
    var d = new Date().getTime(); //Timestamp
    var d2 = (performance && performance.now && (performance.now()*1000)) || 0; //Time in microseconds since page-load or 0 if unsupported
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16; //random number between 0 and 16
        if(d > 0){ //Use timestamp until depleted
            r = (d + r)%16 | 0;
            d = Math.floor(d/16);
        } else { //Use microseconds since page-load if supported
            r = (d2 + r)%16 | 0;
            d2 = Math.floor(d2/16);
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}

function updateUUIDs() {
	previousUUID = currentUUID;
	currentUUID = generateUUID();
//	liveOutputDirectoryFilepath = '../outputs/live/' + currentUUID + '/';
	liveOutputDirectoryFilepath = 'http://127.0.0.1:8887/' + currentUUID + '/';
	$('#download-midi-link').prop('href', '/downloadMidi' + '?currentUUID=' + currentUUID);
}

function generateRandomName() {
	var name = generateName();
	var exclamation = generateExclamation();

    $('#song-name').text(name);
    $('#song-exclamation').text(exclamation);
}

module.exports = functions;