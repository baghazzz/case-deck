# Claude Code prompt · case deck (final) · Glance26 AI PM intern case

**How to use this.** Paste everything below the line into Claude Code. Put these in the working directory first:

- `kit/`: unzip `Glance-Inspired-Design-System.zip` and rename `glance-inspired-design-system/` to `kit/`
- `ref/Glance-Inspired-Design-System.pdf`: the visual reference
- `ref/Full plan.pdf`: the content source for facts, tables and numbers
- `ref/Travel_Assistant_Decision_Reasoning.md`: the content source for the argument, the decision log and the jury questions

Every number below comes from the Full plan or the Decision Reasoning. Claude Code must not change, round or add a number.

---

## 1 · Task

Build a seventeen-slide main deck plus a ten-slide appendix at 1920 × 1080. It is for a product manager intern (AI) case round at Glance.

- **Order and flow** follow the five steps in `ref/Travel_Assistant_Decision_Reasoning.md` ("How we got there"): reframe the problem, read the 50%, derive the principle, test the options, fit it to 20 engineer-days. The deck argues in that order, so the options are judged against causes, not against each other.
- **Facts and tables** come from `ref/Full plan.pdf`.
- **Look** follows the Wake design system in `kit/` and `ref/Glance-Inspired-Design-System.pdf`.
- **Density.** The main deck carries the argument. Anything a juror might ask about but does not need in order to follow the argument goes to the appendix or the speaker notes.

Read these before writing any code. They are authoritative.

- `kit/DESIGN_SYSTEM_SUMMARY.md`
- `kit/01_DESIGN_PRINCIPLES/visual-principles.md` and `content-principles.md`
- `kit/03_TYPOGRAPHY/typography-spec.md` and `kit/04_COLORS/color-system.md`
- `kit/07_COMPONENTS/cards/README.md` and `kit/07_COMPONENTS/assistant/README.md`
- `kit/14_IMPLEMENTATION/component-specifications.md`
- `ref/Full plan.pdf`, all 36 pages. Extract it with `pdftotext -layout` and keep the text beside you. Wherever this prompt says "copy from the plan", copy the table verbatim.
- `ref/Travel_Assistant_Decision_Reasoning.md`, in full. Wherever this prompt says "copy from the reasoning", copy verbatim, changing "we" to "I" only where the prompt says so.

Open `ref/Glance-Inspired-Design-System.pdf` at pages 1, 6, 8, 12, 41 and 42, and every PNG in `kit/13_DECK_ASSETS/png/`. The deck must look like it belongs to that system. Match that finish, not a generic dark template.

---

## 2 · Build method (follow exactly)

1. Write each slide as standalone HTML at exactly 1920 × 1080: `slides/01.html` to `slides/17.html` and `slides/A01.html` to `slides/A10.html`.
2. Each slide links `../kit/14_IMPLEMENTATION/tokens.css`, `../kit/14_IMPLEMENTATION/components.css` and a shared `slides/deck.css`.
   - `components.css` already loads Inter and Instrument Serif from `kit/fonts/`.
   - Do not add web fonts, CDNs or JavaScript libraries. The build must run offline.
3. Inline `kit/11_SVG_ASSETS/icons/sprite.svg` once per slide. Use icons as `<svg class="icon"><use href="#i-plane"/></svg>`.
4. Draw every chart and diagram as inline SVG or HTML, using token colours only. No chart libraries and no raster images of charts.
5. Show phone screens as `<img>` of the kit's SVGs, in `kit/12_UI_EXAMPLES/travel-assistant/`. Never redraw a screen in HTML.
6. Build the step tracker (section 3) once, as a partial in `slides/deck.css` plus a small HTML snippet each slide includes, so all slides match.
7. Render every slide to PNG at 2× (3840 × 2160) with Playwright.
   - Use a fixed 1920 × 1080 viewport and `deviceScaleFactor: 2`.
   - Wait for `document.fonts.ready` before capturing.
8. Assemble `deck.pptx` with python-pptx.
   - Slide size 16:9. Each PNG goes full-bleed at (0, 0), with no other shapes.
   - Put the speaker notes from this prompt into each slide's notes.
   - Insert a plain divider slide titled "Appendix" between slide 17 and A01, using the same ground as slide 17.
   - Do not lay slides out in python-pptx itself. It cannot reproduce scrims, glass controls, hairlines or these fonts.
9. Print the HTML to `deck.pdf` as a vector reading copy.
10. Add `build.sh`, which runs the whole chain.
11. Add `README.md` with:
    - how to edit one slide and rebuild;
    - a table listing the one red element on each slide;
    - the on-slide word count of each main slide (see the density rule).
12. Comment the HTML. This deck will be revised several times.

---

## 3 · Design rules

### Grounds (one per slide)

| Slide type | Ground | Text |
|---|---|---|
| Content | `--color-background` #0C0C10; cards on `--color-surface` #16161B | `--color-text-primary`, `--color-text-secondary` |
| Title (01) and closing (17) | `--color-stage` #000 with `kit/11_SVG_ASSETS/backgrounds/stage-signal.svg` full-bleed | White |
| Emphasis (05), the only light slide | `data-theme="light"` on `<body>`, ground #F6F5F8, white cards with `--shadow-1` | #0C0C10 |
| Pivot (10) | `--color-primary-subtle` #3A0716 | White title, 80% white body |
| Appendix (A01–A10) | Content ground, with the eyebrow prefixed `APPENDIX ·` | As content |

### Colour has a job

**Red means now.** `--color-primary` #FF0049 appears on exactly one element per slide:

- the single highlighted bar, line, dot or tile in that slide's infographic; or
- the primary button inside a mockup.

The eyebrow is **not** red (this differs from the kit's sample slides). Set eyebrows in `--color-text-tertiary`, so red stays free for the data. The step tracker is never red.

**The other colours:**

| Colour | Token | Use it for |
|---|---|---|
| Lavender | `--color-iris` #DDBEF0 | Only things the assistant says or personalises |
| Green | `--color-success` | Verified, live or V1-shipped |
| Amber | `--color-warning` | Cached, changed, at risk, or Tier 0 |
| Orange-red | `--color-error`, always with an icon | Errors. Never use the brand red for an error |
| Everything else | White, secondary, tertiary, `rgba(255,255,255,.24)` | All other marks |

### Type

| Element | Font and size | Colour and rules |
|---|---|---|
| Slide titles | Instrument Serif 72–96 / 1.02 | Sentence case, max two lines. The only serif on the slide |
| Eyebrow | Inter 600, 16, uppercase, +0.08em | Tertiary |
| Lede | Inter 28 / 40 | Secondary, max two lines |
| Body | Inter 22 / 34 | |
| Table text | Inter 18 / 26 | Header row 14, uppercase, tertiary |
| Metadata and captions | Inter 16 / 24 | Tertiary, middle dots between facts |
| Stat figures | Inter 700, tabular numerals, 64–120 | Never the serif |

Minimum text size anywhere is **16px**. If something will not fit, cut a row or move it to the appendix. Never shrink type below 16.

### Geometry

- Margins: 120px at the sides, 96px at the top.
- Content column starts under the title block, at about y = 300.
- Radii: cards 16, hero surfaces 24, pills 999.
- Hairlines: 1px `--color-divider`.
- No drop shadows on dark slides. Elevation is a step in surface tone.

### Flow devices

**The step tracker.** Slides 03–16 carry a five-segment tracker, top right, aligned with the eyebrow baseline, 520px wide:

`1 Reframe · 2 Read the 50% · 3 Principle · 4 Test the options · 5 Fit to 20 days`

- Each segment is a 3px bar with its label beneath in Inter 600 14 (the one place 14px is allowed, as with table headers).
- Current step: bar and label white. Completed steps: 48% white. Future steps: 24% white.
- Slide 02 shows the same five steps large, as the deck's agenda (see slide 02). Slides 01 and 17 and the appendix carry no tracker.

**Hand-offs.** The last sentence of each slide's speaker notes hands off to the next slide. Keep it plain ("So the next question is which of these the 50% actually measures."). Never put the hand-off on the slide.

### Density rule (main deck)

- One infographic per slide. It answers the title; everything else supports it.
- At most about 60 words of on-slide text outside the infographic's own labels and tables. Record the count in `README.md`.
- If a table has more than seven rows on a main slide, it belongs in the appendix, with a line on the main slide pointing to it ("Full table: A01").
- Leave space. At least 15% of each main slide is empty ground.

### Every content slide carries

- **Eyebrow** above the title, naming the plan section (for example `1.4 · WHY 50%`).
- **Step tracker**, slides 03–16.
- **Footer**: a hairline, then `Prithwish Chakraborty · Glance26 AI PM case · Travel assistant accuracy` on the left and the page number on the right. Both tertiary.
- **Evidence tag** on any assumed or illustrative number. Beside the figure, in 16px tertiary: *Assumption*, *Illustrative* or *Sizing, not forecast*.

### Infographic rules (every chart on every slide)

- **Direct labels, no legends.** Label every bar, line and node at its end. The only exception is the size key on slide 11.
- **One highlight.** That is the slide's red. Everything else is white at 72% or `rgba(255,255,255,.24)`.
- **No value ramps across categories.** No 3D, no pie or donut charts, no gradients inside data marks.
- **Honest axes.** Bars start at zero. If a range makes a small value invisible, say so in the caption rather than using a broken axis. A log scale is allowed when the caption says so.
- **Plain headings.** Each infographic answers the slide title. Its caption states the one thing to notice, as a sentence.
- **Arrows.** Flows and pipelines use 1.5px hairline arrows. Missing or failing steps use a dashed outline in `--color-error` with the `alert` icon.

### Don'ts (binding)

- No Glance logo and no Glance brand assets. Write "Glance" in plain text. The kit's "wake" wordmark appears only inside the phone mockups.
- No company logos on the precedent slide. Names in text only.
- No emoji, no uppercase buttons, no text on an image without a scrim, no drop shadows on dark slides.
- No second red element on a slide.
- Never present an illustrative or assumed figure as measured.

---

## 4 · Voice: write like a PM, not like a model

This deck is judged by people who read a lot of AI-generated work. It must read as one person's judgment.

**Titles are the argument.** Every title is a full sentence stating that slide's conclusion. Reading only the 17 titles must tell the whole story (the list is in section 5). Use the titles given here, word for word.

**Write it like this:**

- Short declarative sentences. Concrete nouns. Numbers instead of adjectives: "₹4,764 where the airline charged ₹299", not "significantly higher fees".
- First person for decisions and doubts: "I cut Option C because…", "I don't know yet whether…". The reasoning file says "we"; change it to "I" for decisions and judgments, and keep "we" only for work the team does in execution.
- Name the trade-off every time something is chosen: what it costs, what it risks, what would change the decision.
- Say plainly what is assumed and what is not known.

**Banned words:** leverage, seamless, robust, delve, unlock, empower, holistic, synergy, cutting-edge, game-changer, revolutionise, streamline, elevate, harness, navigate (figuratively), landscape, ecosystem, journey (except the user journey slide), "in today's fast-paced world", "it's worth noting", "at the end of the day", "moreover", "furthermore".

**Banned patterns:**

- **Em dashes.** Use a full stop, comma, colon or middle dot instead.
- **"Not X, but Y" reframes.** Allowed once in the whole deck, in slide 10's notes.
- **Rhetorical questions** in titles or body. Questions are allowed only as quoted jury questions in A08 and as the week-0 question on slide 17.
- **Groups of three added for rhythm.**
- **Exclamation marks.**
- **A bold lead-in on every bullet.**
- **Ending a slide on a slogan.** Only slides 10 and 17 carry a line meant to be quoted.

**Speaker notes** are spoken sentences, two to five per slide. Write them the way you would explain it to an engineer at the next desk. Where a slide carries a decision, the notes include what would change my mind, taken from the matching decision (D1–D12) in the reasoning file. End with the hand-off to the next slide.

---

## 5 · The storyline (titles in order)

The argument, in five sentences (copy from the reasoning, "The argument in five sentences", and keep it beside you while building):

1. The assistant's errors are three problems, not one: it states prices, policies and fare details it does not own, in one confident voice, with nothing checking a claim against its source.
2. The 50% is a trip-level rate, so the weakest component, flight price, dominates it, while the costliest errors surface too late to show up in it.
3. So A and B ship as one rule: prices fetched at the moment of decision and never written by the model, policy answered only from a cited source, with a person for stranding cases.
4. C is cut because it relocates staleness into model weights, where it cannot be seen, dated or cited.
5. V1 is measured against the price the user acted on, tuned by config in a sandbox, and its telemetry decides V2.

| # | Step | Source section | Title |
|---|---|---|---|
| 01 | Open | Cover | Make it check before it speaks |
| 02 | Open | Plan on one page · Decision | One rule, shipped in four engineer-weeks, halves the error rate |
| 03 | 1 Reframe | Plan 1.1–1.2 · D1 | Four complaints, three different failures |
| 04 | 1 Reframe | Plan 1.3 | Nothing checks a claim before the user sees it |
| 05 | 2 Read the 50% | Plan 1.4 | Errors multiply, so the weakest part sets the trip rate |
| 06 | 2 Read the 50% | Plan 2a | Most errors are made early and found late |
| 07 | 3 Principle | Plan 2b | Every public failure was a model stating a fact it didn't own |
| 08 | 3 Principle | Reasoning step 3 | Who owns a fact decides how the assistant may state it |
| 09 | 4 Test the options | Reasoning step 4 · D2–D6 | A fetches fast facts, B cites slow ones, C memorises them |
| 10 | 4 Test the options | Decision | One rule, two evidence providers |
| 11 | 5 Fit to 20 days | Plan 3 · D7 | Severity decides first, then RICE ranks |
| 12 | 5 Fit to 20 days | Plan 4 · D5 | Two independent nets check every claim |
| 13 | 5 Fit to 20 days | Experience | The assistant can't make up a fare |
| 14 | 5 Fit to 20 days | Plan 5.1–5.3 · D8 | Two engineers, ten days, and neither waits on the other |
| 15 | 5 Fit to 20 days | Plan 5.4 · D10–D11 | Tuning is config, not code |
| 16 | 5 Fit to 20 days | Plan 5.5–5.8 · D9, D12 | Each version has to earn the next one |
| 17 | Close | Reasoning: assumptions | What would change my mind |

Slide 02's "halves" refers to the sizing (about 50% to 25–32%). Its evidence tag *Sizing, not forecast* must sit next to that figure on the slide.

If an element on a slide does not serve this sequence, cut it or move it to the appendix.

---

## 6 · Slide-by-slide (main deck)

### 01 · Title

**Ground:** stage + `stage-signal.svg`.

**Right side:** `assistant-lockscreen.svg` about 620px tall, level, with a 1px divider hairline under it as a floor.

**Left side:**

- Eyebrow: `GLANCE26 · AI PRODUCT MANAGER INTERN · CASE STUDY`
- Title (Instrument Serif 104): **Make it check before it speaks**
- Lede (Inter 30 / 42, 72% white): A travel-booking assistant quotes wrong fares, sold-out hotels and wrong visa rules. This is how I'd fix it in four engineer-weeks.
- Name line (Inter 22, 64% white): Prithwish Chakraborty · f20240470@pilani.bits-pilani.ac.in · 30/09/2026

**Red:** the lock-screen mockup's "See fare" button.

> **Notes:** The fix isn't a smarter model. It's a rule about which facts the model is allowed to state, and a way to prove the rule is working. I'll give you the answer first, then the five steps that got me there.

### 02 · The answer on one page

**Content slide, no tracker.** Eyebrow `THE ANSWER FIRST`.

**Top: the rule**, Inter 600 36 / 48, white, full width, one block: No price, availability or policy claim reaches the user without evidence from the source that owns it. Option C is cut.

**Middle: four commitment tiles** in a row, `--color-surface`, radius 16. Label in Inter 600 18 secondary, figure in Inter 700 tabular 56, one line under it in 16px tertiary. Copy from the reasoning, "What we commit to":

| Tile | Figure | Line under it |
|---|---|---|
| Capacity | 20 engineer-days | 2 engineers × 2 weeks · 18.5 planned, 1.5 held as buffer |
| North star | ~50% → ≤ 30% | Trip booking error rate · V2 ≤ 15% · tag *Sizing, not forecast* |
| Evidence | ≥ 99% | of price, availability and policy claims carry their evidence |
| Guardrails | +1.5 s · −5% | Time to price p90 over baseline · booking conversion drop limit |

**Red:** the `≤ 30%` in the north-star tile.

**Bottom: "How I got here", the five steps as the deck's agenda.** Five numbered cells in a row joined by hairline arrows. Each cell: number in Inter 700 tabular 32, step name in Inter 600 20, one line in 16px secondary, and the slide numbers where it lives in tertiary.

| # | Step | One line | Slides |
|---|---|---|---|
| 1 | Reframe the problem | "Hallucination" is three failures in three layers | 03–04 |
| 2 | Read the 50% | Errors multiply; the costliest ones are counted late | 05–06 |
| 3 | Derive the principle | Who owns a fact decides how it may be stated | 07–08 |
| 4 | Test the options | A and B fit the principle; C breaks it | 09–10 |
| 5 | Fit it to 20 days | Gate by severity, rank by RICE, cut at capacity | 11–16 |

> **Notes:** I diagnosed before I compared options, so each option is judged against a cause, not against the other options. If you remember one slide, it's this one. Step one starts with what the problem statement actually says.

### 03 · Four complaints, three different failures

Tracker at step 1. Eyebrow `1.1–1.2 · WHAT THE PROBLEM STATEMENT ACTUALLY SAYS`. Lede: The assistant acts as the source of truth for facts it does not own, and sounds equally sure reading live data, a stale cache or its own memory.

**Infographic, full width: a claim-ownership grid.**

- Rows: Flight price, Hotel availability, Visa and entry rules, Refund terms, Baggage allowance, In-flight meal.
- Columns: Who owns the truth · How fast it changes · Cost if wrong. Copy the cells from plan 1.2.
- Add a "speed of change" bar in its own narrow column: filled at a width proportional to speed (minutes = full, per fare = half, weeks = a quarter), one neutral colour.
- Group rows under three margin labels, each with an icon in secondary, copied from reasoning step 1:
  - *Transactional* (flight price, hotel availability), icon `plane`: changes in minutes, owned by supplier inventory
  - *Regulatory* (visa, refund terms), icon `passport`: changes in days or weeks, owned by governments and airlines
  - *Fare attribute* (baggage, meal), icon `meal`: owned by the fare record of this exact ticket

**Red:** the "Cost if wrong" cell for Visa and entry rules (text in `--color-primary`: "Denied boarding, stranding, liability").

Under the grid, one line in secondary: Three owners, three speeds, three costs. One fix cannot cover all three.

> **Notes:** "Hallucination" is one word for three failures in three layers. A bigger model or a better prompt still has no live price and still has a training date. What would change my mind: week-0 logs showing most errors come from one layer, say the model misreading a correct supplier response. So where in the pipeline does each one break?

### 04 · Nothing checks a claim before the user sees it

Tracker at step 1. Eyebrow `1.3 · HOW THE ASSISTANT WORKS TODAY`.

**Infographic: the request pipeline** as a horizontal flow of 7 hairline boxes, 1.5px arrows between them:

User request → Intent parsing → Router → Data path (three stacked sub-boxes: Cache · Live supplier call · Document store) → Prompt assembly → Model → Checkout

- Between Model and Checkout, draw a dashed box with the `alert` icon, labelled **"Missing: check the reply against its source"**.
- Under each real box, a small tertiary label with the layer name. Add failure-map IDs only where the plan gives them.

**Below the flow, three cards in a row**, one per failure from slide 03, each saying where it breaks:

- **Stale or wrongly keyed prices** · Data path and cache key · F-12, F-15, F-31
- **Policy answered from memory** · Router never fires retrieval · F-04
- **Attributes from the wrong source** · Router sends meal and bag questions to policy docs · F-05, F-25

**Red:** the dashed "missing check" box outline, in `--color-primary` (it is the point of the slide). The icon inside it is amber.

Caption: *F-numbers refer to the 40 failure modes in the Travel Assistant Failure Map.*

> **Notes:** The model sounds the same whether it read a live fare, a forty-minute-old cache or nothing at all. Nothing downstream notices. Before choosing a fix, I needed to read the 50% properly.

### 05 · Errors multiply, so the weakest part sets the trip rate

**The emphasis slide, light theme.** Tracker at step 2 (tracker colours inverted for light: #0C0C10 current, 48% and 24% of #0C0C10). Eyebrow `1.4 · WHY 50%`. Lede: A trip succeeds only if every component is right.

**Infographic: two multiplication chains**, each four white tiles joined by `×` and `=`. Figures in Inter 700 tabular 96.

| Row | Flight price | | Hotel availability | | Fees and ancillaries | | Whole trip |
|---|---|---|---|---|---|---|---|
| Today | `60%` | × | `92%` | × | `92%` | = | `50.8%` |
| If flight price is fixed | `98%` | × | `92%` | × | `92%` | = | `82.9%` |

- The `98%` tile is the only red, figure in `--color-primary-dark` #B80036 (AA on light).
- Put a thin bar under each "Whole trip" tile, at 50.8% and 82.9% of the tile width, so the jump is visible without reading.

Caption, tertiary: *Illustrative inputs, chosen to reproduce the brief's 50%. What holds for any plausible inputs: the weakest component dominates.*

> **Notes:** Fixing the weakest component lifts the trip rate far more than its own share suggests. That's why flight price gets most of the budget. But the 50% has a blind spot, and that's the next slide.

### 06 · Most errors are made early and found late

Tracker at step 2. Eyebrow `2A · THE USER JOURNEY`. Lede: The 50% is counted at checkout. Four of the six claim types go wrong after it.

**Infographic: a "made → found" journey chart.**

- **Columns:** the eight stages across the top (1 Ask · 2 Quote · 3 Compare · 4 Pre-trip questions · 5 Checkout · 6 Prepare · 7 Travel · 8 After the trip).
- **Rows:** six claims (Flight price, Hotel availability, Entry rules, Baggage, Meal, Refund terms).
- **Per row:** a hollow dot where the error is made, a filled dot where it is found, joined by a hairline arrow. Stages come from plan 2a:

| Claim | Made at | Found at |
|---|---|---|
| Flight price | 2–3 | 5 |
| Hotel | 2 | 5 |
| Entry rules | 4 | 7 |
| Baggage | 4 | 7 |
| Meal | 1 and 4 | 7 |
| Refund | 4 | 8 |

- **Red:** a vertical line at stage 5, labelled "The 50% is counted here".
- Arrows that cross the red line (the four late-surfacing claims) are white. The two that end at 5 are 24% white.

Caption, one line: Example request: Delhi to Bangkok, 2 adults, 24–28 October, under ₹60,000, and a Jain meal for my mother. Full happy and unhappy paths: plan 2a.

> **Notes:** The metric over-counts price and under-counts the errors that strand people. So I steer the policy work with leading indicators, grounded claim rate and deflection, instead of waiting for outcome data that arrives weeks late. Next: has anyone else hit this, and what fixed it?

### 07 · Every public failure was a model stating a fact it didn't own

Tracker at step 3. Eyebrow `2B · WHAT HAPPENED TO OTHERS`. Lede: And every fix that held moved the fact back to a source that could be checked.

**Infographic: a two-sided "failed → fixed" board.**

**Left, 1100px: six failure cards in a 3 × 2 grid** (the full list of ten is in the plan; keep the six that map to our complaints). Each has three parts: company and date (Inter 600 18), one line of what happened (16 / 24, secondary), and a chip with the feature it gives us.

| Case | What happened | Chip |
|---|---|---|
| Air Canada, Feb 2024 | Invented a bereavement-refund rule; tribunal held the airline liable, about C$650 | B2 |
| ChatGPT and Puerto Rico, Aug 2025 | "No visa needed"; the couple needed an ESTA and was denied boarding | B6 |
| Booking.com and Accor in ChatGPT, Feb 2026 | Stated rates didn't match the booking card; euros for a US user | A1, A8 |
| CCPA probe, May 2026 | Agoda showed ₹4,764 where Akasa Air charged ₹299 | A6 |
| Chevrolet dealer bot, Dec 2023 | Agreed to sell a Tahoe for $1, "a legally binding offer" | A1 |
| Klarna, May 2025 | AI push "had gone too far"; human agents brought back | B4 |

**Right, 480px: "What worked"** on `--color-surface`. Four rows, each with `check` in success and a chip:

- KAYAK.ai · real-time provider pricing in chat · A2
- Booking.com AI Trip Planner · prices as cards from inventory · A1
- Expedia Rapid Price Check · matched, changed or unavailable before booking · A3
- IATA Timatic · the database airlines check at boarding · B5

**Foot strip, full width:** one stat, `8%` of travellers comfortable booking through AI (Expedia/YouGov, 2026), in Inter 700 tabular 56, with one line beside it: Trust is scarce, so each visible error costs more than one booking.

**Red:** the `8%` figure.

No logos.

> **Notes:** None of the deployments that worked used a fine-tuned model as the source of truth. Every fix that held did one thing: it moved the fact back to whoever owns it. That gives me the principle.

### 08 · Who owns a fact decides how the assistant may state it

Tracker at step 3. Eyebrow `THE PRINCIPLE`. Lede: For every claim, three questions: who owns the truth, how fast it changes, and what a wrong answer costs.

**Infographic: a claim map with three regions.** A 2D plot, 1200 × 560, on the left two thirds.

- **X axis: how fast the truth changes**, ordinal, left to right: Minutes · Per fare or flight · Days to weeks · Years.
- **Y axis: cost if wrong**, ordinal, bottom to top: Low · A fee or a failed booking · Stranding, fraud or liability.
- **Dots** (18px, white 72%), each labelled directly. Positions from plan 1.2 and plan 4's freshness budget:

| Claim | Speed | Cost |
|---|---|---|
| Flight price | Minutes | Fee or failed booking |
| Hotel availability | Minutes | Fee or failed booking |
| Contact numbers, opening hours | Minutes | Stranding, fraud or liability |
| Baggage allowance | Per fare | Fee or failed booking |
| In-flight meal | Per flight | Low to fee (place between) |
| Refund terms | Per fare | Stranding, fraud or liability (money disputes, regulatory exposure) |
| Visa and entry rules | Days to weeks | Stranding, fraud or liability |
| Travel concepts | Years | Low |

- **Three shaded regions** behind the dots, `--color-surface` and `--color-surface-muted`, each with a label in Inter 600 20 and one line in 16px secondary:
  - Left column: **Fetch it** · live evidence at the moment the user decides
  - Upper right: **Cite it** · a dated official source, or hand off
  - Lower right: **Say it** · general knowledge; the validator still scans for prices
- Put a dashed hairline across the top band labelled "Nothing above this line comes from model memory".
- **Red:** the Visa and entry rules dot.

**Right third: the rule, derived.** Three short lines, Inter 24 / 36, stacked with hairlines:

- Fast facts are fetched.
- Slow, high-stakes facts are cited.
- Nothing high-stakes comes from model memory.

Caption: *Fare attributes (baggage, meals) sit on the fetch side: they come from this ticket's fare record, not from policy documents.*

> **Notes:** This is the whole method on one slide. I didn't pick the principle to suit an option; the options come next, and I test each one against it.

### 09 · A fetches fast facts, B cites slow ones, C memorises them

Tracker at step 4. Eyebrow `THE THREE OPTIONS, AGAINST THE PRINCIPLE`. Lede: A and B each fit the principle for one kind of fact, and each needs a missing piece to work. C breaks it.

**Infographic: a three-column verdict board.** Columns A · B · C, each a `--color-surface` card, radius 16.

**Row 1, verdict chip** at the top of each card:

- A: "Fits · fetches fast facts" (success)
- B: "Fits · cites slow facts" (success)
- C: "Breaks it · memorises slow facts" (the slide's red, outlined `--color-primary`)

**Rows 2–5, a compact scorecard** with `check`, `close` and `alert` icons in success, tertiary and warning:

| | A · live price and inventory | B · cite-or-deflect for policy | C · fine-tuned policy model |
|---|---|---|---|
| Fixes the main driver (flight price) | ✓ | ✗ | ✗ |
| Fixes the stranding risk (visa) | ✗ | ✓ | ⚠ goes stale |
| Fits 20 engineer-days | ✓ | ✓ | ✗ uses all of it |
| RICE as written · confidence | 96,000 · 80% | 54,000 · 60% | 4,500 · 30% |

**Row 6, "What it needs to work"**, one short block per card, copied from the reasoning:

- **A, rebuilt around decisions, not mentions (D4).** A live call on every mention adds 1–2 s a turn. Re-price at the decision, bind prices to an offer ID, add the supplier fallback. The split package costs 1.7 engineer-weeks and covers more mechanisms.
- **B, plus a router rule (D6).** If a visa question is classed as chat, the gate never runs. B1 lifts B from 60% to 80% confidence for 0.3 engineer-weeks.
- **C, nothing fixes it (D3).** It moves staleness from a cache, where it has an age, into weights, where it has none. It cannot cite a source, and fixes none of the price errors.

> **Notes:** A alone leaves the stranding risk open, and that harm is irreversible. B alone leaves the 50% untouched. Together they fit in 20 days once each is cut to its core. What would change my mind: if A's core needed more than about 14 days, B would shrink to B1, B2 and B4. So the decision is one rule.

### 10 · One rule, two evidence providers

**Pivot slide**, ground #3A0716, tracker at step 4 in white tones. Eyebrow in 72% white: `THE DECISION`.

**Title** (Instrument Serif 96): **One rule, two evidence providers**

**The rule**, Inter 600 44 / 56, white, full width: No price, availability or policy claim reaches the user without evidence from its source.

**Infographic: a three-lane rule diagram.** Three horizontal lanes separated by 12%-white hairlines. Each lane has four parts:

- a label on the left (Inter 600 26);
- an evidence icon;
- one sentence (Inter 24 / 36, 80% white);
- an option badge on the right.

| Label | Icon | Sentence | Badge |
|---|---|---|---|
| **Volatile facts are fetched** | `clock` | Prices render from a live offer at the moment the user decides. | "Option A, rebuilt as A1–A6" |
| **Regulatory facts are cited** | `passport` | Policy answers quote a retrieved official snippet, or hand off to the page and a person. | "Option B, plus the router rule that makes it fire" |
| **Nothing is memorised** | `close` | Option C is cut. | "Cut" |

**Red:** the "Cut" badge, outlined in `--color-primary`.

This is the one slide allowed a "not X, but Y" line. Put it in the notes, not on the slide.

> **Notes:** The answer isn't A, B or C. It's the rule, and A and B are the two ways the rule gets its evidence. C would move staleness into the weights, where it has no age and no timestamp. Now it has to fit in 20 engineer-days.

### 11 · Severity decides first, then RICE ranks

Tracker at step 5. Eyebrow `3 · PRIORITISATION`. Lede: RICE measures expected value, so it can't see irreversibility. Many ₹500 gaps would outscore one stranded traveller.

**Infographic, left 1100px: a severity × effort selection matrix.** It shows why each feature was picked, not just its score. Every feature from plan section 3 is one dot.

**Axes**

- **Y, severity of the harm it prevents.** This is the plan's RICE impact score, drawn as three labelled bands, bottom to top:
  - 1 · Visible mismatch
  - 2 · Failed or abandoned booking
  - 3 · Stranding or money lost
- **X, effort in engineer-weeks, log scale.** Ticks at 0.1, 0.2, 0.5, 1, 2 and 4, with engineer-days beneath each tick in tertiary (0.5, 1, 2.5, 5, 10, 20). A log scale is used because efforts run from half a day to the whole budget; say so in the caption.

**Quadrant lines**

- **Vertical split at 0.65 engineer-weeks**, labelled "fits one V1 lane".
- **Horizontal split between bands 2 and 3**, labelled "irreversible harm".

**Quadrant labels** (Inter 600 18, 72% white, in each corner):

| Quadrant | Label | Sub-line (16px tertiary) |
|---|---|---|
| Top left | Severe and cheap · build in V1 | B6 and B7 wait: they need B5's data |
| Bottom left | Broad and cheap · RICE decides the order | |
| Top right | Severe but slow · V2, contract lead time | |
| Bottom right | Slow for what it fixes · later waves or cut | |

**Dots.** Place every dot exactly on its effort (x) and inside its severity band (y). Inside a band, spread dots vertically so no dot or label overlaps; only the x position is exact. Copy each value from plan section 3:

| Feature | Severity | Effort (eng-wk) | Reach /mo | RICE | Wave |
|---|---|---|---|---|---|
| A4 Honest quote language | 1 | 0.1 | 100,000 | 800,000 | V1 |
| A6 Quote the total | 1 | 0.2 | 90,000 | 360,000 | V1 · Tier 0 |
| A8 Cache key fix | 1 | 0.3 | 90,000 | 150,000 | V1 buffer |
| B3 Last-verified stamp | 1 | 0.3 | 30,000 | 80,000 | V1 stamp |
| T1 Fare-attribute answers | 1 | 0.8 | 15,000 | 15,000 | V2 |
| T2 Constraint carry-through | 1 | 0.8 | 40,000 | 25,000 | V3 |
| A10 Price hold | 1 | 2.0 | 40,000 | 10,000 | V3 |
| A5 Supplier fallback | 2 | 0.3 | 9,000 | 48,000 | V1 |
| A3 Checkout re-validation | 2 | 0.4 | 40,000 | 200,000 | V1 |
| A1 Price cards bound to an offer ID | 2 | 0.5 | 90,000 | 288,000 | V1 |
| A2 Re-price at decision | 2 | 0.5 | 60,000 | 192,000 | V1 |
| A9 Hotel live availability | 2 | 0.6 | 45,000 | 120,000 | V2 first |
| A7 Late-bound supplier fields | 2 | 1.0 | 90,000 | 90,000 | V2 branch |
| T3 Post-booking alerts | 2 | 1.5 | 10,000 | 6,667 | V3 |
| B4 Human handoff | 3 | 0.1 | 3,000 | 72,000 | V1 · Tier 0 |
| B7 Verified contact registry | 3 | 0.2 | 5,000 | 60,000 | V2 · Tier 0 |
| B1 Policy router hard rule | 3 | 0.3 | 30,000 | 240,000 | V1 · Tier 0 |
| B6 Entry-requirement checklist | 3 | 0.4 | 12,000 | 72,000 | V2 · Tier 0 |
| B2 Cite-or-deflect gate | 3 | 0.6 | 30,000 | 120,000 | V1 · Tier 0 |
| B5 Authoritative entry-rules feed | 3 | 1.0 | 12,000 | 28,800 | V2 · Tier 0 |
| Option A as written | 2 | 1.5 | 90,000 | 96,000 | Comparison |
| Option B as written | 3 | 1.0 | 30,000 | 54,000 | Comparison |
| Option C as written | 2 | 4.0 | 30,000 | 4,500 | Cut |

**Encodings**

- **Dot area** is proportional to monthly reach: 3,000 → 12px diameter, 100,000 → 44px. Add one small size key under the chart (3k · 30k · 100k). This is the only key; everything else is labelled directly.
- **Fill shows the wave:**
  - V1: solid white at 72%.
  - V1 buffer and V1 stamp (A8, B3): 24% white fill with a dashed white ring.
  - V2: hollow white ring.
  - V3: hollow ring at 24% white.
  - Options as written: dashed outline, labelled in italics.
- **Tier 0** features get a 2px `--color-warning` ring, 3px outside the dot.
- **Labels** sit beside each dot: feature ID and short name in Inter 600 16, with the RICE score after a middle dot in tertiary, for example "B1 Router rule · 240k". Draw a 1px leader line where a label has to move away from its dot.
- **Red:** the Option C dot, filled `--color-primary`, labelled "C · 4,500 · cut: 30% confidence, the whole budget". It is the lone dot at the far right.

**Two annotations** (16px tertiary, with a 1px leader line):

- **On A9:** "Fits a lane, but flights drive the 50%. Hotels lead V2."
- **On A6,** which sits low but carries a Tier 0 ring: "Tier 0 by legal exposure (drip pricing), so it jumps the queue."

**How to read it** (one line under the chart, Inter 18, secondary): The top-left quadrant ships first. The bottom-left ships in RICE order until the 20 days run out. Everything on the right waits for data, a contract, or V2.

**Right, 440px: one card, "The gate".** Tier 0 = prevents an irreversible harm (stranding, denied boarding, fraud) or a legal exposure (drip pricing). V1 takes every Tier 0 feature that needs no outside contract, then the highest RICE until 20 engineer-days run out.

Caption: *Effort is on a log scale. Severity is the RICE impact score. RICE = reach × impact × confidence ÷ effort. Reach uses the plan's assumptions: 100,000 trip sessions a month reach a quote. Full table: A01.* Put the tag *Assumption* beside it.

> **Notes:** Severity first is a value judgement, and I'm naming it as one. RICE is right about expected value and blind to irreversibility, so I use it for the first and a gate for the second. Two Tier 0 items wait for V2 on purpose: the visa feed needs a data contract with lead time. So what does the V1 system look like?

### 12 · Two independent nets check every claim

Tracker at step 5. Eyebrow `4 · ARCHITECTURE`. Lede: V1 closes 14 of 40 failure modes and narrows 13 more. The options as written fully covered 8.

**Infographic: the V1 evidence path**, a flow diagram of hairline boxes, radius 12, using the full width:

User asks → Router (claim type) → three evidence sources, stacked:

- Live offer record
- Retrieved official snippet
- None needed, for travel concepts

→ **Validator** (scans every reply for prices, dates and policy terms, whatever the router said) → Reply with evidence, or "let me check" / hand-off.

- Draw a second, curved hairline from the Router straight to the Validator, labelled "general chat still passes the validator".
- **Red:** a 6px dot on the Validator box, labelled "second net".

**Beneath, two short cards side by side:**

- **The model never writes a price (D5).** Every figure renders from an offer record. The validator strips any currency figure in the model's text that has no offer ID.
- **The weak point is named.** The claim classifier is a single point of failure, which is why the validator runs independently of the router.

Caption: *Freshness budget per claim type: A04.*

> **Notes:** Models restate, round and total numbers; the $1 Tahoe and the Accor mismatch both came from model-written prices. What would change my mind: the validator blocking honest replies at a rising rate. Then I fix patterns; I don't remove the rule. Here's what the user sees.

### 13 · The assistant can't make up a fare

Tracker at step 5. Eyebrow `EXPERIENCE · ON A GLANCE SURFACE`.

**Three phones side by side**, each about 720px tall:

1. `assistant-lockscreen.svg`, caption: A live fare on the lock screen, with the time it was checked
2. `assistant-chat.svg`, caption: The fare card renders from the API; the model never types the number
3. `assistant-policy.svg`, caption: Rules cite a source and last-verified date, or hand off to a person

**Right column, 380px: four rules**, each an icon plus one sentence:

- `shield-check` · Every price is bound to an offer ID.
- `clock` · Every price says when it was checked: "Live · checked 9:41" in green, "Cached 9:32" in amber.
- `passport` · Every rule shows its source and last-verified date.
- `chat` · No source, no answer. Visa and airport cases get a person.

**Foot line** (Inter 22, secondary): Glance users are mostly on mobile, in short sessions. A "Checking live fares…" state covers the 1–2 s supplier call instead of a blank screen.

**Red:** inside the mockups only.

> **Notes:** Live calls fire only at decisions, identical calls share one request, and time to price has a hard limit of baseline plus 1.5 seconds. That's my answer to the latency worry. Next: who builds this, in what order.

### 14 · Two engineers, ten days, and neither waits on the other

Tracker at step 5. Eyebrow `5.1–5.3 · EXECUTION`. Lede: 18.5 of 20 engineer-days planned, 1.5 held back until week-one data says where they're needed.

**Infographic: a two-lane Gantt**, days 1–10 across the full width, day gridlines in divider colour.

- **Engineer 1 · price track · 9.5 of 10 days:** A1 price cards + validator → A6 total with fees → A2 re-price at decision → A5 supplier fallback → A3 checkout re-validation.
- **Engineer 2 · policy and platform · 9 of 10 days:** E1 claim telemetry → E2 replay of 200 conversations → A4 honest quote language → B1 router rule → B2 cite-or-deflect → B3 last-verified stamp → B4 human handoff → flags and rollout.
- **PM lane** (white 72%): KPI definitions · labelling the 200 replay conversations · all user-facing copy · supplier and legal · go or no-go at each step.
- **Bar lengths:** proportional to effort. Where the plan does not give per-feature days, derive them from the RICE effort column (1 engineer-week = 5 days). Keep each lane's total at 9.5 and 9.
- **Milestone diamonds** (8px, rotated, white outline):
  - Day 2: baseline logged
  - Day 3: A4 to 50% of users
  - Day 7: buffer decision
  - Days 8–10: A2 in shadow
  - Day 10: Gate 1
- **Red:** the Gate 1 diamond.

**Beneath, two cards:**

- **Buffer rule, Day 7.** Price gaps track party size or currency → A8. Hotels above 25% of trip errors → start A9. Otherwise, harden the validator.
- **Cut line, Day 6.** If behind, drop B3's stamp first, then the buffer item. Never drop A5 (A2 can't ship without it) or B4 (the stranding path).

> **Notes:** "4 engineer workweeks" together with "2 weeks" under Option C reads as two engineers. Every dependency stays inside one lane, so neither waits. What would change my mind: a different team shape from the eng lead in week 0. I'd keep the rule and re-cut at the same cut line. Then, how do we know it worked?

### 15 · Tuning is config, not code

Tracker at step 5. Eyebrow `5.4 · THE V1 SANDBOX`. Lede: V1 exposes its trade-offs as knobs, so improving it means turning a knob and reading the result.

**Infographic, top: the metric tree.**

One north-star tile at the top, full width, radius 24:

- **Trip booking error rate**, measured against the decision price (the total on the card when the user tapped Book).
- Three figures in Inter 700 tabular 96: `~50%` today → `≤ 30%` after V1 → `≤ 15%` after V2.
- **Red:** the `≤ 30%` figure.
- Tag: *Sizing: 25–32% after V1, about 11% after V2. Sizing, not forecast.*

Under it, joined by hairlines, **three driver tiles:**

| Driver | Baseline → target |
|---|---|
| Decision-price accuracy, flights | ~60% → ≥ 85% |
| Grounded claim rate | measured in week 1 → ≥ 99% |
| Policy deflection rate | 0% → a 10–30% band. Caption: "a band, not a ceiling: a gate that deflects everything scores 100% grounded" |

Two **guardrail tiles**, 24% white borders:

- Time to price (p90) ≤ baseline + 1.5 s
- Assistant booking conversion: no drop beyond 5%

**Infographic, bottom: the knob panel.** Four knobs drawn as slider tracks with their range and a marker at the start value, the trade-off in 16px tertiary under each:

| Knob | Start | Range |
|---|---|---|
| K1 re-price window | 10 min | 0–30 min |
| K2 supplier timeout | 1.5 s | 0.8–3 s |
| K3 fallback age | 30 min | 0–60 min |
| K6 entry-rule freshness | 7 days | 1–14 days |

Caption: *KPI definitions and the "if this happens, do this" rules: A05.*

> **Notes:** The metric compares the payment price with the decision price, not the last price shown. Otherwise the disclosure feature would make every checkout match and the number would look fixed when users still paid more than they chose. Complaints are read alongside, never used as a target. Last step: what V1 leaves open.

### 16 · Each version has to earn the next one

Tracker at step 5. Eyebrow `5.5–5.8 · ROADMAP`.

**Infographic, left: the version roadmap** as stacked phase bands with gates between them:

| Phase | Content |
|---|---|
| **V1** (weeks 1–4) | build, shadow 2–3 days, then 10% · 50% · 100% of users, split by user |
| **Gate 2** | 7 days at 100% · error rate ≤ 30% · grounded ≥ 99% · deflection 10–30% · guardrails hold |
| **V1.1** | tuning only, no new features |
| **V2** (next 4 engineer-weeks, target ≤ 15%) | A9 hotels · B5 + B6 entry-rules feed and checklist · T1 baggage and meals · B3 change detection · B7 contacts. The lead item switches on V1's data |
| **V3** | A10 holds · T2 constraints in code · T3 post-booking alerts · a confirmation gate before any agentic booking, nothing pre-selected |

- **Red:** the Gate 2 marker.

**Right: "Knowingly not in V1"** (D9), four rows, each with its V1 mitigation in secondary:

- Hotel live availability · shown with its time, "confirmed at booking"
- Fare jumps before payment · disclosed before the payment page
- Meal and baggage answers · deflected to the fare details
- Authoritative visa feed · cite-or-deflect plus human handoff

> **Notes:** Naming what V1 still gets wrong is deliberate; a plan that claims to fix everything hasn't looked closely. Seven mechanisms produce "wrong price", and telemetry fingerprints which one dominates, so V2's first item is chosen by data (A03). Option C comes back only as a phrasing layer over retrieved text, never as a source.

### 17 · What would change my mind

**Ground:** stage + `stage-signal.svg`. No tracker.

**Title** (Instrument Serif 88): **What would change my mind**

**Lede** (Inter 26 / 38, 85% white): The rule survives every assumption below. Only the order of work changes.

**Four rows**, hairline-separated, Inter 22 / 34. Each row: the assumption in white, then "If wrong, I…" in 72% white. Copy from the reasoning's assumptions table, the four with the biggest effect:

| Assumption | If wrong, I… |
|---|---|
| Team is 2 engineers × 2 weeks | Keep the rule; re-cut V1 at the same cut line |
| Price errors come mostly from aged or restated quotes | Spend the buffer on A8, or pull A7 or A10 into V2 first |
| Hotels are under 25% of trip errors | Start A9 in the buffer and lead V2 with it |
| A policy document store exists | Build a minimal index of official pages first; B2 deflects more at the start |

**The one question for day one**, Inter 600 28, white: What changed 4–6 weeks ago? A model or prompt change, a cache TTL change, a new supplier, traffic past rate limits or seasonal demand each points to a different first fix.

**Closing line**, Instrument Serif italic 40, white: Volatile facts are fetched. Regulatory facts are cited. Nothing is memorised.

**Contact** (Inter 20, 64% white): Prithwish Chakraborty · f20240470@pilani.bits-pilani.ac.in

**Red:** `kit/11_SVG_ASSETS/decorative/live-signal.svg` at 64px, bottom right.

> **Notes:** Every assumption is checked in week 0 or week 1, and each has a stated response. None of them reopens Option C. Happy to take questions; the appendix has the full tables, the decision log and the questions I expect.

---

## 7 · Appendix (backup, shown only when asked)

Appendix slides use the content ground, carry no tracker, and may be denser than the main deck (tables down to 16px), but still one topic per slide. Each gets a title that states its point.

| Slide | Title | Content |
|---|---|---|
| **A01** | How the ranking was scored | Full RICE table, all rows from plan section 3, including the options as written. A method strip on top with the impact, confidence, effort and Tier 0 scales, copied from the plan. |
| **A02** | Twenty-two fixes for fourteen problems | Problem → feature coverage map. Left: P1–P14 (copy from plan 2b "The problem list"). Right: four families as chip stacks, E · Measure (E1, E2), A · Prices and availability (A1–A10), B · Policy (B1–B7), T · Fare attributes and the trip (T1–T3). Hairlines from each problem to the chips that solve it, copied from the "Solves" column of plan 2c; do not guess a mapping. V1 chips white on `--color-surface-muted`; V2 and V3 at 24% white. Red: the hairline from P5 to B1. |
| **A03** | Seven ways a price goes wrong, each with its own fingerprint | Seven small-multiple schematic charts, 4 + 3 grid, one per mechanism (quote aged, fee-shaped gap, fare bucket closed, wrong cache key, model-restated number, partial supplier results, demand spike), each with its fingerprint and "Fixed by" chip, from plan 1.5. Caption: *Schematic shapes, not data.* Right column: the four causes the brief doesn't name, from plan 1.6. Red: the "quote aged" line. |
| **A04** | Every claim has a freshness budget | Six vertical cards, one per claim type: evidence required, budget at V1 start as a stat, and "if missing or too old" in amber. Copy from plan 4, "Freshness budget per claim type". |
| **A05** | Every metric is computed from what users see and do | KPI definitions table from the plan, the health checks (unwarned change rate ≈ 0 · fallback < 5% · live checks per booking inside supplier allowance · validator block rate stable · handoff wait within target), and the "if this happens → do this" table from plan 5.4. Note: price tolerance ₹100 or 1%, whichever is larger, to agree with finance. |
| **A06** | 39 tickets, TRV-10 to TRV-48 | The four epics (TRV-1 to TRV-4) with done-when criteria. The sprint rhythm on one line: Sprint 1 Days 1–5 (20 of 20 points) · Sprint 2 Days 6–10 (17 + 3 buffer) · Sprint 3 weeks 3–4, sandbox, no points. |
| **A07** | Twelve decisions, and what would reverse each | Decision log D1–D12 as one table (Inter 16 / 22): Decision · Chose · Rejected · What would change my mind. Copy from the reasoning, shortening each cell to one line. Change "we" to "I". |
| **A08** | Questions I expect | Six jury questions from the reasoning, each as the question in Inter 600 18 and a two-sentence answer in 16 / 24 secondary, in a 2 × 3 grid: "Why spend any budget on visas?" · "Aren't you ignoring your own RICE?" · "Why not C?" · "Won't deflection lose users?" · "Doesn't A's latency lose bookings?" · "If you had only one week?" Put the other five questions and full answers in this slide's speaker notes. |
| **A09** | Assumptions, and the questions for week 0 | The full six-row assumptions table from the reasoning (Assumption · Value used · Checked by · If wrong, I…), each tagged *Assumption*, plus the five week-0 questions from plan 1.7. |
| **A10** | Sources | The plan's source list, titles only, 16px, in two columns. |

---

## 8 · Final checks before rendering

1. **Numbers copied, not computed.** Every figure matches `ref/Full plan.pdf` or the reasoning file. Check that 60% × 92% × 92% = 50.8% and 98% × 92% × 92% = 82.9% still multiply, but do not change them.
2. **Every assumption is tagged.** Every volume, share, target and sizing carries its tag.
3. **Titles tell the story.** Read the 17 titles alone. They must match section 5 exactly, and read as one argument.
4. **The flow holds.** The step tracker shows the right step on slides 03–16. Slide 02's agenda slide numbers match the deck. Every set of speaker notes ends with a hand-off to the next slide.
5. **Density.** Every main slide has one infographic, at most about 60 words outside it, no table longer than seven rows (except slide 11's matrix data, which is drawn, not printed), and visible empty ground. Record word counts in the README.
6. **One red per slide.** Fill the README table. Any slide with two, remove one.
7. **Colour discipline.** Lavender only on assistant output inside mockups. No logos. "Glance" in plain text.
8. **Type.** No text under 16px except the tracker labels and table headers at 14. No serif outside titles and the closing line. Stats in Inter 700 tabular.
9. **Voice.**
   - Search all slide text and notes for the banned words and for "—". There must be zero hits.
   - Count "not X, but Y" constructions. There must be at most one, in slide 10's notes.
   - Decisions are in the first person.
10. **Visual review.** Render and look at every PNG at 50% zoom next to `kit/13_DECK_ASSETS/png/`. Fix anything that looks like a different system or looks crowded.
