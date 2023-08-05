# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import loads
from os.path import dirname, join, realpath

from . import Panel, Prompt, logo, name, p_ask, p_lang, system, timedelta, tzinfo

languages_folder = join(dirname(realpath(__file__)), "languages")


class Zone(tzinfo):
    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name


def importlanguages():
    if name == "nt":
        system("cls")
    else:
        system("clear")
    logo()

    p_lang(f"[1] [bold red]TÜRK[/][bold white]ÇE")
    p_lang(f"[2] [bold blue]ENG[/][bold white]LI[/][bold red]SH")

    p_ask(
        Panel(
            f"\n[bold yellow]🦴 Please write a language number:\n\n[bold yellow]🦴 Lütfen bir dil numarası yazın:\n"
        )
    )

    lng = Prompt.ask(f"🌍", choices=["1", "2"], default="1")

    if lng == "1":
        COUNTRY = "Turkey"
        DOGELANG = "tr"
        GMT = Zone(+3, False, "GMT")
        TZ = "Europe/Istanbul"
        TZ_NUMBER = "1"

    elif lng == "2":
        COUNTRY = "Britain"
        DOGELANG = "en"
        GMT = Zone(0, False, "GMT")
        TZ = "Europe/London"
        TZ_NUMBER = "1"

    return COUNTRY, DOGELANG, GMT, TZ, TZ_NUMBER


COUNTRY, DOGELANG, GMT, TZ, TZ_NUMBER = importlanguages()

LAN = loads(open(f"{languages_folder}/{DOGELANG}.json.py", "r").read())["STRINGS"]
