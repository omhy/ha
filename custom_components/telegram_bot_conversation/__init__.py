# Create as custom_components/telegram_bot_conversation/__init__.py
# Requires telegram_bot to be set up. 
from homeassistant import core
from homeassistant.components.telegram_bot import (
    EVENT_TELEGRAM_TEXT,
    ATTR_TEXT,
    SERVICE_SEND_MESSAGE,
    DOMAIN as TELEGRAM_DOMAIN,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_USER_ID,
    ATTR_CHAT_ID,
)
from homeassistant.components.conversation import process

DOMAIN = "telegram_bot_conversation"


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    async def text_events(event: core.Event):
        # Only deal with private chats.
        if event.data[ATTR_CHAT_ID] != event.data[ATTR_USER_ID]:
            return

        response = await process(hass, event.data[ATTR_TEXT], "telegram-bot")

        await hass.services.async_call(
            TELEGRAM_DOMAIN,
            SERVICE_SEND_MESSAGE,
            {
                ATTR_MESSAGE: response.speech["plain"]["speech"],
                ATTR_TARGET: event.data[ATTR_USER_ID],
            },
        )

    hass.bus.async_listen(EVENT_TELEGRAM_TEXT, text_events)
    return True
