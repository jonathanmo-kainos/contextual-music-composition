/*jshint esversion: 6 */

var music_player_controller = require('../js/music_player_controller');

describe('music_player_controller tests', () => {
	test('convertSecondsToTime 1', () => {
		expect(music_player_controller.convertSecondsToTime(1)).toBe('00:01');
	});

	test('convertSecondsToTime 10', () => {
		expect(music_player_controller.convertSecondsToTime(10)).toBe('00:10');
	});

	test('convertSecondsToTime 100', () => {
		expect(music_player_controller.convertSecondsToTime(100)).toBe('01:40');
	});

	test('convertSecondsToTime 1000', () => {
		expect(music_player_controller.convertSecondsToTime(1000)).toBe('16:40');
	});

	test('convertSecondsToTime 10000', () => {
		expect(music_player_controller.convertSecondsToTime(10000)).toBe('2:46:40');
	});

	test('generateUUID unique', () => {
		var uuid1 = music_player_controller.generateUUID();
		var uuid2 = music_player_controller.generateUUID();
		expect(uuid1).not.toBe(uuid2);
	});

	test('generateUUID regex', () => {
		var expected = [
			expect.stringMatching(/[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}/),
		];
		var uuids = [music_player_controller.generateUUID(), music_player_controller.generateUUID()];
        expect(uuids).toEqual(expect.arrayContaining(expected),);
	});
});