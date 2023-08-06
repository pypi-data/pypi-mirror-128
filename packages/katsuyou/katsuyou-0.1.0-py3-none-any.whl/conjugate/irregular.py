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

#為る, する
SURU = lambda word : Bundle(
    stem = Bundle(
        neutral = Bundle(
            te_form = word[:-2]+("為" if word[-2]=="為" else "し")+"て",
            i_stem = word[:-2]+("為" if word[-2]=="為" else "し"),
        )
    ),
    plain = Bundle(
        positive = Bundle(
            nonpast = word[:-2]+("為" if word[-2]=="為" else "す")+"る",
            past = word[:-2]+("為" if word[-2]=="為" else "し")+"た",
            optative = word[:-2]+("為" if word[-2]=="為" else "し")+"たい",
            past_optative = word[:-2]+("為" if word[-2]=="為" else "し")+"たかった",
            optative_te_form = word[:-2]+("為" if word[-2]=="為" else "し")+"たくて",
            volitional = word[:-2]+("為" if word[-2]=="為" else "し")+"よう",
            ba_conditional = word[:-2]+("為" if word[-2]=="為" else "す")+"れば",
            tara_conditional = word[:-2]+("為" if word[-2]=="為" else "し")+"たら",
            receptive = word[:-2]+("為" if word[-2]=="為" else "さ")+"れる",
            causative = word[:-2]+("為" if word[-2]=="為" else "さ")+"せる",
            potential = word[:-2]+("出来" if word[-2]=="為" else "でき")+"る",
            imperative = word[:-2]+("為" if word[-2]=="為" else "し")+"ろ",
            progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ている",
            past_progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていた",
            past_presumptive = word[:-2]+("為" if word[-2]=="為" else "し")+"たろう"
        ),
        negative = Bundle(
            nonpast = word[:-2]+("為" if word[-2]=="為" else "し")+"ない",
            past = word[:-2]+("為" if word[-2]=="為" else "し")+"なかった",
            optative = word[:-2]+("為" if word[-2]=="為" else "し")+"たくない",
            past_optative = word[:-2]+("為" if word[-2]=="為" else "し")+"たくなかった",
            optative_te_form = word[:-2]+("為" if word[-2]=="為" else "し")+"たくなくて",
            ba_conditional = word[:-2]+("為" if word[-2]=="為" else "し")+"なければ",
            tara_conditional = word[:-2]+("為" if word[-2]=="為" else "し")+"なかったら",
            receptive = word[:-2]+("為" if word[-2]=="為" else "さ")+"れない",
            causative = word[:-2]+("為" if word[-2]=="為" else "さ")+"せない",
            potential = word[:-2]+("出来" if word[-2]=="為" else "でき")+"ない",
            imperative = word[:-2]+("為" if word[-2]=="為" else "す")+"るな",
            progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていない",
            past_progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていなかった"
        )
    ),

    polite = Bundle(
        positive = Bundle(
            nonpast = word[:-2]+("為" if word[-2]=="為" else "し")+"ます",
            past = word[:-2]+("為" if word[-2]=="為" else "し")+"ました",
            volitional = word[:-2]+("為" if word[-2]=="為" else "し")+"ましょう",
            tara_conditional = word[:-2]+("為" if word[-2]=="為" else "し")+"ましたら",
            receptive = word[:-2]+("為" if word[-2]=="為" else "さ")+"れます",
            causative = word[:-2]+("為" if word[-2]=="為" else "さ")+"せます",
            potential = word[:-2]+("為" if word[-2]=="為" else "さ")+"れます",
            progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ています",
            past_progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていました"
        ),
        negative = Bundle(
            nonpast = word[:-2]+("為" if word[-2]=="為" else "し")+"ません",
            past = word[:-2]+("為" if word[-2]=="為" else "し")+"ませんでした",
            optative = word[:-2]+("為" if word[-2]=="為" else "し")+"たくありませんでした",
            tara_conditional = word[:-2]+("為" if word[-2]=="為" else "し")+"ませんでしたら",
            receptive = word[:-2]+("為" if word[-2]=="為" else "さ")+"れません",
            causative = word[:-2]+("為" if word[-2]=="為" else "さ")+"せません",
            potential = word[:-2]+("為" if word[-2]=="為" else "さ")+"れません",
            imperative = word[:-2]+("為" if word[-2]=="為" else "し")+"ないで",
            progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていません",
            past_progressive = word[:-2]+("為" if word[-2]=="為" else "し")+"ていました"
        )
    )
)
