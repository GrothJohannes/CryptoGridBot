# BTC Grid Trading Bot

Ein regelbasierter, backtestbarer Grid-Trading-Bot für BTC/USDT — emotionslos, modular, vollständig in Python.

---

## Überblick

Dieser Bot kombiniert klassische Grid-Logik mit einem trendfolgenden SMA-Filter. Er kauft automatisch Dips und verkauft Rallyes innerhalb einer definierten Preisspanne — aber nur dann, wenn der übergeordnete Markttrend bullish ist. Bei bearishem Signal pausiert der Bot vollständig. Kein Short-Grid, kein unnötiges Risiko.

**Einsatzzweck:** Erst Spot ohne Hebel (Test), danach Futures mit maximal 3× Hebel.

---

## Strategie im Überblick

### 1. Richtungsfilter (120-Tage SMA)

Der Bot handelt ausschließlich Long. Die Entscheidung basiert auf dem 120-Tage Simple Moving Average (SMA) auf Tagesbasis (UTC-Schluss).

| Signal | Bedingung |
|--------|-----------|
| **Long-Grid starten** | ≥ 2 Tageskerzen in Folge schließen > SMA120, UND Schlusskurs > SMA120 + 1% |
| **Long-Grid beenden** | ≥ 2 Tageskerzen in Folge schließen < SMA120, UND Schlusskurs < SMA120 − 1% |

Die Anzahl der Bestätigungskerzen ist getrennt für Entry und Exit konfigurierbar (`CONFIRMATION_CANDLES_ENTRY` / `CONFIRMATION_CANDLES_EXIT`).

### 2. Dynamischer Stop-Loss

```
stop_loss_price = SMA_120_aktuell × 0.99
```

Der Stop-Loss ist kein fester Preis — er wird täglich neu berechnet. In einem Bullenmarkt zieht er automatisch nach oben mit und sichert Gewinne progressiv ab. Keine manuelle Anpassung notwendig.

### 3. Grid-Mechanik

- **Unter aktuellem Preis:** gestaffelte Buy-Orders (Dips kaufen)
- **Über aktuellem Preis:** gestaffelte Sell-Orders (Rallyes verkaufen)
- Nach jedem Fill: sofortige Gegenorder auf dem nächsten Grid-Level
- Gebühren werden pro Trade in der Profitberechnung berücksichtigt
- Bei Range-Exit: Bot stoppt, manuelle Review, Grid wird neu berechnet

---

## Projektstruktur

```
btc_grid_bot/
├── config.py        # Alle Parameter zentral — keine Hardcodes elsewhere
├── data.py          # OHLCV-Kursdaten holen (täglich, UTC-Schluss)
├── sma_filter.py    # SMA berechnen, Crossover-Erkennung, Stop-Loss
├── grid_logic.py    # Grid-Level, Orders aufbauen/canceln, Fill-Handling
├── risk.py          # Positionsgröße, Hebel-Check, Liquidationspreis
├── execution.py     # Exchange-Anbindung via ccxt (Paper → Live)
├── backtest.py      # Historische Simulation der Gesamtstrategie
├── monitor.py       # Tägliches SMA-Update, Stop-Loss, Fill-Überwachung
└── main.py          # Entry Point, orchestriert alle Module
```

---

## Konfiguration (config.py)

| Parameter | Wert | Beschreibung |
|-----------|------|--------------|
| `SMA_PERIOD` | 120 | Tage für den gleitenden Durchschnitt |
| `GRID_SPACING_PCT` | 0.003 | 0,3% Abstand zwischen Grid-Levels |
| `MAX_GRID_COUNT` | 200 | Hartes Limit für aktive Orders |
| `CONFIRMATION_CANDLES_ENTRY` | 2 | Mindest-Bestätigungskerzen für Entry |
| `CONFIRMATION_CANDLES_EXIT` | 2 | Mindest-Bestätigungskerzen für Exit |
| `CAPITAL_INVESTED` | 0.80 | 80% des allokierten Kapitals |
| `CAPITAL_RESERVE` | 0.20 | 20% als dynamischer Puffer |
| `LEVERAGE` | 3 | Harte Obergrenze, nie überschreiten |

---

## Entwicklungsreihenfolge

1. `config.py` — Parameter definieren
2. `data.py` — historische OHLCV-Daten laden
3. `sma_filter.py` — SMA + Confirmation-Logik isoliert testen
4. `backtest.py` — Gesamtstrategie historisch validieren
5. `grid_logic.py` — Grid-Mechanik testen
6. Spot-Grid ohne Hebel im Paper-Trading validieren
7. Futures + Hebel (max 3×)
8. `monitor.py` + `execution.py` — Live-Betrieb

> **Regel:** Niemals Live-API anbinden ohne vorherigen Backtest.

---

## Voraussetzungen

```bash
pip install pandas numpy ccxt python-dotenv
```

API-Keys werden sicher aus einer `.env`-Datei geladen — niemals im Code hardcoden.

---

## Code-Qualität

- Type Hints für alle Funktionen
- `logging` statt `print()`
- Fehlerbehandlung für alle API-Calls (try/except + Retry-Logik)
- Klarer Input/Output-Kontrakt pro Funktion
- Alle Parameter in `config.py` — keine Hardcodes in Logik-Dateien

---

## Risikohinweis

Dieser Bot ist ein persönliches Entwicklungsprojekt. Kryptowährungshandel birgt erhebliche Verlustrisiken. Der Einsatz von Hebelprodukten kann zu einem Totalverlust des eingesetzten Kapitals führen. Immer zuerst auf Testnet/Paper-Trading validieren.
