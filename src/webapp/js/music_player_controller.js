$("#play").on("click", function() {
    MIDIjs.initAll();
    MIDIjs.play('../../../outputs/live/livesong.mid');
});
$("#pause").on("click", function() {
    MIDIjs.pause('../../../outputs/live/livesong.mid');
});
