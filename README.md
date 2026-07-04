# AcademicInsight Bot

KI-gestütztes Tool zur automatisierten Analyse und Zusammenfassung wissenschaftlicher Paper. Entwickelt zur Unterstützung meiner Bachelorarbeit.

## Über das Projekt

Die Web-App (Streamlit) nimmt ein wissenschaftliches Paper entgegen – entweder als PDF/TXT-Upload oder als eingefügten Text – und lässt es über ein LLM (Llama 3.3 70B via Groq API) in drei wählbaren Modi aufbereiten:

- **Kompakte Zusammenfassung** – strukturiert, mit Kernpunkten
- **Fachbegriffe & Definitionen** – extrahiert und kurz erklärt
- **Kernfragen** – zentrale Forschungsfragen bzw. mögliche Schwachstellen des Papers

Das Ergebnis lässt sich direkt als `.txt`-Datei herunterladen.

## Setup

**Voraussetzungen:** Python 3.10+

```bash
pip install -r requirements.txt
```

**API-Key konfigurieren:**

1. Einen kostenlosen API-Key auf [console.groq.com](https://console.groq.com) erstellen
2. Im Projektordner die Datei `secrets.toml.example` nach `.streamlit/secrets.toml` kopieren
3. Darin den Platzhalter durch den eigenen Key ersetzen:

```toml
GROQ_API_KEY = "dein-echter-key"
```

> `.streamlit/secrets.toml` ist in `.gitignore` eingetragen und wird nicht mit hochgeladen – jeder Nutzer trägt dort seinen eigenen Key ein.

## Starten

```bash
streamlit run app.py
```

Alternativ unter Windows: `start_bot.bat` doppelklicken (Pfad im Skript ggf. anpassen).

## Verwendete Technologien

- [Streamlit](https://streamlit.io/) – Web-UI
- [Groq API](https://groq.com/) – LLM-Inferenz (Llama 3.3 70B)
- [pypdf](https://pypdf.readthedocs.io/) – PDF-Textextraktion
