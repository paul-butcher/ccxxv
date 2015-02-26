from __future__ import print_function
import re
from os import path

HERE = path.abspath(path.dirname(__file__))


def cli_main():
    import sys
    wordlist = None
    if not sys.stdin.isatty():
        wordlist = sys.stdin.read()
    return main(*sys.argv[1:], wordlist=wordlist)


def main(word0, word1=None, wordlist=None):
    if word1:
        print_groups(Solver(wordlist).solve_word_pair(word0, word1))
    else:
        print("\n".join(Solver(wordlist).solve_single_word(word0)))


class Solver(object):
    """
    A crossword solving assistant.

    :param wordlist: The wordlist to use, either the name of the wordlist,
      or an iterable of strings.

    The solver uses the UK Advanced Cryptics dictionary by default.
    This dictionary contains various proper nouns common in crosswords
    as well as words normally considered legal in word games such as Scrabble.


    >>> Solver().solve_single_word('Aachen')
    ['Aachen']

    Other wordlists may be specified in the same format as UKACD, a string with one entry per line.

    >>> s = Solver(wordlist='Hello\\nWorld')
    >>> s.solve_single_word('.....')
    ['Hello', 'World']

    Alternatively the wordlist_name argument can be used to load a wordlist from the wordlists directory

    >>> s = Solver(wordlist_name='sample')
    >>> s.solve_single_word('.....')
    ['Hello', 'World']

    """

    def __init__(self, wordlist=None, wordlist_name='UKACD'):
        self.wordlist = wordlist or self.load_wordlist(wordlist_name)

    @classmethod
    def load_wordlist(cls, wordlist_name):
        with open(path.join(HERE, 'wordlists', wordlist_name + '.txt')) as dict_file:
            return dict_file.read()

    def solve_single_word(self, pattern):
        """
        :param pattern: an answer pattern.  missing letters are indicated by '.'
        :return: A list of words that conform to that pattern.

        Traditional crossword pattern solver behaviour -
        Given a pattern, returns all words that fit that pattern.


        >>> s = Solver()
        >>> s.solve_single_word('.ylophone')
        ['xylophone']

        Capitalisation is not important.

        >>> s.solve_single_word('a.ron')
        ['Aaron', 'Akron', 'apron']
        >>> s.solve_single_word('A.ron')
        ['Aaron', 'Akron', 'apron']

        Patterns may include spaces, and spaces will be matched.

        >>> s.solve_single_word('a.andon s.ip')
        ['abandon ship']

        However, a space won't be matched as an unknown character

        >>> s.solve_single_word('abandon.ship')
        []

        The same is true for hyphens

        >>> s.solve_single_word('abat-.our')
        ['abat-jour']
        >>> s.solve_single_word('abat.jour')
        []

        There is no requirement that any letters are known or not known

        >>> s.solve_single_word('Aachen')
        ['Aachen']

        >>> s.solve_single_word('........................')
        ['Aldiborontiphoscophornia', 'hydrochlorofluorocarbons']

        """
        return re.findall(
            r'(?:(?<=\n)|^)(%s)(?:(?=\n)|$)' % pattern.replace('.', r'\w'),
            self.wordlist,
            re.IGNORECASE
        )

    def solve_word_pair(self, pattern0, pattern1):
        """
        :param pattern0: an answer pattern.  Missing letters are indicated by '.'; '+'
         marks the unknown letter which is common to both words.
        :param pattern1: as with pattern0.
        :return: A list of words that conform to that pattern.

        Given two patterns that cross on an unknown letter (marked as '+' in the patterns),
        returns a dictionary where the keys correspond to the crossing letter and the values is
        a tuple containing a list for each pattern

        >>> s = Solver()
        >>> s.solve_word_pair('+oology', 'ad+e')
        {'z': (['zoology'], ['adze'])}

        The first 'column' matches the first argument, the second matches the second.

        >>> s.solve_word_pair('ad+e', '+oology')
        {'z': (['adze'], ['zoology'])}

        '.' indicates a missing character, just as in a single-word query.

        >>> s.solve_word_pair('z+olo..', '.uin+a')
        {'o': (['zoology'], ['quinoa'])}

        Capitalisation needn't match on the crossing letter.

        >>> s.solve_word_pair('+aron', 'b+ron')
        {'a': (['Aaron'], ['baron'])}

        A crossing character is required on both arguments

        >>> s.solve_word_pair('.aron', 'baron')
        Traceback (most recent call last):
        ...
        ValueError: Both arguments need a crossing character "+"

        Spaces are respected.

        >>> s.solve_word_pair('a.andon s.i+', '+ies')
        {'p': (['abandon ship'], ['pies'])}

        If no words can be found, an empty dictionary is returned:

        >>> s.solve_word_pair('xyzz+', '+ellow')
        {}
        >>> s.solve_word_pair('+ellow', 'x+zzy')
        {}
        """
        crosses = _find_crossing_points(pattern0, pattern1)
        words0 = self.solve_single_word(pattern0.replace('+', r'\w'))
        candidate_chars = _chars_at(crosses[0], words0)
        if candidate_chars:
            words1 = self.solve_single_word(pattern1.replace('+', '[%s]' % ''.join(candidate_chars)))
            return _make_letter_groups(candidate_chars, crosses[0], words0, crosses[1], words1)
        return {}

def _find_crossing_points(pattern0, pattern1):
    crosses = (pattern0.find('+'), pattern1.find('+'))
    if -1 in crosses:
        raise ValueError('Both arguments need a crossing character "+"')
    return crosses


def _make_letter_groups(candidate_chars, position0, words0, position1, words1):
    groups = {}

    for char in candidate_chars:
        group = (
            [word for word in words0 if word[position0].lower() == char],
            [word for word in words1 if word[position1].lower() == char]
        )

        if group[0] and group[1]:
            groups[char] = group

    return groups


def _chars_at(position, words):
    """
    Returns a lowercased set of all characters at the given position in the given list of words.
    """
    return set([word[position].lower() for word in words])


def print_groups(groups):
    for key, value in groups.items():
        print(key)
        index = 0
        if len(value[0]) >= len(value[1]):
            for index, word in enumerate(value[1]):
                print(value[0][index] + '\t' + word)

            for word in value[0][index+1:]:
                print(word)
        else:
            longest = 0
            for index, word in enumerate(value[0]):
                print(word + '\t' + value[1][index])
                length = len(word)
                if length > longest:
                    longest = length

            format_string = "{0:%s}\t{1}" % longest
            for i in xrange(index, len(value[1])):
                print(format_string.format(' ', value[1][i]))

