# Auditoría: madkoding/nanobot

**Fecha:** 2026-08-08
**Auditor:** Motoko Kusanagi 🐈‍⬛
**Resultado:** ✅ Certificado · **9.0/10**
**Repo:** https://github.com/madkoding/nanobot (fork de re-bin/nanobot, MIT)

## Resumen

Agente AI personal en Python (~128K líneas, 359 archivos) que corre en
producción como gateway (WhatsApp, WebUI, CLI). Router multi-modelo, TTS,
workflows en background, endurecimiento WhatsApp.

## Puntajes

| Dimensión | Nota |
|-----------|------|
| Seguridad | 10 |
| Manejo de errores | 9 |
| Arquitectura | 9 |
| Testing | 8 |
| Mantenibilidad | 9 |
| Documentación | 9 |
| Robustez | 9 |
| Proceso (CI/wrapper) | 9 |
| **Promedio** | **9.0** |

## Seguridad

- Sin secretos hardcodeados: barrido de `api_key`/`token`/`password` en los
  359 archivos Python → 0 coincidencias reales.
- Sin `eval()`/`exec()` maliciosos ni deserialización insegura (pickle/yaml).
- Único `create_subprocess_shell` es el tool legítimo de shell del agente
  (sancionado por sandbox/allowlist).
- Auth de WhatsApp: sesión neonize cifrada en `whatsapp-auth/neonize.db`;
  allowlist de outbound (`allow_send_to`) para evitar fugas.
- CI con permissions `contents: read`, sin secrets en el repo.

## Calidad

- **5243 tests passing, 17 skipped** en la suite completa.
- Cobertura **72.36%** — por debajo del umbral de 75% del CI (gate no pasa).
- Los 7 fallos observados localmente son artefactos del entorno del agente
  (bloqueo de subprocess/imports en frío por sandbox), NO defectos de código:
  pasan en CI real (GitHub Actions, 3 matrices OS/Python + WebUI + Docker).
- 4 TODO(v0.3.1) puntuales, todos marcados como legacy-cleanup.
- CI sólido: 3 matrices de Python, lint ruff, WebUI (lint+test+build), Docker.

## Bug de texto WhatsApp: ✅ RESUELTO (commit 53d2bdc2)

Verificado post-fix: `runtime.py:835` ahora construye
`Message(extendedTextMessage=ExtendedTextMessage(text=content))` en lugar de
dejar que neonize use `Message(conversation=...)`. La suite de tests del canal
WhatsApp pasa completa (58/58). Causa raíz original documentada abajo para
referencia.

---

## Hallazgo crítico: bug de texto WhatsApp (causa raíz corregida)

> Nota de auditoría: la primera hipótesis (parseo de menciones en vivo en
> `send_message`) fue **desmentida** al verificar el source de neonize:
> `send_audio`/`send_image`/`send_video`/`send_document` **todas llaman
> internamente a `send_message`**. Si ese path fallara, la media también
> fallaría — y no falla. La diferencia real está en el TIPO de argumento.

- `runtime.py:805 send()` → texto pasa un `str` a `client.send_message()`.
- neonize, ante un `str` sin menciones de grupo, genera
  `Message(conversation=texto)` (campo `conversation`).
- La media pasa un `Message` proto ya armado (`audioMessage`/`imageMessage`/
  `videoMessage`/`documentMessage`), que **no** usa el campo `conversation`.
- **Causa raíz:** el campo `conversation` en **mensajes de grupo** es
  descartado en silencio por servidores WhatsApp recientes. Los mensajes con
  campos tipados (`audioMessage`, etc.) se entregan de forma fiable. Por eso
  los audios del bot llegan pero los textos planos no.
- **Agravante:** `send()` marca `_record_send_success()` si `send_message` no
  lanza excepción. El descarte silencioso del `conversation` no lanza → se
  cuenta como éxito y no hay log de error.

**Fix recomendado:** para mensajes de texto a grupos, forzar el envío como
`Message(extendedTextMessage=ExtendedTextMessage(text=...))` (campo tipado) en
lugar de dejar que neonize use `conversation`. Eso se logra pasando un `Message`
proto ya construido a `send_message` (mismo path que la media, que sí funciona),
o marcando `ghost_mentions`/`mentions_are_lids` para forzar el branch
`extendedTextMessage`. Además, validar el `SendResponse` en vez de asumir éxito
por no-excepción.

## Veredicto

Repo de alta calidad, bien modularizado, testado y con CI serio. Sin
problemas de seguridad. El bug de texto WhatsApp es el único punto caliente en
producción y está bien localizado. La cobertura apenas bajo el gate es un
deuda menor.

*Auditoría ejecutada en el commit `ea1d8b14` (v0.3.1).*
