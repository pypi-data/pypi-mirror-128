# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2021 Alexsandro Thomas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .util.bundle import Bundle
from functools import cache

def plain_positive_nonpast(word) :
    return word

@cache
def plain_positive_past(word) :
    return word[:-1]+"かった"

def plain_positive_presumptive(word) :
    return word+"だろう"

def plain_positive_ba_conditional(word) :
    return word[:-1]+"ければ"

def plain_positive_te_form(word) :
    return word[:-1]+"くて"

@cache
def plain_negative_nonpast(word) :
    return word[:-1]+"くない"

def plain_negative_past(word) :
    return plain_positive_past(plain_negative_nonpast(word))

def plain_negative_presumptive(word) :
    return plain_positive_presumptive(plain_positive_past(word))

def plain_negative_ba_conditional(word) :
    return plain_positive_ba_conditional(plain_positive_past(word))

def plain_negative_te_form(word) :
    return plain_positive_te_form(plain_negative_nonpast(word))

def polite_positive_nonpast(word) :
    return word+"です"

def polite_positive_past(word) :
    return polite_positive_nonpast(plain_positive_past(word))

def polite_positive_presumptive(word) :
    return word+"でしょう"

@cache
def polite_negative_nonpast(word) :
    return word[:-1]+"くありません"

def polite_negative_past(word) :
    return polite_negative_nonpast(word)+"でした"

def polite_negative_presumptive(word) :
    return polite_positive_presumptive(plain_negative_nonpast(word))

lookup = Bundle(
    plain = Bundle(
        positive = Bundle(
            nonpast = plain_positive_nonpast,
            past = plain_positive_past,
            presumptive = plain_positive_presumptive,
            ba_conditional = plain_positive_ba_conditional,
            te_form = plain_positive_te_form
        ),
        negative = Bundle(
            nonpast = plain_negative_nonpast,
            past = plain_negative_past,
            presumptive = plain_negative_presumptive,
            ba_conditional = plain_negative_ba_conditional,
            te_form = plain_negative_te_form
        )
    ),

    polite = Bundle(
        positive = Bundle(
            nonpast = polite_positive_nonpast,
            past = polite_positive_past,
            presumptive = polite_positive_presumptive
        ),
        negative = Bundle(
            nonpast = polite_negative_nonpast,
            past = polite_negative_past,
            presumptive = polite_negative_presumptive
        )
    )
)
