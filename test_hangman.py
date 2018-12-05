from unittest import TestCase
import mock

from hangman import HangmanGame


class HangmanGameTestCase(TestCase):

    def setUp(self):
        self.h = HangmanGame()
        self.h.choosen_word = '3dhubshubs'
        self.h.prepare()

    def check_input_processed(self, input, expected_result, attempts):
        result = self.h.process_input(input)
        assert result == expected_result
        assert self.h.failed_attemts_left == attempts

    def test_process_invalid_input(self):
        self.check_input_processed('', 'not_letter', 5)
        self.check_input_processed('abc', 'not_letter', 5)
        self.check_input_processed('3', 'not_letter', 5)
        self.check_input_processed('_', 'not_letter', 5)
        self.check_input_processed('3abc', 'not_letter', 5)
        self.check_input_processed('', 'not_letter', 5)

    def test_process_valid_input(self):
        self.check_input_processed('a', 'unlucky_guess', 4)
        self.check_input_processed('z', 'unlucky_guess', 3)

        self.check_input_processed('d', 'lucky_guess', 3)
        self.check_input_processed('h', 'lucky_guess', 3)

        self.check_input_processed('h', 'already_revealed', 3)
        self.check_input_processed('a', 'already_wasted', 3)

    def test_process_win(self):
        self.check_input_processed('d', 'lucky_guess', 5)
        self.check_input_processed('h', 'lucky_guess', 5)
        self.check_input_processed('u', 'lucky_guess', 5)
        self.check_input_processed('b', 'lucky_guess', 5)
        self.check_input_processed('s', 'epic_win', 5)

    def test_process_fail(self):
        self.check_input_processed('z', 'unlucky_guess', 4)
        self.check_input_processed('x', 'unlucky_guess', 3)
        self.check_input_processed('y', 'unlucky_guess', 2)
        self.check_input_processed('w', 'unlucky_guess', 1)
        self.check_input_processed('v', 'epic_fail', 0)

    @mock.patch('hangman.get_input', mock.Mock(side_effect=['z', 'x', 'c', 'v', 'b', 'n']))
    def test_game(self):
        self.h.start_game()
        assert self.h.failed_attemts_left == 0
