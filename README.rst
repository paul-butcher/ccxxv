CCXXV
====

CCXXV is a crossword assistant, intended to help you find the right word to fill out your missing squares.

In addition to the normal functionality to help fill out a single answer, it can also help in those tricky corners
where you have two clues that cross on an unknown letter.

Installation
------------
ccxxv is available through pip::

    $ pip install ccxxv

Usage
-----

To find a word with missing letters, use '.' to represent any missing letters::

    $ ccxxv ba..na

    banana

To find a pair of words that cross on an unknown letter, use '+' to represent the crossing letter::

    $ ccxxv ba+.na u+cle

    n
    banana  uncle


These commands use the default wordlist, `UKACD <http://www.crosswordman.com/wordlist.html>`_.  To use a different
wordlist, pipe it to stdin::

    $ echo xxx | ccxxv ...

    xxx


Why the name?
-------------

CCXXV is 225 in Roman numerals.  Crosswords typically occupy a 15x15 grid, 15x15 is 225 and Roman numerals are a common device in crosswords
(e.g. "Drink for about 50 notes (3)", ALE).


Wordlist
========

The default word list is UKACD 2009, Copyright (c) 2009 J Ross Beresford, All rights reserved.

This is a wordlist designed for crosswords, and contains commonly used phrases and Proper Nouns.