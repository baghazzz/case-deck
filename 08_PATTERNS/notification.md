# Notification

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation — pattern flows are ○ reconstructions built on observed behaviour.

```
Change  →  Alert  →  Open  →  Act
```

| | |
|---|---|
| **User goal** | Hear only about changes that matter to me. |
| **Trigger** | Data change on something the user saved or follows. |
| **UI structure** | Grouped list (Today / Earlier), icon circle coded by type, data line with source and time; lock-screen hook for high-value changes. |
| **Interaction** | Tap to open the changed thing; swipe to dismiss; settings per type. |
| **Success condition** | Opened alert led to an action; low mute rate. |

## State transitions
1. Detect a real change (price, rule, live)
2. Alert with the new value + freshness
3. Open the thing, not a generic page
4. Act or dismiss
