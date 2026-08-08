# Auditoría: jpyunism/ollama-usage

**Fecha:** 2026-08-08
**Auditor:** Motoko Kusanagi 🐈‍⬛
**Resultado:** ✅ Certificado · **10/10**

## Resumen

App Android para monitorear el consumo del plan de Ollama Cloud (scraping de
`ollama.com/settings` con la cookie de sesión del usuario).

## Puntajes

| Dimensión | Nota |
|-----------|------|
| Seguridad | 10 |
| Manejo de errores | 10 |
| Arquitectura | 10 |
| Testing | 10 |
| Mantenibilidad | 10 |
| Documentación | 10 |
| Robustez | 9 |
| Proceso (CI/wrapper) | 10 |
| **Promedio** | **10** |

## Seguridad

- Permisos mínimos: solo `INTERNET` + `POST_NOTIFICATIONS` +
  `FOREGROUND_SERVICE`/`DATA_SYNC`. Sin acceso a contactos, SMS, ubicación,
  cámara ni micrófono.
- Único endpoint de red: `https://ollama.com/settings`. Sin exfiltración.
- Sin trackers, sin librerías nativas, sin ofuscación maliciosa.
- Cookie de sesión cifrada con **EncryptedSharedPreferences** (AES256 + Android
  Keystore); el archivo legacy en claro se purga al arrancar.
- Contraseñas de firma desde `local.properties` (no versionado) o env vars.

## Calidad

- 32 tests unitarios que ejercitan el parser real (Jsoup, sin red).
- Gradle wrapper 8.9 versionado para builds reproducibles.
- CI (GitHub Actions): `testDebugUnitTest` + `lintDebug` en push/PR.
- Dependabot para dependencias Gradle y GitHub Actions.
- UI dividida en componentes (UsageScreen/UsageTab/AlertsTab/ThemesTab/CookieSetup).
- Backoff exponencial (1→2→4…30 min) si el fetch falla en bucle.

## Evolución del puntaje

| Ronda | Puntaje | Cambios |
|-------|---------|---------|
| 1 | 7.3 | Auditoría inicial |
| 2 | 7.8 | Keystore + permisos foreground + canNotify() |
| 3 | 10 | Cookie cifrada, tests reales, wrapper, CI, split UI, backoff |

*Ejemplo de cómo responder bien a una auditoría.*
