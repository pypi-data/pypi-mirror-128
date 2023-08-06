# -*- encoding: utf-8 -*-
# modint v0.4.0
# Python implementation of the Chinese Remainder algorithm
# Copyright © 2018, Shlomi Fish.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Python implementation of the Chinese Remainder algorithm

:Copyright: © 2018, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__title__ = 'modint'
__version__ = '0.4.0'
__author__ = 'Shlomi Fish'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# import gettext
# G = gettext.translation('modint', '/usr/share/locale', fallback='C')
# _ = G.gettext
# -*- coding: utf-8 -*-

__author__ = """Shlomi Fish"""
__email__ = 'shlomif@shlomifish.org'
__version__ = '0.1.0'


class ChineseRemainderConstructor:
    """Synopsis:

from modint import ChineseRemainderConstructor, chinese_remainder

cr = ChineseRemainderConstructor([2, 5])
assert cr.rem([1, 0]) == 5
assert cr.rem([0, 3]) == 8

# Convenience function
assert chinese_remainder([2, 3, 7], [1, 2, 3]) == 17
    """
    def __init__(self, bases):
        """Accepts a list of integer bases."""
        self._bases = bases
        p = 1
        for x in bases:
            p *= x
        self._prod = p
        self._inverses = [p//x for x in bases]
        self._muls = [inv * self.mul_inv(inv, base) for base, inv
                      in zip(self._bases, self._inverses)]

    def rem(self, mods):
        """Accepts a list of corresponding modulos for the bases and
        returns the accumulated modulo.
        """
        ret = 0
        for mul, mod in zip(self._muls, mods):
            ret += mul * mod
        return ret % self._prod

    def mul_inv(self, a, b):
        """Internal method that implements Euclid's modified gcd algorithm.
        """
        initial_b = b
        x0, x1 = 0, 1
        if b == 1:
            return 1
        while a > 1:
            div, mod = divmod(a, b)
            a, b = b, mod
            x0, x1 = x1 - div * x0, x0
        return (x1 if x1 >= 0 else x1 + initial_b)


def chinese_remainder(n, mods):
    """Convenience function that calculates the chinese remainder directly."""
    return ChineseRemainderConstructor(n).rem(mods)


def invmod(base, mod):
    """
    invmod(base=base, mod=mod) * mod % base == 1

    Modular multiplicative Inverse convenience function. See:

    https://stackoverflow.com/questions/4798654/

    (Added in v0.4.0)
    """
    return chinese_remainder([base, mod], [1, 0]) // mod
