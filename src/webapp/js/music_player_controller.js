$("#play").on("click", function() {
    MIDIjs.initAll();
    MIDIjs.play('../../../outputs/live/livesong.mid');
});
$("#pause").on("click", function() {
    MIDIjs.pause('../../../outputs/live/livesong.mid');
});

function generateRandomMusic() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", '/generate', true); // true for asynchronous
    xmlHttp.send(null);
}