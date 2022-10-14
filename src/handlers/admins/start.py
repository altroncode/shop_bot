import aiogram.types
from aiogram import types
from aiogram.dispatcher import filters

import responses.main_menu
import responses.start
from filters import is_user_in_db, is_admin
from loader import dp
from services import db_api, notifications
from services.db_api import queries


@dp.message_handler(filters.Text('✅ Accept'), is_admin.IsUserAdmin())
async def accept_rules(message: aiogram.types.Message):
    with db_api.create_session() as session:
        queries.add_user(
            session, message.from_user.id, message.from_user.username.lower()
        )
        await responses.start.NewUserResponse(message)
        await responses.main_menu.AdminMainMenuResponse(message)
        await notifications.NewUserNotification(message.from_user.id, message.from_user.username).send()


@dp.message_handler(filters.CommandStart(), is_admin.IsUserAdmin(), is_user_in_db.IsUserInDB(show_alert=False))
async def start(message: types.Message):
    await responses.start.UserExistsResponse(message)
    await responses.main_menu.AdminMainMenuResponse(message)


@dp.message_handler(filters.CommandStart(), is_admin.IsUserAdmin())
async def start(message: types.Message):
    await responses.start.RulesResponse(message)
