from argparse import Namespace
from .. import loader, utils
import asyncio, pytz, re, telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time
import telethon.events as events
import random
import string
import humanize
import math


client = 0;
class data:
 owner_id = 1221419333

class commands:

 async def calc(message, ability, fromlvl, tolvl):
  """Калькулятор"""
  if int(fromlvl) >= int(tolvl) or int(fromlvl) < 0 or int(tolvl) < 0: return;

  new_message, ability_string, price = "", "", 0;

  for i in range(int(fromlvl), int(tolvl)):
   match ability:
    case ("заразность"|"зараз"|"зз"):
     price += (i + 1)**2.5;
     ability_string = "✅ Усиление заразности патогена";
    case ("иммунитет"|"иммун"|"имун"):
     price += (i + 1)**2.45; 
     ability_string = "✅ Укрепление иммунитета";
    case ("летальность"|"летал"|"леталка"):
     price += (i + 1)**1.95;
     ability_string = "🗓 Усиление летальности патогена";
    case ("квалификация"|"квала"|"скорость"):
     price += (i + 1)**2.6;
     ability_string = "✅ Ускорение производства патогена";
    case ("патогены"|"паты"|"патоген"|"пат"):
     price += (i + 1)**2;
     ability_string = "🗓 Увеличение количества ячеек с патогеном";
    case ("безопасность"|"сб"|"служба"):
     price += (i + 1)**2.1;
     ability_string = "✅ Укрепление службы безопасности"; 
    case _:
     return;

  price = str(int(price));
  new_message = ability_string + " на " + str(int(tolvl) - int(fromlvl))+ " ур (до " + tolvl + ")\n";
  new_message += "🧬 Цена: " + str(humanize.intcomma(price)).replace(",", ".") + " био-ресурсов";
  await message.reply(new_message);


class CalcMod(loader.Module):
 'Показывает сколько нужно био-опыта для улучшения.\n Используй: Калькулятор (аргумент) (от) (до).\nАргументы:\nзаразность|зараз|зз\nиммунитет|иммун\nквалификация|квала|скорость\nпатогены|паты|патоген|пат\nбезопасность|сб|служба'
 strings = {"name": "Calculator"};

 async def watcher(self, message):
  if not isinstance(message, telethon.tl.types.Message): return;
  author, content = await message.get_sender(), message.message;

  if author.id != data.owner_id: return

  parts = content.split(" ");
  command = parts[0];
  match command:
   case "Калькулятор":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "калькулятор":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "калк":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "Калк":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "calc":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "Calc":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "кал":
    await commands.calc(message, parts[1], parts[2], parts[3]); 
   case "д":   
    await commands.calc(message, parts[1], parts[2], parts[3]);
