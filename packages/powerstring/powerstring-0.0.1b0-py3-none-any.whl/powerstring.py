#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Powerstring module provides many features for working with strings.

Working with multiline strings in python can be very frustating. There's
an option by using backslash n and spaces which can be very confusing for
reading. Another option is creating multiline strings with three quotes.
The problem with that option is, that you have problems with the indention
and the code will look ugly.
This module provides a feature where you can create multiline strings without
destroying the overall look of the code. You can also style parts of the text,
insert horizontal rules, create lists and add comments in the text itself.

This module also provides following features:
- swapping substrings within a string
- replacing substrings within a string
- progress counter/bar
- highlighted strings
- ansi sequences
"""

__author__ = "phoenixR"
__version__ = "0.0.1 beta"
__copyright__ = "Copyright 2021, phoenixR"
__license__ = "MIT"

# [ REGEX ]
# re.A | re.ASCII        only ascii chars for \b \w \d \s
# re.I | re.IGNORECASE   case-insensitive
# re.L | re.LOCALE       interpret words according to the current locale
# re.M | re.MULTILINE    ^ start of *line*; $ end of *line*
# re.S | re.DOTALL       . matches anything
# re.U | re.UNICODE      interpret letters according to the unicode character set
# re.X | re.VERBOSE      ignores whitespace outside set and # as comment
# 
# ^ $ . [ ] * + ? { } | ( ) 
# 
# *   0 or more
# +   1 or more
# ?   0 or 1
# 
# \w   word
# \W   not word
# \s   whitespace
# \S   not whitespace
# \d   digit
# \D   not digit
# \A   beginning of string
# \Z   end of line
# \z   end of string
# \G   matches point where last match finished
# \b   word boundries outside and backspace inside brackets
# \B   not word boundries
# 
# 
# [ TODO ]
# * code the other functions
# * add line align
# * default escape argument

#############################################
# CODE ######################################

# modules
from collections import namedtuple
from os import get_terminal_size
import re
import string as string_module
import typing

from emoji import emojize
import roman

# constants
CONST_TERMINAL_WIDTH = True

_TYPE_COLOR = typing.Optional[typing.Union[str, int]]
_TYPE_STYLE = typing.Optional[typing.List[str]]

TW, TH = get_terminal_size()
tw = lambda: TW if CONST_TERMINAL_WIDTH else get_terminal_size[0]

QUOTES = "\"'❝❞"

Ansi = namedtuple("Ansi", ["id", "name", "lcase"])
COLORS = [
    Ansi(0, ["Black"],                              ["black"]),
    Ansi(1, ["Maroon"],                             ["maroon"]),
    Ansi(2, ["Green"],                              ["green"]),
    Ansi(3, ["Olive"],                              ["olive"]),
    Ansi(4, ["Navy"],                               ["navy"]),
    Ansi(5, ["Purple"],                             ["purple"]),
    Ansi(6, ["Teal"],                               ["teal"]),
    Ansi(7, ["Silver"],                             ["silver"]),
    Ansi(8, ["Grey", "Gray"],                       ["grey", "gray"]),
    Ansi(9, ["Red"],                                ["red"]),
    Ansi(10, ["Lime"],                              ["lime"]),
    Ansi(11, ["Yellow"],                            ["yellow"]),
    Ansi(12, ["Blue"],                              ["blue"]),
    Ansi(13, ["Fuchsia"],                           ["fuchsia"]),
    Ansi(14, ["Aqua"],                              ["aqua"]),
    Ansi(15, ["White"],                             ["white"]),
    Ansi(16, ["Grey0", "Gray0"],                    ["grey0", "gray0"]),
    Ansi(17, ["NavyBlue"],                          ["navyblue"]),
    Ansi(18, ["DarkBlue"],                          ["darkblue"]),
    Ansi(19, ["Blue3"],                             ["blue3"]),
    Ansi(20, ["Blue3"],                             ["blue3"]),
    Ansi(21, ["Blue1"],                             ["blue1"]),
    Ansi(22, ["DarkGreen"],                         ["darkgreen"]),
    Ansi(23, ["DeepSkyBlue4"],                      ["deepskyblue4"]),
    Ansi(24, ["DeepSkyBlue4"],                      ["deepskyblue4"]),
    Ansi(25, ["DeepSkyBlue4"],                      ["deepskyblue4"]),
    Ansi(26, ["DodgerBlue3"],                       ["dodgerblue3"]),
    Ansi(27, ["DodgerBlue2"],                       ["dodgerblue2"]),
    Ansi(28, ["Green4"],                            ["green4"]),
    Ansi(29, ["SpringGreen4"],                      ["springgreen4"]),
    Ansi(30, ["Turquoise4"],                        ["turquoise4"]),
    Ansi(31, ["DeepSkyBlue3"],                      ["deepskyblue3"]),
    Ansi(32, ["DeepSkyBlue3"],                      ["deepskyblue3"]),
    Ansi(33, ["DodgerBlue1"],                       ["dodgerblue1"]),
    Ansi(34, ["Green3"],                            ["green3"]),
    Ansi(35, ["SpringGreen3"],                      ["springgreen3"]),
    Ansi(36, ["DarkCyan"],                          ["darkcyan"]),
    Ansi(37, ["LightSeaGreen"],                     ["lightseagreen"]),
    Ansi(38, ["DeepSkyBlue2"],                      ["deepskyblue2"]),
    Ansi(39, ["DeepSkyBlue1"],                      ["deepskyblue1"]),
    Ansi(40, ["Green3"],                            ["green3"]),
    Ansi(41, ["SpringGreen3"],                      ["springgreen3"]),
    Ansi(42, ["SpringGreen2"],                      ["springgreen2"]),
    Ansi(43, ["Cyan3"],                             ["cyan3"]),
    Ansi(44, ["DarkTurquoise"],                     ["darkturquoise"]),
    Ansi(45, ["Turquoise2"],                        ["turquoise2"]),
    Ansi(46, ["Green1"],                            ["green1"]),
    Ansi(47, ["SpringGreen2"],                      ["springgreen2"]),
    Ansi(48, ["SpringGreen1"],                      ["springgreen1"]),
    Ansi(49, ["MediumSpringGreen"],                 ["mediumspringgreen"]),
    Ansi(50, ["Cyan2"],                             ["cyan2"]),
    Ansi(51, ["Cyan1"],                             ["cyan1"]),
    Ansi(52, ["DarkRed"],                           ["darkred"]),
    Ansi(53, ["DeepPink4"],                         ["deeppink4"]),
    Ansi(54, ["Purple4"],                           ["purple4"]),
    Ansi(55, ["Purple4"],                           ["purple4"]),
    Ansi(56, ["Purple3"],                           ["purple3"]),
    Ansi(57, ["BlueViolet"],                        ["blueviolet"]),
    Ansi(58, ["Orange4"],                           ["orange4"]),
    Ansi(59, ["Grey37", "Gray37"],                  ["grey37", "gray37"]),
    Ansi(60, ["MediumPurple4"],                     ["mediumpurple4"]),
    Ansi(61, ["SlateBlue3"],                        ["slateblue3"]),
    Ansi(62, ["SlateBlue3"],                        ["slateblue3"]),
    Ansi(63, ["RoyalBlue1"],                        ["royalblue1"]),
    Ansi(64, ["Chartreuse4"],                       ["chartreuse4"]),
    Ansi(65, ["DarkSeaGreen4"],                     ["darkseagreen4"]),
    Ansi(66, ["PaleTurquoise4"],                    ["paleturquoise4"]),
    Ansi(67, ["SteelBlue"],                         ["steelblue"]),
    Ansi(68, ["SteelBlue3"],                        ["steelblue3"]),
    Ansi(69, ["CornflowerBlue"],                    ["cornflowerblue"]),
    Ansi(70, ["Chartreuse3"],                       ["chartreuse3"]),
    Ansi(71, ["DarkSeaGreen4"],                     ["darkseagreen4"]),
    Ansi(72, ["CadetBlue"],                         ["cadetblue"]),
    Ansi(73, ["CadetBlue"],                         ["cadetblue"]),
    Ansi(74, ["SkyBlue3"],                          ["skyblue3"]),
    Ansi(75, ["SteelBlue1"],                        ["steelblue1"]),
    Ansi(76, ["Chartreuse3"],                       ["chartreuse3"]),
    Ansi(77, ["PaleGreen3"],                        ["palegreen3"]),
    Ansi(78, ["SeaGreen3"],                         ["seagreen3"]),
    Ansi(79, ["Aquamarine3"],                       ["aquamarine3"]),
    Ansi(80, ["MediumTurquoise"],                   ["mediumturquoise"]),
    Ansi(81, ["SteelBlue1"],                        ["steelblue1"]),
    Ansi(82, ["Chartreuse2"],                       ["chartreuse2"]),
    Ansi(83, ["SeaGreen2"],                         ["seagreen2"]),
    Ansi(84, ["SeaGreen1"],                         ["seagreen1"]),
    Ansi(85, ["SeaGreen1"],                         ["seagreen1"]),
    Ansi(86, ["Aquamarine1"],                       ["aquamarine1"]),
    Ansi(87, ["DarkSlateGray2"],                    ["darkslategray2"]),
    Ansi(88, ["DarkRed"],                           ["darkred"]),
    Ansi(89, ["DeepPink4"],                         ["deeppink4"]),
    Ansi(90, ["DarkMagenta"],                       ["darkmagenta"]),
    Ansi(91, ["DarkMagenta"],                       ["darkmagenta"]),
    Ansi(92, ["DarkViolet"],                        ["darkviolet"]),
    Ansi(93, ["Purple"],                            ["purple"]),
    Ansi(94, ["Orange4"],                           ["orange4"]),
    Ansi(95, ["LightPink4"],                        ["lightpink4"]),
    Ansi(96, ["Plum4"],                             ["plum4"]),
    Ansi(97, ["MediumPurple3"],                     ["mediumpurple3"]),
    Ansi(98, ["MediumPurple3"],                     ["mediumpurple3"]),
    Ansi(99, ["SlateBlue1"],                        ["slateblue1"]),
    Ansi(100, ["Yellow4"],                          ["yellow4"]),
    Ansi(101, ["Wheat4"],                           ["wheat4"]),
    Ansi(102, ["Grey53", "Gray53"],                 ["grey53", "gray53"]),
    Ansi(103, ["LightSlateGrey", "LightSlateGray"], ["lightslategrey", "lightslategray"]),
    Ansi(104, ["MediumPurple"],                     ["mediumpurple"]),
    Ansi(105, ["LightSlateBlue"],                   ["lightslateblue"]),
    Ansi(106, ["Yellow4"],                          ["yellow4"]),
    Ansi(107, ["DarkOliveGreen3"],                  ["darkolivegreen3"]),
    Ansi(108, ["DarkSeaGreen"],                     ["darkseagreen"]),
    Ansi(109, ["LightSkyBlue3"],                    ["lightskyblue3"]),
    Ansi(110, ["LightSkyBlue3"],                    ["lightskyblue3"]),
    Ansi(111, ["SkyBlue2"],                         ["skyblue2"]),
    Ansi(112, ["Chartreuse2"],                      ["chartreuse2"]),
    Ansi(113, ["DarkOliveGreen3"],                  ["darkolivegreen3"]),
    Ansi(114, ["PaleGreen3"],                       ["palegreen3"]),
    Ansi(115, ["DarkSeaGreen3"],                    ["darkseagreen3"]),
    Ansi(116, ["DarkSlateGray3"],                   ["darkslategray3"]),
    Ansi(117, ["SkyBlue1"],                         ["skyblue1"]),
    Ansi(118, ["Chartreuse1"],                      ["chartreuse1"]),
    Ansi(119, ["LightGreen"],                       ["lightgreen"]),
    Ansi(120, ["LightGreen"],                       ["lightgreen"]),
    Ansi(121, ["PaleGreen1"],                       ["palegreen1"]),
    Ansi(122, ["Aquamarine1"],                      ["aquamarine1"]),
    Ansi(123, ["DarkSlateGray1"],                   ["darkslategray1"]),
    Ansi(124, ["Red3"],                             ["red3"]),
    Ansi(125, ["DeepPink4"],                        ["deeppink4"]),
    Ansi(126, ["MediumVioletRed"],                  ["mediumvioletred"]),
    Ansi(127, ["Magenta3"],                         ["magenta3"]),
    Ansi(128, ["DarkViolet"],                       ["darkviolet"]),
    Ansi(129, ["Purple"],                           ["purple"]),
    Ansi(130, ["DarkOrange3"],                      ["darkorange3"]),
    Ansi(131, ["IndianRed"],                        ["indianred"]),
    Ansi(132, ["HotPink3"],                         ["hotpink3"]),
    Ansi(133, ["MediumOrchid3"],                    ["mediumorchid3"]),
    Ansi(134, ["MediumOrchid"],                     ["mediumorchid"]),
    Ansi(135, ["MediumPurple2"],                    ["mediumpurple2"]),
    Ansi(136, ["DarkGoldenrod"],                    ["darkgoldenrod"]),
    Ansi(137, ["LightSalmon3"],                     ["lightsalmon3"]),
    Ansi(138, ["RosyBrown"],                        ["rosybrown"]),
    Ansi(139, ["Grey63", "Gray63"],                 ["grey63", "gray63"]),
    Ansi(140, ["MediumPurple2"],                    ["mediumpurple2"]),
    Ansi(141, ["MediumPurple1"],                    ["mediumpurple1"]),
    Ansi(142, ["Gold3"],                            ["gold3"]),
    Ansi(143, ["DarkKhaki"],                        ["darkkhaki"]),
    Ansi(144, ["NavajoWhite3"],                     ["navajowhite3"]),
    Ansi(145, ["Grey69", "Gray69"],                 ["grey69", "gray69"]),
    Ansi(146, ["LightSteelBlue3"],                  ["lightsteelblue3"]),
    Ansi(147, ["LightSteelBlue"],                   ["lightsteelblue"]),
    Ansi(148, ["Yellow3"],                          ["yellow3"]),
    Ansi(149, ["DarkOliveGreen3"],                  ["darkolivegreen3"]),
    Ansi(150, ["DarkSeaGreen3"],                    ["darkseagreen3"]),
    Ansi(151, ["DarkSeaGreen2"],                    ["darkseagreen2"]),
    Ansi(152, ["LightCyan3"],                       ["lightcyan3"]),
    Ansi(153, ["LightSkyBlue1"],                    ["lightskyblue1"]),
    Ansi(154, ["GreenYellow"],                      ["greenyellow"]),
    Ansi(155, ["DarkOliveGreen2"],                  ["darkolivegreen2"]),
    Ansi(156, ["PaleGreen1"],                       ["palegreen1"]),
    Ansi(157, ["DarkSeaGreen2"],                    ["darkseagreen2"]),
    Ansi(158, ["DarkSeaGreen1"],                    ["darkseagreen1"]),
    Ansi(159, ["PaleTurquoise1"],                   ["paleturquoise1"]),
    Ansi(160, ["Red3"],                             ["red3"]),
    Ansi(161, ["DeepPink3"],                        ["deeppink3"]),
    Ansi(162, ["DeepPink3"],                        ["deeppink3"]),
    Ansi(163, ["Magenta3"],                         ["magenta3"]),
    Ansi(164, ["Magenta3"],                         ["magenta3"]),
    Ansi(165, ["Magenta2"],                         ["magenta2"]),
    Ansi(166, ["DarkOrange3"],                      ["darkorange3"]),
    Ansi(167, ["IndianRed"],                        ["indianred"]),
    Ansi(168, ["HotPink3"],                         ["hotpink3"]),
    Ansi(169, ["HotPink2"],                         ["hotpink2"]),
    Ansi(170, ["Orchid"],                           ["orchid"]),
    Ansi(171, ["MediumOrchid1"],                    ["mediumorchid1"]),
    Ansi(172, ["Orange3"],                          ["orange3"]),
    Ansi(173, ["LightSalmon3"],                     ["lightsalmon3"]),
    Ansi(174, ["LightPink3"],                       ["lightpink3"]),
    Ansi(175, ["Pink3"],                            ["pink3"]),
    Ansi(176, ["Plum3"],                            ["plum3"]),
    Ansi(177, ["Violet"],                           ["violet"]),
    Ansi(178, ["Gold3"],                            ["gold3"]),
    Ansi(179, ["LightGoldenrod3"],                  ["lightgoldenrod3"]),
    Ansi(180, ["Tan"],                              ["tan"]),
    Ansi(181, ["MistyRose3"],                       ["mistyrose3"]),
    Ansi(182, ["Thistle3"],                         ["thistle3"]),
    Ansi(183, ["Plum2"],                            ["plum2"]),
    Ansi(184, ["Yellow3"],                          ["yellow3"]),
    Ansi(185, ["Khaki3"],                           ["khaki3"]),
    Ansi(186, ["LightGoldenrod2"],                  ["lightgoldenrod2"]),
    Ansi(187, ["LightYellow3"],                     ["lightyellow3"]),
    Ansi(188, ["Grey84", "Gray84"],                 ["grey84", "gray84"]),
    Ansi(189, ["LightSteelBlue1"],                  ["lightsteelblue1"]),
    Ansi(190, ["Yellow2"],                          ["yellow2"]),
    Ansi(191, ["DarkOliveGreen1"],                  ["darkolivegreen1"]),
    Ansi(192, ["DarkOliveGreen1"],                  ["darkolivegreen1"]),
    Ansi(193, ["DarkSeaGreen1"],                    ["darkseagreen1"]),
    Ansi(194, ["Honeydew2"],                        ["honeydew2"]),
    Ansi(195, ["LightCyan1"],                       ["lightcyan1"]),
    Ansi(196, ["Red1"],                             ["red1"]),
    Ansi(197, ["DeepPink2"],                        ["deeppink2"]),
    Ansi(198, ["DeepPink1"],                        ["deeppink1"]),
    Ansi(199, ["DeepPink1"],                        ["deeppink1"]),
    Ansi(200, ["Magenta2"],                         ["magenta2"]),
    Ansi(201, ["Magenta1"],                         ["magenta1"]),
    Ansi(202, ["OrangeRed1"],                       ["orangered1"]),
    Ansi(203, ["IndianRed1"],                       ["indianred1"]),
    Ansi(204, ["IndianRed1"],                       ["indianred1"]),
    Ansi(205, ["HotPink"],                          ["hotpink"]),
    Ansi(206, ["HotPink"],                          ["hotpink"]),
    Ansi(207, ["MediumOrchid1"],                    ["mediumorchid1"]),
    Ansi(208, ["DarkOrange"],                       ["darkorange"]),
    Ansi(209, ["Salmon1"],                          ["salmon1"]),
    Ansi(210, ["LightCoral"],                       ["lightcoral"]),
    Ansi(211, ["PaleVioletRed1"],                   ["palevioletred1"]),
    Ansi(212, ["Orchid2"],                          ["orchid2"]),
    Ansi(213, ["Orchid1"],                          ["orchid1"]),
    Ansi(214, ["Orange1"],                          ["orange1"]),
    Ansi(215, ["SandyBrown"],                       ["sandybrown"]),
    Ansi(216, ["LightSalmon1"],                     ["lightsalmon1"]),
    Ansi(217, ["LightPink1"],                       ["lightpink1"]),
    Ansi(218, ["Pink1"],                            ["pink1"]),
    Ansi(219, ["Plum1"],                            ["plum1"]),
    Ansi(220, ["Gold1"],                            ["gold1"]),
    Ansi(221, ["LightGoldenrod2"],                  ["lightgoldenrod2"]),
    Ansi(222, ["LightGoldenrod2"],                  ["lightgoldenrod2"]),
    Ansi(223, ["NavajoWhite1"],                     ["navajowhite1"]),
    Ansi(224, ["MistyRose1"],                       ["mistyrose1"]),
    Ansi(225, ["Thistle1"],                         ["thistle1"]),
    Ansi(226, ["Yellow1"],                          ["yellow1"]),
    Ansi(227, ["LightGoldenrod1"],                  ["lightgoldenrod1"]),
    Ansi(228, ["Khaki1"],                           ["khaki1"]),
    Ansi(229, ["Wheat1"],                           ["wheat1"]),
    Ansi(230, ["Cornsilk1"],                        ["cornsilk1"]),
    Ansi(231, ["Grey100", "Gray100"],               ["grey100", "gray100"]),
    Ansi(232, ["Grey3", "Gray3"],                   ["grey3", "gray3"]),
    Ansi(233, ["Grey7", "Gray7"],                   ["grey7", "gray7"]),
    Ansi(234, ["Grey11", "Gray11"],                 ["grey11", "gray11"]),
    Ansi(235, ["Grey15", "Gray15"],                 ["grey15", "gray15"]),
    Ansi(236, ["Grey19", "Gray19"],                 ["grey19", "gray19"]),
    Ansi(237, ["Grey23", "Gray23"],                 ["grey23", "gray23"]),
    Ansi(238, ["Grey27", "Gray27"],                 ["grey27", "gray27"]),
    Ansi(239, ["Grey30", "Gray30"],                 ["grey30", "gray30"]),
    Ansi(240, ["Grey35", "Gray35"],                 ["grey35", "gray35"]),
    Ansi(241, ["Grey39", "Gray39"],                 ["grey39", "gray39"]),
    Ansi(242, ["Grey42", "Gray42"],                 ["grey42", "gray42"]),
    Ansi(243, ["Grey46", "Gray46"],                 ["grey46", "gray46"]),
    Ansi(244, ["Grey50", "Gray50"],                 ["grey50", "gray50"]),
    Ansi(245, ["Grey54", "Gray54"],                 ["grey54", "gray54"]),
    Ansi(246, ["Grey58", "Gray58"],                 ["grey58", "gray58"]),
    Ansi(247, ["Grey62", "Gray62"],                 ["grey62", "gray62"]),
    Ansi(248, ["Grey66", "Gray66"],                 ["grey66", "gray66"]),
    Ansi(249, ["Grey70", "Gray70"],                 ["grey70", "gray70"]),
    Ansi(250, ["Grey74", "Gray74"],                 ["grey74", "gray74"]),
    Ansi(251, ["Grey78", "Gray78"],                 ["grey78", "gray78"]),
    Ansi(252, ["Grey82", "Gray82"],                 ["grey82", "gray82"]),
    Ansi(253, ["Grey85", "Gray85"],                 ["grey85", "gray85"]),
    Ansi(254, ["Grey89", "Gray89"],                 ["grey89", "gray89"]),
    Ansi(255, ["Grey93", "Gray93"],                 ["grey93", "gray93"])
]

_FG_ESC = "\x1b[38;5;{}m"
_BG_ESC = "\x1b[48;5;{}m"

R = RESET = "\x1b[0m"

B = BOLD = "\x1b[1m"
U = UNDERLINED = "\x1b[4m"
I = INVISIBLE = "\x1b[8m"


# errors
class EscapeError(Exception):
    pass

class BetaError(Exception):
    pass

class UnknownClassError(Exception):
    pass

# classes
# syntax
class Syntax:
    class Default:
        legal_escape = "%\\$=;"
        def process(obj, escape_char = None):
            if isinstance(obj, str):
                string = obj.replace("\n", escape_char + "n")
                obj = Powerstring(f"""
                    {string}
                """, escape = escape_char, syntax = Syntax.Default)
            string = obj.text
            
            no_sqbr = "[^\[\]]*?" # square brackets
            highlight_template_pattern = lambda symbol: fr"({obj.rescape}*)({re.escape(symbol)}{{2}}(?P<text>.+?){re.escape(symbol)}{{2}})"
            
            ## singleline comments
            pattern = fr" ?({obj.rescape}*)(//.*)$"
            flags = re.MULTILINE
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped and escape_char else "") + m.group()
                ) if escape_char or not obj.show_comments else (
                    lambda m: "" if not _check_escape(m.group(1)).is_escaped else m.group()
                ),
                string,
                flags = flags
            )
            
            ## multiline comments
            pattern = fr" ?({obj.rescape}*)(/\*.*?\*/) ?"
            flags = re.DOTALL
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    lambda m: "" if not _check_escape(m.group(1)).is_escaped else m.group()
                ),
                string,
                flags = flags
            )
            
            ## selected text
            pattern = fr"({obj.rescape}*)(\[(?P<text>{no_sqbr})\]\((?P<classes>[\w +-]*)\))"
            flags = re.ASCII
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    text = m.group("text")
                    this_classes = m.group("classes").split(" ")
                    style = ""
                    for class_ in this_classes:
                        emptymatch = re.fullmatch(r"\s|", class_)
                        colormatch = re.match(r"^(\+|-)(.+)", class_)
                        if colormatch:
                            style += color(colormatch.group(2), 0 if colormatch.group(1) == "+" else 1)
                            continue
                        if not emptymatch:
                            class_value = classes.get(class_)
                            if class_value == None:
                                raise UnknownClassError(f"Unknown class '{class_}'")
                            style += class_value
                    return style + text + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string,
                flags = flags
            )
            
            ## selected text short
            pattern = fr"({obj.rescape}*)(\[(?P<text>{no_sqbr})\](?P<highlight>[!+i]))"
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    text = m.group("text")
                    highlight = m.group("highlight")
                    if highlight == "!":
                        style = color(9)
                    elif highlight == "+":
                        style = color(226, 1)
                    else:
                        style = color(45)
                    return style + text + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            # title
            pattern = fr"({obj.rescape}*)(\[ ?(?P<text>{no_sqbr}) ?\])"
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return BOLD + UNDERLINED + color("Olive") + m.group("text") + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## horizontal rule
            pattern = fr"^[ \t]*({obj.rescape}*)[*_-]{{3,}}[ \t]*$"
            flags = re.MULTILINE
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return "\N{EM DASH}" * tw()
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string,
                flags = flags
            )
            
            ## bold text
            pattern = highlight_template_pattern("*")
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return BOLD + m.group("text") + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## underlined text
            pattern = highlight_template_pattern("_")
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return UNDERLINED + m.group("text") + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## bold + underlined
            pattern = highlight_template_pattern("^")
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return UNDERLINED + BOLD + m.group("text") + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## invisible text
            pattern = highlight_template_pattern("~")
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return INVISIBLE + m.group("text") + RESET
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## emoji
            #! add escape func
            string = emojize(string)
            
            ## icons
            pattern = fr"({obj.rescape}*)(\((?P<icon>[x!?i])\))"
            flags = re.IGNORECASE
            def repl(m):
                if not _check_escape(m.group(1)).is_escaped:
                    return {
                        "x": emojize(":cross_mark:"),
                        "i": emojize(":information:"),
                        "?": emojize(":red_question_mark:"),
                        "!": emojize(":warning:")
                    }[m.group("icon")]
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string,
                flags = flags
            )
            
            ## hashtag
            pattern = fr"(\W)({obj.rescape}*)(#[a-zA-Z]+(\w?a)*)(\W)"
            def repl(m):
                if not _check_escape(m.group(2)).is_escaped:
                    return m.group(1) + UNDERLINED + m.group(3) + RESET + m.group(5)
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if not _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            # newline
            pattern = fr"({obj.rescape}*)n"
            def repl(m):
                if _check_escape(m.group(1)).is_escaped:
                    return "\n"
                return m.group()
            string = re.sub(
                pattern,
                (
                    lambda m: (escape_char if _check_escape(m.group(1)).is_escaped else "") + m.group()
                ) if escape_char else (
                    repl
                ),
                string
            )
            
            ## escapes
            #! add escape func
            pattern = fr"{obj.rescape}*"
            string = re.sub(
                pattern,
                lambda m: _check_escape(m.group()).out,
                string
            )
            
            return string
        


class Powerstring:
    def __init__(
        self,
        string: str,
        start_line: typing.Union[str, bool] = "auto",
        escape: str = "%",
        join: str = "\n",
        remove_empty_lines: bool = False,
        show_comments: bool = False,
        align: typing.Union[int, str, None] = None,
        syntax: typing.Optional[typing.Callable] = Syntax.Default,
        **kwargs
    ):
        self.syntax = syntax
        self.start_line = start_line
        self.show_comments = show_comments
        self.remove_empty_lines = remove_empty_lines
        self.escape = escape
        self.rescape = re.escape(escape)
        self.kwargs = kwargs
        
        if "\n" in string:
            meta, content = string.split("\n", 1)
            if meta.startswith(" "):
                meta = meta[1::]
            content = content[:content.rfind("\n")] # remove last line
            try:
                self.title, self.description = meta.split(" -- ")
            except ValueError:
                self.title = meta if meta else None
                self.description = None
        else:
            self.title = None
            self.description = None
            content = string
        
        if len(escape) != 1:
            raise EscapeError(
                "Escape symbol must be exactly one character long."
            )
        if escape not in syntax.legal_escape:
            raise EscapeError(
                f"Only following symbols are allowed for escaping: {syntax.legal_escape}"
            )
        
        self.lines = []
        minspace = len(min(re.findall("^[ \t]*", content, flags = re.M)))
        for line in content.split("\n"):
            if not (self.remove_empty_lines and line == ""):
                if start_line == "auto":
                    self.lines.append(line[minspace::])
                elif start_line:
                    m = re.match(f"^[ \t]*{re.escape(start_line)}", line)
                    if m:
                        pos = m.span()[1]
                        self.lines.append(line[pos::])
                else: # "" or False
                    self.lines.append(line)
        
        '''
        for line in self.lines:
            m = re.match(r"^\?: opt.(?P<arg>[^\.\s]+?) (?P<type>.+?)$", line, flags = re.M)
            if m:
                self.lines.remove(self.lines.index(line))
        '''
        
        self.text = join.join(self.lines)
    def add(self, string: str) -> None:
        for l in string.split("\n"):
            self.lines.append(l)
        self.text += string
    def addline(self, string: str) -> None:
        string = string.replace("\n", " ")
        self.lines.append(string)
        self.text = self.text + string
    def to_markdown(self) -> str:
        beta_error()
    def __str__(self) -> str:
        return self.syntax.process(self)



# functions
def beta_error():
    raise BetaError("Function or method not availbale in this beta version.")

def basic(string: str) -> str:
    """Returns formatted emphasized string."""
    string = string.replace("\n", "\\n")
    return Powerstring(f"""
        {string}
    """, syntax = Syntax.basic, escape = "\\")

def _check_escape(escapes):
    halflength = round(len(escapes) / 2)
    escaped = namedtuple("escaped", ["is_escaped", "out"])
    try:
        symbol = escapes[0]
    except IndexError:
        return escaped(False, None)
    return escaped(
        len(escapes) % 2 != 0, # False if even (not escaped); True if odd (escaped)
        symbol if halflength in (0, 1) else symbol * halflength
    )

def color(
    value: typing.Union[str,int],
    position: typing.Union[str, int] = "fg"
) -> str:
    """Returns an ansi sequence with a given color."""
    position = str(position).lower()
    fg = ["0", "fg", "foreground"]
    bg = ["1", "bg", "background"]
    for c in COLORS:
        if str(value).lower() in (*c.lcase, c.id):
            if position in fg:
                return _FG_ESC.format(c.id)
            elif position in bg:
                return _BG_ESC.format(c.id)
    if position in fg:
        return _FG_ESC.format(value)
    elif position in bg:
        return _BG_ESC.format(value)

def colors():
    print(str(Powerstring("""
        ---
        [ ALL COLORS ]
        
    """)))
    print("\n".join([str(Powerstring("""
        **{: >3} | {}**
        {}
        {}
        
    """.format(*tuple([
        c.id, " / ".join(c.name),
        _FG_ESC.format(c.id) + " / ".join(c.name) + RESET,
        _BG_ESC.format(c.id) + " / ".join(c.name) + RESET
    ])))) for c in COLORS]))

def colored(
    string: str,
    classes_: typing.Union[str, typing.List[str]] = [],
    fg: _TYPE_COLOR = None,
    bg: _TYPE_COLOR = None,
) -> str:
    """beta_error()ed string gets returned with given colors and styles."""
    fore = "" if fg == None else color(fg, 0)
    back = "" if bg == None else color(bg, 1)
    pre = ""
    if isinstance(classes_, str):
        classes_ = classes_.split(" ")
    for c in classes_:
        if c in classes:
            pre += classes[c]
    return pre + fore + back + string + RESET

def convert_vowels(string: str) -> str:
    """Converts diacritic letters within a stting to their orgin letter."""
    for k, v in _DIACRITIC.items():
        string = string.replace(k, v)
    return string

def contains_numeric(
    string: str,
    commas: typing.List[str] = ["."],
    abstract: bool = False # allows π, ∞, ...
) -> typing.Tuple[bool, typing.List[typing.Union[str, int, float]]]:
    """Checks if a string contains a numeric substring."""
    beta_error()

def printc(
    string: str,
    classes_: typing.Union[str, typing.List[str]] = [],
    fg: _TYPE_COLOR = None,
    bg: _TYPE_COLOR = None
) -> None:
    """beta_error()ed string gets printed with given colors and styles."""
    print(colored(
        string,
        classes_,
        fg,
        bg
    ))
cprint = printc

def escape(
    string: str,
    escape_char: str = "%",
    syntax: typing.Callable = Syntax.Default
) -> str:
    return syntax.process(string, escape_char)

def get_8bit(
    color: typing.Union[str, typing.Tuple[int, int, int]],
    position: typing.Union[str, int] = "fg"
) -> int:
    """Get 8bit color value of either hex, rgb or hls or hsv."""
    beta_error()

def hr():
    """Return horizontal rule."""
    return "\N{EM DASH}" * tw()

def is_numeric(
    string: str,
    commas: typing.List[str] = ["."],
    abstract: bool = False # allows π, ∞, ...
) -> bool:
    """Checks if a string is numeric."""
    beta_error()

def progress(steps: int, rounded: int = 0) -> typing.Iterator[str]:
    """Creates a progress counter."""
    for step in range(1, steps + 1):
        percentage = step / steps * 100
        if rounded >= 0: percentage = round(percentage, rounded)
        yield percentage
    #yield 100.

def replace_all(
    string: str,
    chain: bool = False,
    case_sensitive: bool = True,
    *substrings: typing.Tuple[str, str]
) -> str:
    """Replaces all given substrings within a string."""
    beta_error()
    if chain:
        for pair in substrings:
            string = re.sub(*pair, string, flags = re.I if case_sensitive else None)

def swap(
    string: str,
    *substrings: typing.Tuple[str, str]
) -> str:
    """Swaps all given substrings within a string."""
    for sub in substrings:
        value1, value2 = re.escape(sub[0]), re.escape(sub[1])
        string = re.sub(fr"(value1)(.*?)(value2)", r"\3\2\1", string)
    return string

def textify(array: typing.List[str], join: str = "and") -> str:
    """Turns list to a text list."""
    return ", ".join(array[0:-1]) + join + " " + array[-1]

def lenvisible(string: str) -> int:
    """Rerurns visible length of a string."""
    return len(re.sub(
        r"\\x1b\[.+?m",
        "",
        repr(string)
    )) - 2 # remove quotes

classes = {
    **dict.fromkeys(["bold", "b"], BOLD),
    **dict.fromkeys(["underlined", "underline", "ul", "u"], UNDERLINED),
    **dict.fromkeys(["invisible", "hidden", "inv", "i", "hide"], INVISIBLE),
    **dict.fromkeys(["link", "url"], color(45)),
    **dict.fromkeys(["warn", "warning"], color(88)),
    **dict.fromkeys(["mark", "highlight", "hl"], color(11, 1))
}

class Symbols:
    arrowleft = larrow = "\N{LEFTWARDS ARROW}" # ←
    arrowright = rarrow = "\N{RIGHTWARDS ARROW}" # →
    calender = "\N{MUSICAL SYMBOL SIX-STRING FRETBOARD}"
    dashline = hr = dl = "\N{EM DASH}" * tw()
    lorem = loremipsum = "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    loremtitle = loremt = slorem = shortlorem = "Lorem ipsum dolor sit amet"
    music_wholenote = "\N{MUSICAL SYMBOL WHOLE NOTE}"
    music_halfnote = "\N{MUSICAL SYMBOL HALF NOTE}"
    music_quarternote = "\N{MUSICAL SYMBOL QUARTER NOTE}"
    music_eightnote = "\N{MUSICAL SYMBOL EIGHTH NOTE}"
    music_sixteenthnote = "\N{MUSICAL SYMBOL SIXTEENTH NOTE}"
    music_thirtysecondnote = "\N{MUSICAL SYMBOL THIRTY-SECOND NOTE}"
    music_sixtyfourthnote = "\N{MUSICAL SYMBOL SIXTY-FOURTH NOTE}"
    music_onehundredtwentyeightnote = "\N{MUSICAL SYMBOL ONE HUNDRED TWENTY-EIGHTH NOTE}"
    pi = "\N{GREEK SMALL LETTER PI}"
    pow0 = exp0 = "\N{SUPERSCRIPT ZERO}" 
    pow1 = exp1 = "\N{SUPERSCRIPT ONE}"
    pow2 = exp2 = "\N{SUPERSCRIPT TWO}"
    pow3 = exp3 = "\N{SUPERSCRIPT THREE}"
    pow4 = exp4 = "\N{SUPERSCRIPT FOUR}"
    pow5 = exp5 = "\N{SUPERSCRIPT FIVE}"
    pow6 = exp6 = "\N{SUPERSCRIPT SIX}"
    pow7 = exp7 = "\N{SUPERSCRIPT SEVEN}"
    pow8 = exp8 = "\N{SUPERSCRIPT EIGHT}"
    pow9 = exp9 = "\N{SUPERSCRIPT NINE}"
    rose = "\N{MUSICAL SYMBOL PEDAL UP MARK}"
    dot_red = color(9) + "\u00B7" + RESET
    dot_yellow = color(11) + "\u00B7" + RESET
    dot_green = color(2) + "\u00B7" + RESET
    dot_gray = dot_grey = color(8) + "\u00B7" + RESET


if __name__ == "__main__":
    def getvars(class_):
        s = Powerstring("")
        s.add("\n".join(sorted([f"[{i[0]}](b +68)\n[{i[1]}](+81)\n" for i in class_.__dict__.items() if not (i[0].startswith("__") and i[0].endswith("__"))])))
        return str(s)
    print(getvars(Symbols))
    print(list(classes.keys()))
    colors()