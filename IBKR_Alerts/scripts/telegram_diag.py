#!/usr/bin/env python3
"""Diagnóstico de Telegram: valida token, webhook, chat_id y envío de mensajes.
Uso:
  export TELEGRAM_BOT_TOKEN=xxxx   # o usa .env con python-dotenv
  export DEFAULT_CHAT_ID=-100123... # opcional
  python scripts/telegram_diag.py "Mensaje de prueba"

Salida: imprime resultados de getMe, getWebhookInfo, chats vistos en getUpdates y
el resultado de sendMessage con códigos de error claros.
"""
from __future__ import annotations
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # why: si no está instalado, igual seguimos con variables del entorno
    pass

API = "https://api.telegram.org"
TIMEOUT = 15


def env(name: str) -> Optional[str]:
    v = os.getenv(name)
    return v.strip() if v else None


def mask_token(tok: str) -> str:
    if len(tok) <= 10:
        return "***"
    head, tail = tok[:7], tok[-4:]
    return f"{head}...{tail}"


def tg_call(token: str, method: str, **params: Any) -> Tuple[int, Dict[str, Any]]:
    url = f"{API}/bot{token}/{method}"
    try:
        r = requests.post(url, json=params, timeout=TIMEOUT)
        status = r.status_code
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"ok": False, "description": r.text}
        return status, data
    except requests.RequestException as e:
        return 0, {"ok": False, "description": str(e)}


def main() -> int:
    token = env("TELEGRAM_BOT_TOKEN") or ""
    chat_id_env = env("DEFAULT_CHAT_ID")
    test_text = " ".join(sys.argv[1:]) or "IBKR_Alerts: prueba de envío"

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN no definido en entorno ni .env")
        return 2

    print(f"🔐 Token: {mask_token(token)}")

    # 1) getMe
    s, data = tg_call(token, "getMe")
    print("\n▶ getMe:", s, json.dumps(data, ensure_ascii=False))
    if s == 401 or data.get("error_code") == 401:
        print("❌ 401 Unauthorized: token inválido/antiguo. Reinicia el proceso con el token nuevo.")
        return 3
    if not data.get("ok"):
        print("❌ getMe falló →", data.get("description"))
        return 3

    # 2) getWebhookInfo
    s, w = tg_call(token, "getWebhookInfo")
    print("\n▶ getWebhookInfo:", s, json.dumps(w, ensure_ascii=False))
    if w.get("ok") and w.get("result", {}).get("url"):
        print("ℹ️ Tienes webhook configurado. Si usas polling, primero borra webhook: setWebhook url='' (vacío)")

    # 3) getUpdates (por si usas polling o para recolectar chat_ids recientes)
    s, upd = tg_call(token, "getUpdates", limit=10)
    print("\n▶ getUpdates (10):", s, json.dumps(upd, ensure_ascii=False))
    chat_ids: List[int] = []
    if upd.get("ok"):
        for u in upd.get("result", []):
            msg = u.get("message") or u.get("edited_message") or {}
            chat = msg.get("chat") or {}
            cid = chat.get("id")
            if isinstance(cid, int) and cid not in chat_ids:
                chat_ids.append(cid)
    if chat_id_env:
        try:
            cid = int(chat_id_env)
            if cid not in chat_ids:
                chat_ids.insert(0, cid)
        except ValueError:
            print(f"⚠️ DEFAULT_CHAT_ID inválido: {chat_id_env}")

    # 4) Intento de envío
    if not chat_ids:
        print("⚠️ No se detectaron chats. Escribe /start al bot desde un chat o agrega el bot a tu grupo/canal (admin para canales).")
        return 4

    last_error: Optional[str] = None
    for cid in chat_ids[:3]:
        print(f"\n▶ sendMessage → chat_id={cid}")
        s, res = tg_call(token, "sendMessage", chat_id=cid, text=test_text, disable_web_page_preview=True)
        print("status:", s, "resp:", json.dumps(res, ensure_ascii=False))
        if res.get("ok"):
            print("✅ Envío correcto a", cid)
            return 0
        desc = res.get("description", "")
        last_error = desc or str(res)
        if s == 403 or res.get("error_code") == 403:
            print("❌ 403 Forbidden: el bot no tiene permiso/bloqueado/no es admin en canal.")
        elif s == 400 or res.get("error_code") == 400:
            print("❌ 400 Bad Request: probablemente chat_id incorrecto (grupos migrados usan -100...) o formato inválido.")
        elif s == 429 or res.get("error_code") == 429:
            print("⏳ 429 Too Many Requests: throttling; espera y reintenta.")
        else:
            print("❌ Error al enviar:", last_error)
        time.sleep(1)

    print("\nResumen: no se pudo enviar. Último error:", last_error)
    return 5


if __name__ == "__main__":
    raise SystemExit(main())
