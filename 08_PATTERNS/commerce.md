# Commerce

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation — pattern flows are ○ reconstructions built on observed behaviour.

```
Discover  →  Evaluate  →  Compare  →  Act
```

| | |
|---|---|
| **User goal** | Go from inspiration to purchase without doubt about price. |
| **Trigger** | A look, product card, or price alert. |
| **UI structure** | Look (starring you) with hotspots → product sheet / PDP → one 'Buy on store' action; price with freshness stamp. |
| **Interaction** | Tap hotspot → sheet; swipe gallery; select size; tap buy (external) — confirm only if price changed. |
| **Success condition** | Purchase started with the same price that was shown. |

## State transitions
1. Discover: look or card
2. Evaluate: PDP, fit confidence, price checked
3. Compare: similar items rail / compare icon
4. Act: buy; re-price check; dialog on change

## Price integrity (case extension ◇)
Prices on cards, buttons and alerts are rendered from the offer/catalogue response and bound to its ID. A re-price check runs when the
user taps the action; if the value moved, a dialog restates the new price. Supplier timeout → amber "Cached HH:MM" and "Check live price",
never a guessed number.
