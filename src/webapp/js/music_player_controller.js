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

$('#generate-button').one('click', function() {
	userInput = $('#user-input').val();

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
	blackWithWhite = $('#image-colour-toggle').is(':checked');
	noteCertainty = (100 - $('#density-slider').val());
	noteLength = $('#length-slider').val();
	playbackSpeed = $('#playback-speed-slider').val();
	volume = $('#volume-slider').val();
	randomiseOnScreenSliders = $('#randomise-on-screen-sliders').is(':checked');
	randomiseOffScreenSliders = $('#randomise-off-screen-sliders').is(':checked');
	pcaSliderComponents = getPcaSliderComponents();

	stopPlayback();

    $.get('/generateSpecifiedMusic', {
            userInput: userInput,
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

$(document).on('click', '#download-midi-link', function() {
	d = new Date();
	var currentLink = $('#download-midi-link').prop('href');
	$('#download-midi-link').prop('href', currentLink + '?' + d.getTime());
});

function getPcaSliderComponents() {
	for (i = 1; i <= 10; i++) {
		pcaSliderComponents[i-1].number = parseFloat($('#slider-' + i).val());
		console.log($('#slider-' + i).val());
	}
	console.log('pcaSliderComponents: ', pcaSliderComponents.length);
	return JSON.stringify(pcaSliderComponents);
}

function setSliderValues(sliderComponents) {
	pcaSliderComponents = sliderComponents;
	for (i = 1; i <= 10; i++) {
		$('#slider-' + i).val(sliderComponents[i-1].number);
		$('#slider-' + i).prop('min', sliderComponents[i-1].bottomLimit);
		$('#slider-' + i).prop('max', sliderComponents[i-1].topLimit);
		$('#slider-' + i).prop('step', sliderComponents[i-1].incrementValue);
	}
	console.log('sliderComponents: ', sliderComponents);
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
		$('#bar-' + i).attr('src','http://127.0.0.1:8887/' + (i-1) + '.png?' + d.getTime());
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