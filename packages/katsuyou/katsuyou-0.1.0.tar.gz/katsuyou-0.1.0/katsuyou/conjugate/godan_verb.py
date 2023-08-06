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
from . import i_adjective, ichidan_verb
from functools import cache

@cache
def stem_neutral_te_form(word:str) :
    if word=="行く" or word=="いく" :
        return word[:-1]+"って"
    translate = {
        "く": "いて",
        "ぐ": "いで",
        "す": "して",
        "ぶ": "んで",
        "む": "んで",
        "ぬ": "んで",
        "う": "って",
        "つ": "って",
        "る": "って"
    }
    return word[:-1]+translate[word[-1]]

@cache
def stem_neutral_a_stem(word:str) :
    translate = {
        "く": "か",
        "ぐ": "が",
        "す": "さ",
        "ぶ": "ば",
        "む": "ま",
        "ぬ": "な",
        "う": "わ",
        "つ": "た",
        "る": "ら"
    }
    return word[:-1]+translate[word[-1]]

@cache
def stem_neutral_i_stem(word:str) :
    if word=="御座る" or word=="ござる" :
        return word[:-1]+"い"
    translate = {
        "く": "き",
        "ぐ": "ぎ",
        "す": "し",
        "ぶ": "び",
        "む": "み",
        "ぬ": "に",
        "う": "い",
        "つ": "ち",
        "る": "り"
    }
    return word[:-1]+translate[word[-1]]

@cache
def stem_neutral_e_stem(word:str) :
    translate = {
        "く": "け",
        "ぐ": "げ",
        "す": "せ",
        "ぶ": "べ",
        "む": "め",
        "ぬ": "ね",
        "う": "え",
        "つ": "て",
        "る": "れ"
    }
    return word[:-1]+translate[word[-1]]

@cache
def stem_neutral_o_stem(word:str) :
    translate = {
        "く": "こ",
        "ぐ": "ご",
        "す": "そ",
        "ぶ": "ぼ",
        "む": "も",
        "ぬ": "の",
        "う": "お",
        "つ": "と",
        "る": "ろ"
    }
    return word[:-1]+translate[word[-1]]

def plain_positive_nonpast(word:str) :
    return word

@cache
def plain_positive_past(word:str) :
    translate = {
        "て": "た",
        "で": "だ"
    }
    stem = stem_neutral_te_form(word)
    return stem[:-1]+translate[stem[-1]]

@cache
def plain_positive_optative(word:str) :
    return stem_neutral_i_stem(word)+"たい"

def plain_positive_past_optative(word:str) :
    return i_adjective.plain_positive_past(plain_positive_optative(word))

def plain_positive_optative_te_form(word:str) :
    return i_adjective.plain_positive_te_form(plain_positive_optative(word))

def plain_positive_volitional(word:str) :
    return stem_neutral_o_stem(word)+"う"

@cache
def plain_positive_ba_conditional(word:str) :
    return stem_neutral_e_stem(word)+"ば"

def plain_positive_tara_conditional(word:str) :
    return plain_positive_past(word)+"ら"

@cache
def plain_positive_receptive(word:str) :
    return stem_neutral_a_stem(word)+"れる"

@cache
def plain_positive_causative(word:str) :
    return stem_neutral_a_stem(word)+"せる"

@cache
def plain_positive_potential(word:str) :
    return stem_neutral_e_stem(word)+"る"

def plain_positive_imperative(word:str) :
    return stem_neutral_e_stem(word)

@cache
def plain_positive_progressive(word:str) :
    return stem_neutral_te_form(word)+"いる"

def plain_positive_past_progressive(word:str) :
    return ichidan_verb.plain_positive_past(plain_positive_progressive(word))

def plain_positive_past_presumptive(word:str) :
    return plain_positive_past(word)+"ろう"

@cache
def plain_negative_nonpast(word:str) :
    return stem_neutral_a_stem(word)+"ない"

@cache
def plain_negative_past(word:str) :
    return i_adjective.plain_positive_past(plain_negative_nonpast(word))

@cache
def plain_negative_optative(word:str) :
    return i_adjective.plain_negative_nonpast(plain_positive_optative(word))

def plain_negative_past_optative(word:str) :
    return i_adjective.plain_negative_past(plain_positive_optative(word))

def plain_negative_optative_te_form(word:str) :
    return i_adjective.plain_negative_te_form(plain_positive_optative(word))

def plain_negative_ba_conditional(word:str) :
    return i_adjective.plain_positive_ba_conditional(plain_negative_past(word))

def plain_negative_tara_conditional(word:str) :
    return plain_negative_past(word)+"ら"

def plain_negative_receptive(word:str) :
    return ichidan_verb.plain_negative_nonpast(plain_positive_receptive(word))

def plain_negative_causative(word:str) :
    return ichidan_verb.plain_negative_nonpast(plain_positive_causative(word))

def plain_negative_potential(word:str) :
    return ichidan_verb.plain_negative_nonpast(plain_positive_potential(word))

def plain_negative_imperative(word:str) :
    return word+"な"

def plain_negative_progressive(word:str) :
    return ichidan_verb.plain_negative_nonpast(plain_positive_progressive(word))

def plain_negative_past_progressive(word:str) :
    return ichidan_verb.plain_negative_past(plain_positive_progressive(word))

@cache
def polite_positive_nonpast(word:str) :
    return stem_neutral_i_stem(word)+"ます"

@cache
def polite_positive_past(word:str) :
    return plain_positive_past(polite_positive_nonpast(word))

def polite_positive_volitional(word:str) :
    return polite_positive_nonpast(word)[:-1]+"しょう"

def polite_positive_tara_conditional(word:str) :
    return polite_positive_past(word)+"ら"

def polite_positive_receptive(word:str) :
    return ichidan_verb.polite_positive_nonpast(plain_positive_receptive(word))

def polite_positive_causative(word:str) :
    return ichidan_verb.polite_positive_nonpast(plain_positive_causative(word))

def polite_positive_potential(word:str) :
    return ichidan_verb.polite_positive_nonpast(plain_positive_potential(word))

def polite_positive_progressive(word:str) :
    return ichidan_verb.polite_positive_nonpast(plain_positive_progressive(word))

def polite_positive_past_progressive(word:str) :
    return ichidan_verb.polite_positive_past(plain_positive_progressive(word))

@cache
def polite_negative_nonpast(word:str) :
    return polite_positive_nonpast(word)+"せん"

@cache
def polite_negative_past(word:str) :
    return polite_negative_nonpast(word)+"でした"

def polite_negative_optative(word:str) :
    return i_adjective.polite_negative_nonpast(plain_positive_optative(word))

def polite_negative_tara_conditional(word:str) :
    return polite_negative_past(word)+"ら"

def polite_negative_receptive(word:str) :
    return ichidan_verb.polite_negative_nonpast(plain_positive_receptive(word))

def polite_negative_causative(word:str) :
    return ichidan_verb.polite_negative_nonpast(plain_positive_causative(word))

def polite_negative_potential(word:str) :
    return ichidan_verb.polite_negative_nonpast(plain_positive_potential(word))

def polite_negative_imperative(word:str) :
    return plain_negative_nonpast(word)+"で"

def polite_negative_progressive(word:str) :
    return ichidan_verb.polite_negative_nonpast(plain_positive_progressive(word))

def polite_negative_past_progressive(word:str) :
    return ichidan_verb.polite_negative_past(plain_positive_progressive(word))

lookup = Bundle(
    stem = Bundle(
        neutral = Bundle(
            te_form = stem_neutral_te_form,
            a_stem = stem_neutral_a_stem,
            i_stem = stem_neutral_i_stem,
            e_stem = stem_neutral_e_stem,
            o_stem = stem_neutral_o_stem,
        )
    ),
    plain = Bundle(
        positive = Bundle(
            nonpast = plain_positive_nonpast,
            past = plain_positive_past,
            optative = plain_positive_optative,
            past_optative = plain_positive_past_optative,
            optative_te_form = plain_positive_optative_te_form,
            volitional = plain_positive_volitional,
            ba_conditional = plain_positive_ba_conditional,
            tara_conditional = plain_positive_tara_conditional,
            receptive = plain_positive_receptive,
            causative = plain_positive_causative,
            potential = plain_positive_potential,
            imperative = plain_positive_imperative,
            progressive = plain_positive_progressive,
            past_progressive = plain_positive_past_progressive,
            past_presumptive = plain_positive_past_presumptive
        ),
        negative = Bundle(
            nonpast = plain_negative_nonpast,
            past = plain_negative_past,
            optative = plain_negative_optative,
            past_optative = plain_negative_past_optative,
            optative_te_form = plain_negative_optative_te_form,
            ba_conditional = plain_negative_ba_conditional,
            tara_conditional = plain_negative_tara_conditional,
            receptive = plain_negative_receptive,
            causative = plain_negative_causative,
            potential = plain_negative_potential,
            imperative = plain_negative_imperative,
            progressive = plain_negative_progressive,
            past_progressive = plain_negative_past_progressive
        )
    ),

    polite = Bundle(
        positive = Bundle(
            nonpast = polite_positive_nonpast,
            past = polite_positive_past,
            volitional = polite_positive_volitional,
            tara_conditional = polite_positive_tara_conditional,
            receptive = polite_positive_receptive,
            causative = polite_positive_causative,
            potential = polite_positive_potential,
            progressive = polite_positive_progressive,
            past_progressive = polite_positive_past_progressive
        ),
        negative = Bundle(
            nonpast = polite_negative_nonpast,
            past = polite_negative_past,
            optative = polite_negative_optative,
            tara_conditional = polite_negative_tara_conditional,
            receptive = polite_negative_receptive,
            causative = polite_negative_causative,
            potential = polite_negative_potential,
            imperative = polite_negative_imperative,
            progressive = polite_negative_progressive,
            past_progressive = polite_negative_past_progressive
        )
    )
)
