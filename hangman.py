from random import choice

# separating text strings is good practice, e.g. for translation purposes
MESSAGES = {
    'welcome': 'Welcome to the HangMan game!',
    'guess_invitation': 'Your guess: ',
    'not_letter': 'This is not a single letter. Please be careful when you type. It\'s violent game, after all.',
    'already_revealed': 'This letter is already revealed. No need to double-check, trust me',
    'already_wasted': 'You already tried with this letter, with no luck. Leave it alone.',
    'lucky_guess': 'You was lucky this time! Keep guessing!',
    'unlucky_guess': 'Nice try, but you was wrong, and this is one step closer to the edge',
    'attempts_left': 'You have {} attempts left!',
    'epic_win': 'You won! Such a lucky day for you. Go buy some lottery.',
    'epic_fail': 'We need to talk. Just sit back and listen. '
                 'It\'s not about you, it\'s about me. '
                 'You have no more attempts. '
                 'This is the end of this game. Bye.'
}


def get_input(text):
    return input(text)


class HangmanGame:

    wordlist = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    choosen_word = None
    failed_attemts_left = 5

    def __init__(self):
        self.choosen_word = choice(self.wordlist)
        self.prepare()

    def prepare(self):
        self.current_state = ['_' if self.is_letter(_) else _ for _ in self.choosen_word]
        self.failed_ateempts_letters = set()

    def is_letter(self, char):
        return 97 <= ord(char) <= 122

    def start_game(self):
        print(MESSAGES['welcome'])
        self.step()

    def step(self):
        # print current state
        print(' '.join(self.current_state))
        print(MESSAGES['attempts_left'].format(self.failed_attemts_left))

        # ask for input
        step_letter = get_input(MESSAGES['guess_invitation']).lower()

        # process input
        result = self.process_input(step_letter)
        print(MESSAGES[result])
        print('')

        if not result.startswith('epic'):
            self.step()

    def process_input(self, l):
        # only letters a-z allowed
        if len(l) != 1:
            return 'not_letter'

        if not self.is_letter(l):
            return 'not_letter'

        if l in self.current_state:
            return 'already_revealed'

        if l in self.failed_ateempts_letters:
            return 'already_wasted'

        if l in self.choosen_word:
            self.current_state = [c if l == c else self.current_state[i] for i, c in enumerate(self.choosen_word)]

            if '_' not in self.current_state:
                return self.finalize_win()
            return 'lucky_guess'
        else:
            self.failed_attemts_left -= 1
            self.failed_ateempts_letters.add(l)

            if self.failed_attemts_left == 0:
                return self.finalize_fail()
            return 'unlucky_guess'

    def finalize_win(self):
        # TODO: highscore
        return 'epic_win'

    def finalize_fail(self):
        return 'epic_fail'
