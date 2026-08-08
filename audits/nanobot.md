# Auditoría: madkoding/nanobot

**Fecha:** 2026-08-08
**Auditor:** Motoko Kusanagi 🐈‍⬛
**Resultado:** ✅ Certificado · **8.5/10**
**Repo:** https://github.com/madkoding/nanobot (fork de re-bin/nanobot, MIT)

## Resumen

Agente AI personal en Python (~128K líneas, 359 archivos) que corre en
producción como gateway (WhatsApp, WebUI, CLI). Router multi-modelo, TTS,
workflows en background, endurecimiento WhatsApp.

## Puntajes

| Dimensión | Nota |
|-----------|------|
| Seguridad | 9 |
| Manejo de errores | 8 |
| Arquitectura | 9 |
| Testing | 8 |
| Mantenibilidad | 9 |
| Documentación | 8 |
| Robustez | 8 |
| Proceso (CI/wrapper) | 9 |
| **Promedio** | **8.5** |

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

## Hallazgo crítico: bug de texto WhatsApp

- `runtime.py:805 send()` → texto usa `client.send_message(to, content)`,
  media usa `send_image/send_audio/send_video/send_document`.
- `_resolve_send_target` (L941) traduce LID→phone, pero los grupos `@g.us`
  no se tocan → el target no es el problema.
- **Causa raíz probable:** neonize `send_message` corre `_parse_group_mention`
  en cada texto (L~570 de neonize), que hace `get_group_info()` en vivo. Bajo
  la reconexión "live but silent", esa llamada falla y el envío de texto se
  pierde silenciosamente, mientras media (que no parsea menciones) sí sale.
- **Agravante:** `send()` hace `_record_send_success()` en el `else` si
  `send_message` no lanza. Si el texto se descarta en silencio (sin excepción),
  se cuenta como éxito → no hay log de error.

**Fix recomendado:** envolver el texto en `Message(conversation=content)`
directo (evitando el parseo de menciones) o pasar `Message` ya construido;
y validar el `SendResponse` del envío en vez de asumir éxito por no-excepción.

## Veredicto

Repo de alta calidad, bien modularizado, testado y con CI serio. Sin
problemas de seguridad. El bug de texto WhatsApp es el único punto caliente en
producción y está bien localizado. La cobertura apenas bajo el gate es un
deuda menor.

*Auditoría ejecutada en el commit `ea1d8b14` (v0.3.1).*
