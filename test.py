#!/usr/bin/env python

import unittest

from gtp import pre_engine, pre_controller
from gtp import parse_message, parse_move
from gtp import BLACK, WHITE
from gtp import Engine


class PreProcessingTest(unittest.TestCase):

    def test_pre_engine(self):
        self.assertEqual(pre_engine("foo\rbar"), "foobar")
        self.assertEqual(pre_engine("foo\nbar"), "foo\nbar")
        self.assertEqual(pre_engine("foo\tbar"), "foo bar")
        self.assertEqual(pre_engine("foo # bar"), "foo ")

    def test_pre_controller(self):
        self.assertEqual(pre_controller("foo\rbar"), "foobar")
        self.assertEqual(pre_controller("foo\nbar"), "foo\nbar")
        self.assertEqual(pre_controller("foo\tbar"), "foo bar")


class ParseTest(unittest.TestCase):

    def test_parse_message(self):
        self.assertEqual(parse_message("foo"), (None, "foo", None))
        self.assertEqual(parse_message("foo bar"), (None, "foo", "bar"))
        self.assertEqual(parse_message("1 foo"), (1, "foo", None))
        self.assertEqual(parse_message("1 foo bar"), (1, "foo", "bar"))
        self.assertEqual(parse_message("1"), (1, None, None))
        self.assertEqual(parse_message(""), (None, "", None))
        self.assertEqual(parse_message(" "), (None, "", None))

    def test_parse_move(self):
        self.assertEqual(parse_move("B D4"), (BLACK, 4, 4))
        self.assertFalse(parse_move("C X"))
        self.assertEqual(parse_move("WHITE q16 XXX"), (WHITE, 16, 16))


class CommandsTest(unittest.TestCase):

    def setUp(self):
        self.engine = Engine()

    def test_admin_commands(self):
        response = self.engine.send("foo\n")
        self.assertEqual(response, "? unknown command\n\n")

        response = self.engine.send("protocol_version\n")
        self.assertEqual(response, "= 2\n\n")
        response = self.engine.send("1 protocol_version\n")
        self.assertEqual(response, "=1 2\n\n")

        response = self.engine.send("2 name\n")
        self.assertEqual(response, "=2 gtp (python library)\n\n")

        response = self.engine.send("3 version\n")
        self.assertEqual(response, "=3 0.1\n\n")

        response = self.engine.send("4 known_command name\n")
        self.assertEqual(response, "=4 true\n\n")
        response = self.engine.send("5 known_command foo\n")
        self.assertEqual(response, "=5 false\n\n")

        response = self.engine.send("6 list_commands\n")
        self.assertEqual(
            response,
            "=6 protocol_version\nname\nversion\nknown_command\n"
            "list_commands\nquit\nboardsize\nclear_board\nkomi\n"
            "play\ngenmove\n\n")

        response = self.engine.send("99 quit\n")
        self.assertEqual(response, "=99\n\n")

    def test_core_play_commands(self):
        response = self.engine.send("7 boardsize 100")
        self.assertEqual(response, "?7 unacceptable size\n\n")
        response = self.engine.send("8 boardsize 19")
        self.assertEqual(response, "=8\n\n")

        response = self.engine.send("9 clear_board")
        self.assertEqual(response, "=9\n\n")

        response = self.engine.send("10 komi 6.5")
        self.assertEqual(response, "=10\n\n")
        response = self.engine.send("11 komi foo")
        self.assertEqual(response, "?11 syntax error\n\n")

    def test_core_play(self):
        response = self.engine.send("12 play black D4")
        self.assertEqual(response, "=12\n\n")

        response = self.engine.send("13 genmove white")
        # test player will always return this
        self.assertEqual(response, "=13 Q16\n\n")


if __name__ == "__main__":
    unittest.main()
