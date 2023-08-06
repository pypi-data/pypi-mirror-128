#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from randomgen.aes import AESCounter
from rtt_data_gen.spreader import rand_gen_alpha, RGeneratorPCG

SEED = b'00112233'
MOD = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001


class SpreaderTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SpreaderTests, self).__init__(*args, **kwargs)

    def test_rand_alpha(self):
        gen = RGeneratorPCG(SEED, cls=AESCounter, cls_kw={'mode': 'sequence'})
        gen_alpha = rand_gen_alpha(4, gen, MOD, 16)
        for ix, val in enumerate(gen_alpha):
            if ix > 100:
                break

        gen_alpha = rand_gen_alpha(3, gen, MOD, 16)
        for ix, val in enumerate(gen_alpha):
            if ix > 100:
                break


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
