# ---------------------------------------------------------------------------------
#  /\_/\  馃寪 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  馃敁 Not licensed.
#  > ^ <   鈿狅笍 Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Iris
# Author: SkillsAngels
# Commands:
# .farmon | .farmoff | .farm | .bag | .irish
# .give
# ---------------------------------------------------------------------------------

version = (0, 0, 2)

# for more info: https://murix.ru/files/ftg
# by xadjilut, 2021

# 屑芯写褍谢褜 褔邪褋褌懈褔薪芯 薪械 屑芯泄 | This module is not half mine.

# _           _            _ _
# | |         | |          (_) |
# | |     _ | |_ _  _ _| |
# | |    / _ \| / _ \/ | | |/ /
# | |_| (_) | || (_) \ \ |   <
# \_/\_/ \\_/|_/_|_|\_\
#
#              漏 Copyright 2022
#
#         developed by @lotosiiik, @byateblan

# meta developer: @hikkaftgmods
# meta banner: https://te.legra.ph/file/a428776824470e0bdccb6.jpg
# meta pic: https://te.legra.ph/file/98192f1f7953275baead5.jpg

import random
from datetime import timedelta

from telethon import functions
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class IrisMod(loader.Module):
    """袛谢褟 邪胁褌芯屑邪褌懈褔械褋泻芯谐芯 褎邪褉屑懈薪谐邪 泻芯懈薪芯胁 胁 懈褉懈褋斜芯褌械"""

    strings = {
        "name": "Iris",
        "farmon": (
            "<i>鉁呅炑傂恍拘缎敌叫盒� 褋芯蟹写邪薪邪, 邪胁褌芯褎邪褉屑懈薪谐 蟹邪锌褍褖械薪, 胁褋褢 薪邪褔薪褢褌褋褟 褔械褉械蟹 20"
            " 褋械泻褍薪写...</i>"
        ),
        "farmon_already": "<i>校卸械 蟹邪锌褍褖械薪芯</i>",
        "farmoff": "<i>鉂屝愋惭傂狙勑把�屑懈薪谐 芯褋褌邪薪芯胁谢械薪.\n鈽笍袧邪写褞锌邪薪芯:</i> <b>%coins% i垄</b>",
        "farm": "<i>鈽笍袧邪写褞锌邪薪芯:</i> <b>%coins% i垄</b>",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.myid = (await client.get_me()).id
        self.iris = 5443619563

    async def farmoncmd(self, message):
        """袟邪锌褍褋褌懈褌褜 邪胁褌芯褎邪褉屑懈薪谐"""
        status = self.db.get(self.name, "status", False)
        if status:
            return await message.edit(self.strings["farmon_already"])
        self.db.set(self.name, "status", True)
        await self.client.send_message(
            self.iris, "肖邪褉屑邪", schedule=timedelta(seconds=20)
        )
        await message.edit(self.strings["farmon"])

    async def farmoffcmd(self, message):
        """袨褋褌邪薪芯胁懈褌褜 邪胁褌芯褎邪褉屑懈薪谐"""
        self.db.set(self.name, "status", False)
        coins = self.db.get(self.name, "coins", 0)
        if coins:
            self.db.set(self.name, "coins", 0)
        await message.edit(self.strings["farmoff"].replace("%coins%", str(coins)))

    async def farmcmd(self, message):
        """袙褘胁芯写 泻芯谢-胁邪 泻芯懈薪芯胁, 写芯斜褘褌褘褏 褝褌懈屑 屑芯写褍谢械屑"""
        coins = self.db.get(self.name, "coins", 0)
        await message.edit(self.strings["farm"].replace("%coins%", str(coins)))

    async def watcher(self, event):
        if not isinstance(event, Message):
            return
        chat = utils.get_chat_id(event)
        if chat != self.iris:
            return
        status = self.db.get(self.name, "status", False)
        if not status:
            return
        if event.raw_text == "肖邪褉屑邪":
            return await self.client.send_message(
                self.iris, "肖邪褉屑邪", schedule=timedelta(minutes=random.randint(1, 20))
            )
        if event.sender_id != self.iris:
            return
        if "袧袝袟袗效衼孝!" in event.raw_text:
            args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
            randelta = random.randint(20, 60)
            if len(args) == 4:
                delta = timedelta(
                    hours=args[1], minutes=args[2], seconds=args[3] + randelta
                )
            elif len(args) == 3:
                delta = timedelta(minutes=args[1], seconds=args[2] + randelta)
            elif len(args) == 2:
                delta = timedelta(seconds=args[1] + randelta)
            else:
                return
            sch = (
                await self.client(
                    functions.messages.GetScheduledHistoryRequest(self.iris, 1488)
                )
            ).messages
            await self.client(
                functions.messages.DeleteScheduledMessagesRequest(
                    self.iris, id=[x.id for x in sch]
                )
            )
            return await self.client.send_message(self.iris, "肖邪褉屑邪", schedule=delta)
        if "袟袗效衼孝" in event.raw_text or "校袛袗效袗" in event.raw_text:
            args = event.raw_text.split()
            for x in args:
                if x[0] == "+":
                    return self.db.set(
                        self.name,
                        "coins",
                        self.db.get(self.name, "coins", 0) + int(x[1:]),
                    )

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ):
        """袨褌锌褉邪胁谢褟械褌 褋芯芯斜褖械薪懈械 懈 胁芯蟹褉邪褖邪械褌 芯褌胁械褌"""
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if mark_read:
                await conv.mark_read()

            if delete:
                await msg.delete()
                await response.delete()

            return response

    @loader.command()
    async def give(self, message):
        """袩械褉械写邪械褌 懈褉懈褋泻懈/谐芯谢写 薪邪 写褉褍谐芯泄 邪泻泻"""
        bot = "@iris_black_bot"
        args = utils.get_args_raw(message)
        nmb = int(args.split(" ")[1])
        player = args.split(" ")[2]
        dada = ""
        if args.split(" ")[0] == "谐芯谢写":
            dada = " 谐芯谢写"
        elif args.split(" ")[0] == "懈褉懈褋泻懈" or args[0] == "懈褉懈褋":
            dada = ""
        else:
            return await utils.answer(
                message, "鉂寍 袨褕懈斜泻邪,褔褌芯-斜褘 锌械褉械写邪褌褜 褌褉械斜褍械褌褋褟 薪邪锌懈褋邪褌褜 懈褉懈褋泻懈 懈谢懈 谐芯谢写."
            )

        text = f"袩械褉械写邪褌褜{dada} {nmb} {player}"
        try:
            text += f'\n{args.split(" | ")[1]}'
        except IndexError:
            pass

        givs = await self.message_q(
            text,
            bot,
            mark_read=True,
            delete=True,
        )

        await utils.answer(message, givs.text)

    @loader.command()
    async def bagcmd(self, message):
        """袩芯泻邪蟹褘胁邪械褌 胁邪褕 屑械褕芯泻"""

        bot = "@iris_black_bot"
        bags = await self.message_q(
            "袦械褕芯泻",
            bot,
            delete=True,
        )

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, bags.text)

    async def irishcmd(self, message):
        """袩芯屑芯褖褜 锌芯 屑芯写褍谢褞 Iris"""
        ihelp = (
            "馃崁| <b>袩芯屑芯褖褜 锌芯 泻芯屑邪薪写邪屑:</b>\n\n .farmon - 袙泻谢褞褔邪械褌 邪胁褌芯 褎邪褉屑.\n .farmoff"
            " - 袙褘泻谢褞褔邪械褌 邪胁褌芯 褎邪褉屑.\n .farm - 袩芯泻邪蟹褘胁邪械褌 褋泻芯谢褜泻芯 胁褘 薪邪褎邪褉屑懈谢懈.\n .bag"
            " - 袩芯泻邪蟹褘胁邪械褌 胁邪褕 屑屑械褕芯泻\n .give - 锌械褉械写邪褢褌 懈褉懈褋泻懈/谐芯谢写\n\n"
            " <b>袩褉懈屑械褉:</b>\n .give {懈褉懈褋泻懈 懈谢懈 谐芯谢写} {褔懈褋谢芯} {褞蟹械褉}. - 斜械蟹 锌褉懈褔懈薪褘.\n"
            " .give {懈褉懈褋泻懈 懈谢懈 谐芯谢写} {褔懈褋谢芯} {褞蟹械褉} | {锌褉懈褔懈薪邪}"
        )
        await utils.answer(message, ihelp)