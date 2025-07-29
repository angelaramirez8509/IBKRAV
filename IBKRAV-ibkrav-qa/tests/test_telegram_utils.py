import os
import pytest
from ibkrav.view.telegram_utils import enviar_telegram

@pytest.mark.skipif(
    not os.getenv("BOT_TOKEN") or not os.getenv("CHAT_ID"),
    reason="Faltan variables BOT_TOKEN o CHAT_ID"
)
def test_enviar_telegram():
    try:
        enviar_telegram("✅ Prueba de mensaje desde pytest IBKRAV")
    except Exception as e:
        pytest.fail(f"Falló el envío a Telegram: {e}")
