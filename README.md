# 🐈‍⬛ Powned by Motoko

Repositorio dedicado a **certificar y validar repos** que nos pasen.

Cuando un repo pasa la auditoría de seguridad y calidad, recibe su badge
**"Powned by Motoko"** con el puntaje promedio de 1 a 10. Este repo centraliza
todos los badges emitidos, junto con el resumen de cada auditoría.

> Este repo NO contiene código de los proyectos auditados. Solo badges,
> scripts de generación y resúmenes de auditoría.

---

## ¿Cómo funciona?

1. Alguien nos pasa un repo para revisar.
2. Se audita en dos ejes:
   - **Seguridad**: malware, exploits, permisos excesivos, endpoints de red,
     trackers, código nativo, secretos hardcodeados, ofuscación.
   - **Calidad**: manejo de errores, arquitectura, testing, mantenibilidad,
     documentación, robustez, proceso (CI/wrapper/dependencias).
3. Se asigna un puntaje de **1 a 10** por dimensión y se calcula el promedio.
4. Si el repo está limpio (sin malware ni exploits), se emite el badge
   **"Powned by Motoko"** con el puntaje promedio.

## Estructura

```
powned-by-motoko/
├── badges/      # Badges emitidos (WebP, estilo shields.io)
├── audits/      # Resúmenes de auditoría por repo
├── scripts/     # Generador de badges
└── README.md
```

## Badges emitidos

| Repo | Puntaje | Badge |
|------|---------|-------|
| [jpyunism/ollama-usage](https://github.com/jpyunism/ollama-usage) | 10/10 | [ver](badges/ollama-usage-10.webp) |
| [madkoding/nanobot](https://github.com/madkoding/nanobot) | 8.5/10 | [ver](badges/nanobot-8.5.webp) |

## Formato del badge

- Segmento izquierdo: **"Powned by Motoko"** (fondo blanco, letra negra)
- Segmento derecho: **puntaje promedio** (fondo morado, letra blanca)
- Formato WebP pequeño, estilo shields.io (WhatsApp no muestra SVG).

## Regenerar un badge

```bash
python3 scripts/make_badge_github.py <repo> <puntaje> <salida.webp>
```

---

*Badges emitidos por Motoko Kusanagi 🐈‍⬛ — calidad y seguridad aseguradas.*
