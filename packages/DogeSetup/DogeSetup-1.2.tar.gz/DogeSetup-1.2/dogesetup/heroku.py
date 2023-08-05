# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from time import sleep

from heroku3 import from_key
from requests.exceptions import HTTPError

from . import *
from .language import DOGELANG, GMT, LAN

LAN = LAN["HEROKU"]


def connect():
    while True:
        api = wowask(f"🔐 {LAN['KEY']}:")
        heroku_conn = from_key(api)
        try:
            p_info(f"⏳ %3 ~ {LAN['LOGINING']}...")
            heroku_conn.apps()
            break
        except Exception:
            p_error(f"🔸 {LAN['INVALID_KEY']}!\n🔄 {LAN['RETRYING_KEY']}...")
            sleep(3)
            if name == "nt":
                system("cls")
            else:
                system("clear")
            logo(DOGELANG)

    p_success(f"✅ %7 ~ {LAN['HEROKU_LOGGED']}!")
    return heroku_conn, api


def createApp(connect):
    p_info(f"⏳ %35 ~ {LAN['CREATING_APP']}...")
    appname = datetime.now(GMT).strftime("dogeuserbot-%d-%m-%y--%H-%M-%S")
    try:
        connect.create_app(
            name=appname, stack_id_or_name="container", region_id_or_name="eu"
        )
    except HTTPError:
        p_error(
            f"💔 {LAN['MOSTAPP']}.\n\n[bold white]🔅 {LAN['FOR_MOSTAPP_SOLVE']}!\n\n🔁 {LAN['IF_SOLVE_TRY_AGAIN']}.[/]"
        )
        exit(1)

    p_success(f"✅ %54 ~ {LAN['SUCCESS_APP']}!")
    return appname


def hgit(connect, repo, appname, api):
    app = connect.apps()[appname]
    giturl = app.git_url.replace("https://", "https://api:" + api + "@")
    if "temponame" in repo.remotes:
        remote = repo.remote("temponame")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("temponame", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        p_error(
            f"🔸 {LAN['ERROR']}: {str(e)}\n\n🔁 {LAN['TRY_AGAIN_SETUP']}.\n📍 {LAN['IF_SEE_ERROR']}."
        )
        try:
            p_info(f"🔄 {LAN['DELETING_APP']}...")
            sleep(2)
            app.delete()
            p_info(f"🚧 {LAN['DELETED_APP']}!")
        except Exception:
            p_error(f"🔸 {LAN['ERROR_DELETED_APP']}!")
            pass  # noqa
        exit(1)

    p_info(f"⏳ %81 ~ {LAN['POSTGRE']}...")
    app.install_addon(plan_id_or_name="062a1cc7-f79f-404c-9f91-135f70175577", config={})
    p_success(f"✅ %84 ~ {LAN['SUCCESS_POSTGRE']}!")
    return app


def opendyno(app):
    p_info(f"⏳ %97 ~ {LAN['OPENING_DYNO']}...")
    try:
        app.process_formation()["doger"].scale(1)
    except Exception:
        p_error(f"🔸 {LAN['ERROR_DYNO']}!\n🔹 {LAN['OPENSELF_DYNO']}.")
        pass  # noqa
