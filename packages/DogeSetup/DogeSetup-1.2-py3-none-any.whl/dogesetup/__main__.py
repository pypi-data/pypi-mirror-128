# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import unlink
from os.path import exists, isdir, isfile, islink
from shutil import rmtree
from time import time

from git import Repo

from . import *
from .heroku import connect, createApp, hgit, opendyno
from .language import COUNTRY, DOGELANG, LAN, TZ, TZ_NUMBER
from .session import sessiongenerator

LAN = LAN["MAIN"]


logo(DOGELANG)
if name == "nt":
    system("cls")
else:
    system("clear")
logo(DOGELANG)
heroku, api = connect()

stringsession, appid, apihash = sessiongenerator()
p_success(f"✅ %34 ~ {LAN['SUCCESS_SESSION']}!")

timestart = time()
appname = createApp(heroku)

p_info(f"⏳ %55 ~ {LAN['GETTING_READY']}...")
dogepath = "./userbot/"
if isdir(dogepath):
    if not exists(dogepath):
        pass
    if isfile(dogepath) or islink(dogepath):
        unlink(dogepath)
    else:
        rmtree(dogepath)

p_info(f"📥 %62 ~ {LAN['DOWNLOADING']}...")
repo = Repo.clone_from("https://github.com/DOG-E/DogeStarter", dogepath, branch="DOGE")

p_important(f"[bold white]📤 %65 ~ {LAN['DEPLOYING']}.[/]")
app = hgit(heroku, repo, appname, api)

p_info(f"⏳ %85 ~ {LAN['WRITING_CONFIG']}...")
config = app.config()
config["API_HASH"] = apihash
config["APP_ID"] = str(appid)
config["COUNTRY"] = COUNTRY
config["DOGELANG"] = DOGELANG
config["ENV"] = "ANYTHING"
config["HEROKU_API_KEY"] = api
config["HEROKU_APP_NAME"] = appname
config["STRING_SESSION"] = stringsession
config["TZ"] = TZ
config["TZ_NUMBER"] = TZ_NUMBER
p_success(f"✅ %96 ~ {LAN['SUCCESS_CONFIG']}!")

opendyno(app)

timeend = round(time() - timestart)
if name == "nt":
    system("cls")
else:
    system("clear")
logo(DOGELANG)
console.print(
    Panel(
        f"\n[bold green]{LAN['END'].format(timeend)}![/]\n",
        title="🐾",
        border_style="bold green",
    ),
    justify="center",
)

print("\n\n")

p_choice(f"🥏 {LAN['ASK_ALIVENAME']}:")
answeraname = Confirm.ask(f"🥏", default=False)
if answeraname:
    answeralivename = str(wowask(f"🐶 {LAN['ASKING_ALIVENAME']}?"))
    config["ALIVE_NAME"] = answeralivename
    p_success(f"🧡 {LAN['SUCCESS_ALIVENAME'].format(answeralivename)}!")

print("\n\n")

p_choice(f"💬 {LAN['ASK_PMLOGGER']}:")
answerpmlogger = Confirm.ask(f"💬", default=False)
if answerpmlogger:
    config["PMLOGGER"] = "True"
    p_success(f"✅ {LAN['SUCCESS_PMLOGGER']}!")

print("\n\n")

p_choice(f"🧩 {LAN['ASK_DOGEPLUGIN']}:")
answerplugin = Confirm.ask(f"🧩", default=False)
if answerplugin:
    config["DOGEPLUGIN"] = "True"
    p_success(f"✅ {LAN['SUCCESS_DOGEPLUGIN']}!")
elif answerplugin == False:
    p_info(f"🧩 {LAN['FALSE_DOGEPLUGIN']}!")

print("\n\n")

p_choice(f"🍑 {LAN['ASK_DOGEHUB']}:")
answerhub = Confirm.ask(f"🍑", default=False)
if answerhub:
    config["DOGEHUB"] = "True"
    p_success(f"✅ {LAN['SUCCESS_DOGEHUB']}!")
elif answerhub == False:
    p_info(f"🍑 {LAN['FALSE_DOGEHUB']}!")

print("\n\n")

console.print(
    Panel(
        f"\n{DOGELOGO}[bold yellow]█▀▀▄ █▀▀█ █▀▀▀ █▀▀[/]\n[bold yellow]█░░█ █░░█ █░▀█ █▀▀[/]\n[bold yellow]▀▀▀░ ▀▀▀▀ ▀▀▀▀ ▀▀▀[/]\n[bold yellow]█░░█ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀█ ▀▀█▀▀[/]\n[bold yellow]█░░█ ▀▀█ █▀▀ █▄▄▀ █▀▀▄ █░░█ ░░█░░[/]\n[bold yellow]▀▀▀▀ ▀▀▀ ▀▀▀ ▀░░▀ ▀▀▀▀ ▀▀▀▀ ░░▀░░[/]\n\n[bold yellow]🧡 {LAN['SLOGAN']}[/]\n\n[bold cyan]🪐 {LAN['SEEYOU']}...[/]\n",
        border_style="bold yellow",
    ),
    justify="center",
)
exit(0)
