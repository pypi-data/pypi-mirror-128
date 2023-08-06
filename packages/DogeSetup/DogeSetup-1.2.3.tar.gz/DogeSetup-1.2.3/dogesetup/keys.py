# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
AI1 = "11416026"
AH1 = "ace27a0cbb553967a7547ce52b7db0d8"

AI2 = "16694326"
AH2 = "49d18b635ae8cb80fff46250dd0fd7f4"

AI3 = "6568116"
AH3 = "0c502e0f7128adc29e721d7e8cde9498"


def random_choice():
    from random import choice

    AI, AH = choice(((AI1, AH1), (AI2, AH2), (AI3, AH3)))

    return AI, AH
