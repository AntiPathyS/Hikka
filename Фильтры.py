from .. import loader, utils


@loader.tds
class Rayfilter(loader.Module):
    """Фильтры"""
    strings = {"name": "Фильтры"}

    async def client_ready(self, client, db):
        self.db = db

    async def фильтрcmd(self, message):
        """Добавить фильтр в список."""
        filters = self.db.get("Фильтры", "фильтры", {})
        key = utils.get_args_raw(message) # .lower()
        reply = await message.get_reply_message() 
        chatid = str(message.chat_id)

        if not key and not reply:
            return await message.edit("<b>Нет аргументов и реплая.(1)</b>")

        if chatid not in filters:
            filters.setdefault(chatid, {})

        if key in filters[chatid]:
            return await message.edit("<b>Такой фильтр уже есть.(1)</b>")

        if reply:
            if key:
                msgid = await self.db.store_asset(reply)
            else:
                return await message.edit("<b>Нужны аргументы, чтобы сохранить фильтр!(1)</b>")
        else:
            try:
                msgid = (await message.client.send_message(f'friendly-{(await message.client.get_me()).id}-assets', key.split(' / ')[1])).id
                key = key.split(' / ')[0]
            except IndexError:
                return await message.edit("<b>Нужен второй аргумент (через / )или реплай.(1)</b>")

        filters[chatid].setdefault(key, msgid)
        self.db.set("Фильтры", "фильтры", filters)
        await message.edit(f"<b>Фильтр \"{key}\" сохранён!(1)</b>") 


    async def стопcmd(self, message):
        """Удаляет фильтр из списка."""
        filters = self.db.get("Фильтры", "фильтры", {})
        args = utils.get_args_raw(message)
        chatid = str(message.chat_id)

        if chatid not in filters:
            return await message.edit("<b>В этом чате нет фильтров.</b>")

        if not args:
            return await message.edit("<b>Нет аргументов.</b>")

        if args:
            try:
                filters[chatid].pop(args)
                self.db.set("Фильтры", "фильтры", filters)
                await message.edit(f"<b>Фильтр \"{args}\" удалён из чата!(1)</b>")
            except KeyError:
                return await message.edit(f"<b>Фильтра \"{args}\" нет.(1)</b>")
        else:
            return await message.edit("<b>Нет аргументов.(1)</b>")


    async def стополcmd(self, message):
        """Удаляет все фильтры из списка чата."""
        filters = self.db.get("Фильтры", "фильтры", {})
        chatid = str(message.chat_id)
 
        if chatid not in filters:
            return await message.edit("<b>В этом чате нет фильтров(1).</b>")

        filters.pop(chatid)
        self.db.set("Фильтры", "фильтры", filters)
        await message.edit("<b>Всё фильтры были удалены из списка чата!(1)</b>")


    async def фильтрыcmd(self, message):
        """Показывает список фильтров чата."""
        filters = self.db.get("Фильтры", "фильтры", {})
        chatid = str(message.chat_id)

        if chatid not in filters:
            return await message.edit("<b>В этом чате нет фильтров(1).</b>")

        msg = ""
        for _ in filters[chatid]:
            msg += f"<b>• {_}</b>\n"
        await message.edit(f"<b>Список фильтров в этом чате(1): {len(filters[chatid])}\n\n{msg}</b>") 


    async def watcher(self, message):
        try:
            filters = self.db.get("Фильтры", "фильтры", {})
            chatid = str(message.chat_id)
            m = message.text.lower()
            if chatid not in filters: return

            for _ in filters[chatid]:
                msg = await self.db.fetch_asset(filters[chatid][_])
                def_pref = self.db.get("friendly-telegram.main", "command_prefix")
                pref = '.' if not def_pref else def_pref[0]

                if len(_.split()) == 1:
                    if _.lower() in m.split():
                        await self.exec_comm(msg, message, pref)
                else:
                    if _.lower() in m:
                        await self.exec_comm(msg, message, pref)
        except: pass

    async def exec_comm(self, msg, message, pref):
        try:
            if msg.text[0] == pref:
                smsg = msg.text.split()
                return await self.allmodules.commands[smsg[0][1:]](await message.reply(smsg[0] +  ' '.join(_ for _ in smsg if len(smsg) > 1)))
            else: pass
        except: pass
        await message.reply(msg)

