# Claude Code prompt · case deck (clean boards edition) · Glance26 AI PM intern case

**How to use this.** Paste everything below the line into Claude Code. These should already be in the repo root, with the folder names exactly as shown:

- `kit/`: unzip `Glance-Inspired-Design-System.zip` and rename `glance-inspired-design-system/` to `kit/`
- `ref/Glance-Inspired-Design-System.pdf`: the visual reference
- `ref/Full plan.pdf`: the content source for facts, tables and numbers
- `ref/Travel_Assistant_Decision_Reasoning.md`: the content source for the argument, the decision log and the jury questions
- `ref/inspiration/` (optional): three strong case-study decks, kept only to study their *structure* (a Netflix case, a healthcare-data case, a boredom-app case). If the folder is missing, the patterns are described in section 3, so nothing is lost. Never copy their wording, colours, logos, photos or screens.

**Deliverables, all in `out/`:**

- `deck.pdf`: the main deliverable. 24 pages at 1920 × 1080, vector, bookmarked, with working links. The jury reads this, often without me speaking, so it has to carry the argument on its own.
- `deck-notes.pdf`: one page per board with its speaker notes underneath, as a pre-read handout.
- `deck.pptx`: the same pages as full-bleed images with notes, for presenting.
- `slides/*.html` and `png/*.png`: the sources and the renders.

Every number below comes from the Full plan or the Decision Reasoning. Claude Code must not change, round or add a number. Every sentence on a board is drawn from those two files (or from the case brief inside the plan); new wording is allowed only to connect facts, never to add one.

---

## 1 · Task

Build a twelve-board main deck, an appendix divider and an eleven-slide appendix (24 pages in all) at 1920 × 1080. It is for a product manager intern (AI) case round at Glance.

**What a board is.** Strong case-study submissions do not spread an argument over twenty airy slides. They put one chapter on one page: a persistent chapter bar at the top, a sentence-title, then three to five panels, each with a label tab, each holding one picture and a few lines. That is the format here. Twelve boards carry the whole argument, and the appendix holds the tables a juror may ask for.

- **Order and flow** follow the five steps in `ref/Travel_Assistant_Decision_Reasoning.md` ("How we got there"): reframe the problem, read the 50%, derive the principle, test the options, fit it to 20 engineer-days. The options are judged against causes, not against each other.
- **Facts and tables** come from `ref/Full plan.pdf`.
- **Look** follows the Wake design system in `kit/` and `ref/Glance-Inspired-Design-System.pdf`. Everything on a board is built from the kit: its tokens, icons, components, illustrations, masks, patterns and phone screens. No stock photos, no photos of people, no outside logos, no other fonts.
- **Use the plan fully.** Before designing, look at `ref/Full plan.pdf` as page images as well as text (`pdftoppm -r 60 -png`), so you see its tables, matrices and diagrams as laid out. Every section of the plan (1.1 to 1.7, 2a, 2b, 2c, 3, 4, 5.1 to 5.8) must land on a numbered board or appendix page. Redraw the plan's diagrams in the deck's style; never paste page images.
- **Use the kit fully.** Section 2b says which card, badge, chip, tab, carousel, overlay, input, illustration, mask, pattern, gradient and screen template goes on which board.
- **Own infographics.** Every panel holds a picture that answers the panel's question: a matrix, a rail, a bullet chart, a timeline, a flow, a rated table. Where the plan has a table, turn it into a picture and keep the table in the appendix.
- **Flow.** The PDF is read in order. Each board hands the reader to the next: the chapter bar, a `Next:` line in the footer, ghost chapter numerals and recurring visual anchors (section 3).
- **Density.** A board is full but ordered: title, then panels, then bold key terms, then detail. Anything a juror might ask about but does not need in order to follow the argument goes to the appendix or the speaker notes.

Read these before writing any code. They are authoritative.

- `kit/DESIGN_SYSTEM_SUMMARY.md`
- `kit/01_DESIGN_PRINCIPLES/visual-principles.md` and `content-principles.md`
- `kit/03_TYPOGRAPHY/typography-spec.md` and `kit/04_COLORS/color-system.md`
- `kit/07_COMPONENTS/cards/README.md` and `kit/07_COMPONENTS/assistant/README.md`
- `kit/14_IMPLEMENTATION/component-specifications.md`
- every `kit/07_COMPONENTS/*/README.md` (cards, assistant, badges, buttons, carousels, chips, content-modules, inputs, media-modules, navigation, overlays, tabs)
- `kit/08_PATTERNS/commerce.md`, `notification.md` and `recommendation.md`; `kit/09_SCREEN_TEMPLATES/README.md`; `kit/11_SVG_ASSETS/README.md`; `kit/12_UI_EXAMPLES/README.md`; `kit/13_DECK_ASSETS/README.md`
- `ref/Full plan.pdf`, all 36 pages. Extract it with `pdftotext -layout` and keep the text beside you. Also render every page to PNG and look at it: the plan's matrices, journey tables and failure map are laid out on purpose. Wherever this prompt says "copy from the plan", copy the table verbatim.
- `ref/Travel_Assistant_Decision_Reasoning.md`, in full. Wherever this prompt says "copy from the reasoning", copy verbatim, changing "we" to "I" only where the prompt says so.

Open `ref/Glance-Inspired-Design-System.pdf` at pages 1, 6, 8, 12, 41 and 42, and every PNG in `kit/13_DECK_ASSETS/png/`. The deck must look like it belongs to that system. Match that finish, not a generic dark template. If `ref/inspiration/` exists, look at each deck once, only to see how a board is organised.

---

## 2 · Build method (follow exactly)

1. Write each slide as standalone HTML at exactly 1920 × 1080: `slides/01.html` to `slides/12.html` (the boards), the appendix divider `slides/A00.html`, and `slides/A01.html` to `slides/A11.html`. Start every board from one shared skeleton, `slides/_board.html`: chapter bar, title zone, board area, footer.
2. Each page links `../kit/14_IMPLEMENTATION/tokens.css`, `../kit/14_IMPLEMENTATION/components.css` and a shared `slides/deck.css`.
   - `components.css` already loads Inter and Instrument Serif from `kit/fonts/`.
   - Do not add web fonts, CDNs or JavaScript libraries. The build must run offline.
3. Inline `kit/11_SVG_ASSETS/icons/sprite.svg` once per slide. Use icons as `<svg class="icon"><use href="#i-plane"/></svg>`.
4. Draw every chart and diagram as inline SVG or HTML, using token colours only. No chart libraries and no raster images of charts.
5. Show phone screens as `<img>` of the kit's SVGs, in `kit/12_UI_EXAMPLES/travel-assistant/`. Never redraw a screen in HTML.
6. Build the chapter bar, the panel with its label tab, the rated cell, the footer and the `Next:` line (section 3) once, as classes in `slides/deck.css` plus small HTML snippets every board includes, so all boards match. Panels are `.panel` and `.panel__tab`; do not restyle them per board.
7. Render every slide to PNG at 2× (3840 × 2160) with Playwright.
   - Use a fixed 1920 × 1080 viewport and `deviceScaleFactor: 2`.
   - Wait for `document.fonts.ready` before capturing.
8. Assemble `deck.pptx` with python-pptx.
   - Slide size 16:9. Each PNG goes full-bleed at (0, 0), with no other shapes.
   - Put the speaker notes from this prompt into each slide's notes.
   - The appendix divider is `slides/A00.html`, titled "Appendix", built on the layout of `kit/13_DECK_ASSETS/section-divider.svg`, with board 12's ground. It sits between board 12 and A01.
   - Do not lay slides out in python-pptx itself. It cannot reproduce scrims, glass controls, hairlines or these fonts.
9. Build the PDF from one combined page, so links and bookmarks work.
   - `build.sh` concatenates all slides into `deck.html`, each as `<section id="s01">` to `<section id="A11">` at 1920 × 1080, with `@page { size: 1920px 1080px; margin: 0 }` and a page break after each. Inline the icon sprite once.
   - Print with Playwright: `page.pdf({ width: '1920px', height: '1080px', printBackground: true, outline: true, tagged: true, preferCSSPageSize: true })`. Every board title is an `<h1>`, so the PDF gets a bookmark tree: the seven chapters as branches, board titles as entries, and Appendix as its own branch.
   - Links: the chapter-bar tabs link to the first board of their chapter, and the agenda cells on board 02 do the same. Each footer `Next:` line links to the next board. Every "Full table: A0x" line links to that appendix page, and each appendix footer has a small "Back to board NN" link. Use `<a href="#s09">`.
   - Set the PDF title ("Make it check before it speaks · Glance26 AI PM case") and author (Prithwish Chakraborty).
   - Also build `deck-notes.pdf` from `notes.html`: A4 landscape, one board image (960 px wide) per page with its speaker notes underneath in Inter 20 / 30, page numbers matching `deck.pdf`.
   - Checks: `pdfinfo deck.pdf` shows 24 pages; `pdffonts deck.pdf` shows Inter and Instrument Serif embedded; text is selectable; the file is under 20 MB. If it is larger, reduce image sizes, never the layout.
10. Add `build.sh`, which runs the whole chain.
11. Add `README.md` with:
    - how to edit one slide and rebuild;
    - a table listing the one red element on each board;
    - the kit coverage table (section 2b) and the plan coverage table (section 8, check 13);
    - the on-slide word count of each board (see the density rule).
12. Comment the HTML. This deck will be revised several times.

---
## 2b · Use the design system fully

The kit has more than tokens. Every family below appears in the deck at least once, on the boards listed. Open the component's README in `kit/07_COMPONENTS/` and the asset in `kit/` before using it, and use the kit's own SVG or CSS rather than redrawing it. Colour any decoration with token colours only. A decoration in `--color-primary` is that board's one red element.

### Components (the widgets)

| Kit component | Boards | Used for |
|---|---|---|
| Card A · hero (`cards/card-a-hero.svg`) | 02 | The rule, over `illustrations/plane.svg` with `gradients/scrim-bottom.svg` under the text |
| Card B · standard | 06 | The three option columns: illustration on top, title, verdict chip (A: `plane.svg`, B: `temple.svg`, C: `iris.svg` at 40% opacity to show it is cut) |
| Card C · compact | 05 | The six failure cases, each with a 56px illustration thumbnail cropped with `decorative/mask-rounded.svg` |
| Card D · commerce | 08 | The live fare card: price, "Live · checked HH:MM" in success, "See fare" |
| Card E · recommendation | 07 | "The gate": a recommendation with its reason |
| Card F · editorial | 03 | The three "where it breaks" rows: headline, one line, source tag |
| Assistant cards (`assistant/assistant-cards.svg`): fare card live, cached and changed; cited policy answer; deflect card | 08 | The evidence outputs at the end of the pipeline, and the callouts on the phones |
| Badges | 06, 07, A02 | Option and verdict badges (06), wave and Tier 0 badges (07) |
| Chips | 05, 06, 09, 11, A02 | Feature-ID chips (A1, B2, …) and wave filters |
| Tabs | 11 | V1 · V1.1 · V2 · V3 across the roadmap, V1 active |
| Carousel (`carousels/`) | 11 | "Knowingly not in V1": four cards, a fifth peeking at the right edge, pagination dots |
| Overlays (`overlays/`) | 08 | The bottom sheet "Fare changed since you looked" as one of the four evidence outputs |
| Inputs (`inputs/`) | 08, 10 | The chat input bar under the chat phone (08); slider and toggle styling for the knob panel (10) |
| Navigation (`navigation/`) | 02–12 | The chapter bar, drawn in the segmented-tab style of this component |
| Content modules (`content-modules/`) | 02, 05, 10 | Stat tiles: the four commitments, the 8%, the north star |
| Media modules (`media-modules/`) | 01, 03 | Masked illustration blocks |
| Buttons | 01, 08 | The primary button appears only inside mockups |

### Assets

| Kit asset | Boards | Job |
|---|---|---|
| `backgrounds/stage-signal.svg` | 01, 12, A00 | Ground |
| `backgrounds/iris-aurora.svg` | 06 | At 25% opacity inside the decision band, top right only |
| `backgrounds/light-iris.svg` | 04 | At 40% opacity on the light board's ground |
| `patterns/dot-grid.svg` | 05, 07 | Behind the plot areas, 4% white |
| `patterns/contours.svg` | 01, 12, A00 | Behind the title, 6% white |
| `patterns/scan-lines.svg` | 03 | Behind the dashed "missing check" box only, 8% |
| `decorative/section-separator.svg` | 02, A00 | Between the brief and the rule on 02; on the divider |
| `decorative/focus-brackets.svg` | 03, 05, 09 | Frames the one thing to look at. White 72%, unless it is the board's red |
| `decorative/highlight-underline.svg` | 01, 06, 12 | Under one word of the title |
| `decorative/accent-arc.svg` | 01 | Behind the phone |
| `decorative/signal-blob.svg` | 06 | A glow behind the rule text in the decision band, 20% |
| `decorative/iris-sparkle.svg` | 08 | Marks text the assistant wrote (lavender) |
| `decorative/mask-ticket.svg` | 04, A10 | The example request as a ticket-shaped card |
| `decorative/mask-pill.svg`, `mask-arch.svg`, `mask-rounded.svg` | 01, 03, 05 | Illustration crops |
| `decorative/live-signal.svg` | 08, 12 | The "Live" marker on the fare card and the closing board |
| `gradients/*` | 02, 05, 08 | Scrims under text on illustrations; `iris-night` behind the assistant phone on 08 at 30% |
| `illustrations/*` | 02, 03, 05, 06, A04 | `plane.svg`, `hotel.svg`, `temple.svg`, `bag.svg`, `food.svg`, `city.svg`, `iris.svg`. On 03, plane marks the Transactional group, temple the Regulatory group, bag and food the Fare attribute group |
| `09_SCREEN_TEMPLATES/*.svg` | 04, A10 | Stage thumbnails: 1 `search`, 2 the assistant chat, 3 `product-detail`, 4 the assistant policy phone, 5 `commerce`, 6 `notifications`, 7 `lockscreen`, 8 `profile` |
| `12_UI_EXAMPLES/dashboard.svg` | 10 | Layout reference for the KPI board. Look at it; do not embed it |
| `12_UI_EXAMPLES/travel-assistant/travel-assistant-flow.svg` | 08 or A10 | The assistant's own flow of screens. Use it on 08 under the phones only if it reads at 16px or more; otherwise on A10 |
| `13_DECK_ASSETS/*.svg` | see right | Starting grids. Open each PNG, follow its layout, replace the content: `title-slide` → 01, `summary-slide` → 02, `architecture-slide` → 03, `component-slide` → 06, `interaction-model-slide` and `card-anatomy-slide` → 08, `section-divider` → A00, `closing-slide` → 12 |
| `06_ICONS` sprite | all | Use the same six icons for the six claims everywhere: flight price `plane`, hotel availability `hotel`, visa and entry rules `passport`, refund terms `refresh`, baggage `baggage`, meal `meal`. Chapter bar: `info`, `search`, `trending`, `shield-check`, `compare`, `calendar`, `refresh`. Status: `check`, `close`, `alert`, `clock`, `live`, `chat`, `lock` |
| `logos/wake-*` | phones only | Never on a board |

### Coverage rule

The README lists, for every row in the two tables above, the board it landed on. If a row cannot be used without crowding a board, move it to the board named as the alternative, or to the appendix. Do not drop it silently.

---

## 3 · Design rules

### The board format (read first)

A main page is a board: one chapter's argument on one page, in panels. These patterns come from strong case-study decks. Use the structure, in Wake's look:

| Pattern | What it is | Where it goes |
|---|---|---|
| Chapter bar | A permanent strip at the top with every chapter as a tab and the current one lit | Boards 02–12 |
| Panel with a label tab | A rounded box with a small pill label straddling its top edge. The label names the question the panel answers ("WHO OWNS EACH CLAIM") | Every board |
| Question, then answer | Each panel ends with one bold line or caption that states what to notice | Every panel |
| Rated matrix with a total | Options across, criteria down, tinted cells, a scored last row | Board 06 |
| Priority stack | Stacked cards "P1, P2, P3", each with its reason | Board 07 |
| Annotated screens | Phones with numbered dashed callouts to the words that explain them | Board 08 |
| Phase table | Columns are phases, rows are timeline, goal, key activities | Board 11 |
| Hypothesis and validation | Two aligned columns: what I assumed, how it gets checked | Board 12 |
| Pitfall and mitigation | Two aligned columns | Board 11 |
| Trade-off box | "What I gave up, and for what" | Board 11 |
| Day-in-the-life path | A dotted path through numbered stages with a feeling or state at each | Board 04 (the trip) |
| Big-number row | Round or square stat tiles with a caption underneath | Boards 02, 05, 10 |

### Grounds

| Page | Ground | Text |
|---|---|---|
| Cover (01) and closing (12) | `--color-stage` #000 with `kit/11_SVG_ASSETS/backgrounds/stage-signal.svg` full-bleed | White |
| Boards 02, 03, 05, 06 (above its band), 07–11 | `--color-background` #0C0C10; panels on `--color-surface` #16161B | `--color-text-primary`, `--color-text-secondary` |
| Board 04, the only light board | `data-theme="light"` on `<body>`, ground #F6F5F8 with `light-iris.svg`, white panels with `--shadow-1` | #0C0C10 |
| Board 06, decision band | The lower band of the page sits on `--color-primary-subtle` #3A0716, full width, radius 24 | White title, 80% white body |
| Appendix (A00–A11) | Content ground, with the eyebrow prefixed `APPENDIX ·` | As content |

### Page grid (1920 × 1080)

- **Chapter bar:** y 0–72. **Title zone:** y 96–236. **Board area:** y 256–988 (732px high). **Footer:** from y 1012.
- Side margins 64. Panel gap 24. Panel padding 24. Twelve columns of about 127px with 24px gutters.
- **Panel:** `--color-surface`, radius 16, 1px `--color-divider` border. The hero panel of a board (the one that answers the title) is radius 24 and the largest.
- **Label tab:** a pill 36px high straddling the panel's top edge, 24px from its left. Fill `--color-surface-muted`, 1px divider border, an icon (20px) then the label in Inter 600 16 uppercase, +0.06em, `--color-text-primary`. Never red.
- **Hairlines** are 1px `--color-divider`. No drop shadows on dark pages. Elevation is a step in surface tone.
- **Scaling.** Sizes quoted for a picture in the board specs are targets for a full-page graphic. In a board, fit every picture to its panel, scaling everything in proportion, and never let text go below 16px (14px for table headers).

### Layout system: the fix for messy boards (binding, overrides any board spec that conflicts)

A previous build of this deck came out messy: panels half empty, labels on top of each other, tangled lines, tables that did not line up, pictures too small to read. The rules below exist to prevent each of those. Target look: **clean, concise, slightly packed**, like the Netflix, CertiNet and Bloom boards: every panel full of useful structure, nothing floating, nothing touching.

**L1 · Fixed panel maps.** Every board uses one of these maps inside the board area (x 64–1856, y 256–988). Panels snap to it; no free-floating pictures. Gap 24 everywhere.

| Map | Layout | Used by |
|---|---|---|
| M-A | One hero panel, full width 1792 × 732 | none by default; only if a board has one picture |
| M-B | Hero 1096 wide (left) + two stacked panels 672 wide (right), each 354 high | 02, 05, 10 |
| M-C | Three equal columns 581 wide × 732 | 03, 08 |
| M-D | Top row: hero 1792 × 440. Bottom row: three panels 581 × 268 | 04, 07, 09 |
| M-E | Left hero 1180 wide + right column 588 wide of two stacked panels 354 high, plus a full-width decision band 1792 × 156 at the bottom (hero and stack shrink to 552 high) | 06 |
| M-F | Four equal panels 884 × 354 (2 × 2) | 11, 12 |

Pick the map named for the board. If a board's spec lists more panels than the map has, merge panels or move one to the appendix. Never invent a new map.

**L2 · Panels are filled, not floating.**
- A picture fills 100% of its panel's inner width and at least 75% of the inner height. Scale the picture up, do not centre a small one in a big box.
- Inner padding 24, label tab straddling the top edge, one caption line (16px) pinned to the panel's bottom-left. Title of the panel is the tab; do not add another heading.
- After rendering, each panel's content bounding box must cover at least 75% of the panel's inner area (check in section 8).

**L3 · Alignment grid inside panels.**
- Everything snaps to an 8px grid. Text is left-aligned. Numbers are right-aligned and tabular.
- In any table or matrix, the row height is fixed (44px for one-line rows, 64px for two-line rows). Icons are 24px and sit in a fixed 40px first column, vertically centred with the text baseline. Header row 40px.
- Bars in a bar chart share one baseline, one bar thickness (28px) and one gap (16px). Bar value labels sit 12px past the bar end, never inside a bar unless the bar is longer than 200px.
- Every column of tiles or cards has identical width and identical height. No two neighbouring elements differ by less than 8px in size or offset: they are either the same or clearly different.

**L4 · Label placement (no overlaps, ever).**
- Labels go in a reserved gutter, not on top of the marks: left of the bars, right of the lines, below the axis. Leader lines are 1px hairlines, straight or a single right-angle, max 48px.
- Scatter and matrix points: place a numbered 32px circle on the point and put the name in a legend list beside the chart, one row per point (ID · name · value). The circle holds only the number. This replaces on-chart text labels for board 07's severity matrix.
- Never rotate text. Never wrap a label to more than two lines. If two labels would be closer than 8px, shorten one or move it to the gutter.
- Collision check is mandatory (section 8, check 15).

**L5 · Recipes for the pictures that went wrong.**

| Picture | Recipe |
|---|---|
| Severity × RICE view (board 07) | Not a free scatter. A ranked **priority stack**: rows sorted by tier then RICE, 44px each. Columns: rank · numbered circle · feature name · a horizontal RICE bar from zero (max width 260) · Tier 0 badge (amber, with icon) where it applies. A thin amber divider line separates Tier 0 rows from the rest, with its label in the gutter. The red is the single top-ranked bar. |
| Claim map (boards 03, 05) | A 6-row table, not a network. Rows are the six claims in fixed order (icon, name). Columns: layer (chip), who owns the fact, how it may be stated. Cells are chips or one short phrase. No connector lines between rows. |
| Timeline / Gantt (board 09) | Two swim lanes (Engineer 1, Engineer 2) × ten day columns of 64px each on an 8px grid. Task blocks are 48px high rounded bars snapped to whole-day columns, label inside the bar (16px, max 22 characters, else the ticket ID only and the full name in the caption list). Gate 1 is one diamond on the day line with its label in the gutter above. Dependencies: at most three 1.5px arrows, each drawn as a single elbow, never crossing a block. |
| Flow / two nets (board 08) | Horizontal chain of equal-size nodes (min 200 × 88) with 56px arrows between. Second net drawn as a second row directly below, same node size, same x positions. No diagonal lines. |
| Journey (board 04) | Eight equal stage cells in one row, each 200 wide: stage number, screen thumbnail (kit SVG, 96 wide), one line of text. Below, two lanes only ("made" hollow dot, "found" filled dot) on a shared axis; the gap between them is a horizontal bracket labelled with the lag. |
| Rated matrix (board 06) | Fixed column widths: criterion 320, then equal option columns. Row height 44. Total row 56, bold, top hairline. |
| Big-number row | Tiles equal width, number Inter 700 72, unit and one-line caption underneath, evidence tag last. |
| Phone trio (board 08) | Three phones the same height (560), same top, equal gaps, numbered callouts sit in the gutter beside each phone with 1px leader lines. Callout circles 32px. |
| A02 fix coverage | A **grouped matrix**, not lines: 14 problem rows (P1–P14) × 4 family columns (E, A, B, T). Each cell holds the chips that solve that problem in that family (V1 chips white on `--color-surface-muted`, V2 and V3 at 24% white). Row height 44, chip height 28. Copy the mapping from the "Solves" column of plan 2c. Split across two column-blocks of 7 rows if needed to fit 16px text. |
| A03 seven price fingerprints | 4 + 3 grid of equal cards 428 × 300. Each card: title, a 380 × 120 schematic (one polyline, 2px, max 8 points, one shaded band), fingerprint line, "Fixed by" chip. The seven cards plus one card holding the four extra causes fill the 4 × 2 grid exactly. |
| A08 questions | 2 × 3 grid of equal cards 581 × 340, question 600 18, answer 16 / 24, filled to 75% or more. |

**L6 · Slightly packed.** Aim for 70 to 90 words of prose per panel-row region and every panel holding structure (rows, tiles, bars, chips), not a paragraph. If a panel has empty space, add the next most useful fact from the plan (a second data point, the evidence tag, a "so what" line), not more padding. A juror should think "dense but calm", never "empty" and never "crowded".

**L7 · One visual language.** Same corner radii (16 panel, 24 hero, 12 tile, 999 pill), same 1px hairline, same icon stroke, same chip height (28), same badge style everywhere. No board may introduce a new border, shadow, gradient or corner style.

### The chapter bar

Seven tabs, each an icon (20px) and a label in Inter 600 18, in the segmented style of `kit/07_COMPONENTS/navigation/`:

`Answer` (`info`) · `Reframe` (`search`) · `Read the 50%` (`trending`) · `Principle` (`shield-check`) · `Options` (`compare`) · `Fit to 20 days` (`calendar`) · `Doubts` (`refresh`)

- Bar: `--color-surface` fill, 72px high, a hairline underneath.
- Current tab: raised surface fill, white text, a 3px white underline. Chapters already read: 72% white. Chapters ahead: 40% white.
- On boards 07 to 11 the current tab reads `Fit to 20 days · 5a Prioritise`, then `5b System`, `5c Execute`, `5d Measure`, `5e Roadmap`.
- The cover carries no bar. The closing board (12) carries it, on the stage ground. Appendix pages carry a one-tab bar reading `Appendix`.
- Each tab links to the first board of its chapter in the PDF. The bar is never red.

### Type

| Element | Font and size | Colour and rules |
|---|---|---|
| Board titles | Instrument Serif 60 / 64 | Sentence case, max two lines, max 1400px wide. The only serif on the page |
| Eyebrow | Inter 600, 16, uppercase, +0.08em | Tertiary, never red |
| Lede | Inter 24 / 34 | Secondary, max two lines |
| Panel prose | Inter 18 / 26 | Secondary, with the one to three words that carry the point set in Inter 700 white |
| Table and matrix text | Inter 16 / 22 | Header row 14, uppercase, tertiary |
| Captions and metadata | Inter 16 / 22 | Tertiary, middle dots between facts |
| Stat figures | Inter 700, tabular numerals, 48–96 | Never the serif |

Minimum text size anywhere is **16px** (14px for the chapter-bar sub-label, table headers and the tick labels of a chart axis). If something will not fit, cut a row or move it to the appendix. Never shrink type below the minimum.

### Colour has a job

**Red means now.** `--color-primary` #FF0049 appears on exactly one element per board:

- the single highlighted bar, line, dot or tile in that board's hero picture; or
- the primary button inside a mockup.

The eyebrow is **not** red (this differs from the kit's sample slides). Set eyebrows in `--color-text-tertiary`, so red stays free for the data. The chapter bar is never red.

**The other colours:**

| Colour | Token | Use it for |
|---|---|---|
| Lavender | `--color-iris` #DDBEF0 | Only things the assistant says or personalises |
| Green | `--color-success` | Verified, live or V1-shipped |
| Amber | `--color-warning` | Cached, changed, at risk, or Tier 0 |
| Orange-red | `--color-error`, always with an icon | Errors. Never use the brand red for an error |
| Everything else | White, secondary, tertiary, `rgba(255,255,255,.24)` | All other marks |

**Rated cells.** For matrices that rate options (yes, partly, no), tint the cell instead of colouring the text: `--color-success` at 16% for a yes, `--color-warning` at 16% for a partial, `rgba(255,255,255,.06)` for a no. The label inside stays white, and the cell always carries a word or an icon as well as the tint, so the meaning never depends on colour.

### Flow devices

**Hand-offs.** The last sentence of each board's speaker notes hands off to the next board. Keep it plain ("So the next question is what the 50% actually measures."). On the board, only the short `Next:` line in the footer carries it (table in section 5). Never a full sentence.

**Ghost chapter numerals.** The first board of each chapter carries the chapter number in Instrument Serif at 240px, 5% white, at the right of the title zone. It is the only large decoration on that board.

**Recurring anchors.** These repeat so the reader recognises them without re-reading:

- The six claims always appear in the same order, with the same six icons: flight price, hotel availability, visa and entry rules, refund terms, baggage, meal (boards 03, 04, 05, A04).
- The three layers keep one treatment each: Transactional, Regulatory and Fare attribute.
- The dashed "missing check" box on board 03 returns as the solid Validator on board 08.
- The phone on the cover returns, with two companions, on board 08.
- The 50.8% on board 04 returns as the `~50%` on boards 02 and 10. The `≤ 30%` target is the same figure on boards 02 and 10.
- Gate 1 (board 09) and Gate 2 (board 11) use the same diamond.

### Density rule (boards)

- A board has three to five panels. One is the hero, the largest, and it answers the title. Every panel holds one picture and at most about 45 words of prose.
- At most about 220 words of on-board prose in total, not counting picture labels, table cells, the chapter bar, eyebrow, footer and `Next:` line. Record the count in `README.md`.
- If a table has more than eight rows on a board, it belongs in the appendix, with a line on the board pointing to it ("Full table: A01").
- Leave air only where it helps: 24px between panels, and text never touches a panel edge. Panels themselves must be full (rule L2). Empty ground between panels is at most 10% of the board.
- Hierarchy carries density: title, then label tabs, then bold key terms, then detail. A juror should be able to read only the title, the tabs and the bold words, and still follow.

### Every board carries

- **Eyebrow** above the title, naming the plan section (for example `1.4 · WHY 50%`).
- **Chapter bar**, boards 02–12.
- **Footer**: a hairline, then `Prithwish Chakraborty · Glance26 AI PM case · Travel assistant accuracy` on the left, the `Next:` line in the middle (16px tertiary, with a small `arrow` icon, linked to the next board) and the page number on the right. All tertiary.
- **Evidence tag** on any assumed or illustrative number. Beside the figure, in 16px tertiary: *Assumption*, *Illustrative* or *Sizing, not forecast*.

### Infographic rules (every picture on every board)

- **Direct labels, no legends.** Label every bar, line and node at its end. The only exception is the size key on board 07.
- **One highlight per board.** That is the board's red. The other pictures on the board use white at 72% or `rgba(255,255,255,.24)`. Everything else is white at 72% or `rgba(255,255,255,.24)`.
- **No value ramps across categories.** No 3D, no pie or donut charts, no gradients inside data marks.
- **Honest axes.** Bars start at zero. If a range makes a small value invisible, say so in the caption rather than using a broken axis. A log scale is allowed when the caption says so.
- **Plain headings.** Each picture answers its panel's question, and the board's hero picture answers the title. A caption or one bold line states the one thing to notice, as a sentence.
- **Arrows.** Flows and pipelines use 1.5px hairline arrows. Missing or failing steps use a dashed outline in `--color-error` with the `alert` icon.

### Don'ts (binding)

- No Glance logo and no Glance brand assets. Write "Glance" in plain text. The kit's "wake" wordmark appears only inside the phone mockups.
- No company logos on the precedents panel. Names in text only.
- No emoji, no uppercase buttons, no text on an image without a scrim, no drop shadows on dark slides.
- No second red element on a board.
- Never present an illustrative or assumed figure as measured.

---
## 4 · Voice: write like a PM, not like a model

This deck is judged by people who read a lot of AI-generated work. It must read as one person's judgment.

**Titles are the argument.** Every title is a full sentence stating that board's conclusion. Reading only the 12 titles must tell the whole story (the list is in section 5). Use the titles given here, word for word.

**Write it like this:**

- Short declarative sentences. Concrete nouns. Numbers instead of adjectives: "₹4,764 where the airline charged ₹299", not "significantly higher fees".
- First person for decisions and doubts: "I cut Option C because…", "I don't know yet whether…". The reasoning file says "we"; change it to "I" for decisions and judgments, and keep "we" only for work the team does in execution.
- Name the trade-off every time something is chosen: what it costs, what it risks, what would change the decision.
- Say plainly what is assumed and what is not known.

**Banned words:** leverage, seamless, robust, delve, unlock, empower, holistic, synergy, cutting-edge, game-changer, revolutionise, streamline, elevate, harness, navigate (figuratively), landscape, ecosystem, journey (except the user journey slide), "in today's fast-paced world", "it's worth noting", "at the end of the day", "moreover", "furthermore".

**Banned patterns:**

- **Em dashes.** Use a full stop, comma, colon or middle dot instead.
- **"Not X, but Y" reframes.** Allowed once in the whole deck, in board 06's notes.
- **Rhetorical questions** in titles or body. Questions are allowed only as quoted jury questions in A08, as the label of a panel, and as the week-0 question on board 12.
- **Groups of three added for rhythm.**
- **Exclamation marks.**
- **A bold lead-in on every bullet.** Bold is for the one to three words that carry a point; it is never a habit.
- **Ending a slide on a slogan.** Only boards 06 and 12 carry a line meant to be quoted.

**Speaker notes** are spoken sentences, three to six per board. Write them the way you would explain it to an engineer at the next desk. Where a slide carries a decision, the notes include what would change my mind, taken from the matching decision (D1–D12) in the reasoning file. End with the hand-off to the next slide.

---

## 5 · The storyline (titles in order)

The argument, in five sentences (copy from the reasoning, "The argument in five sentences", and keep it beside you while building):

1. The assistant's errors are three problems, not one: it states prices, policies and fare details it does not own, in one confident voice, with nothing checking a claim against its source.
2. The 50% is a trip-level rate, so the weakest component, flight price, dominates it, while the costliest errors surface too late to show up in it.
3. So A and B ship as one rule: prices fetched at the moment of decision and never written by the model, policy answered only from a cited source, with a person for stranding cases.
4. C is cut because it relocates staleness into model weights, where it cannot be seen, dated or cited.
5. V1 is measured against the price the user acted on, tuned by config in a sandbox, and its telemetry decides V2.
| # | Chapter | Source section | Title |
|---|---|---|---|
| 01 | Cover | Cover | Make it check before it speaks |
| 02 | Answer | Plan on one page · Decision | One rule, shipped in four engineer-weeks, halves the error rate |
| 03 | 1 Reframe | Plan 1.1–1.3 · D1 | Four complaints are three failures, and nothing checks a claim before the user sees it |
| 04 | 2 Read the 50% | Plan 1.4 · 2a | Errors multiply, and the costliest ones are found after the number is counted |
| 05 | 3 Principle | Plan 2b · reasoning step 3 | Who owns a fact decides how the assistant may state it |
| 06 | 4 Options | Reasoning step 4 · D2–D6 · Decision | One rule, two evidence providers: A fetches, B cites, C is cut |
| 07 | 5a Prioritise | Plan 3 · D7 | Severity decides first, then RICE ranks |
| 08 | 5b System | Plan 4 · D5 · Experience | Two independent nets check every claim, so the assistant can't make up a fare |
| 09 | 5c Execute | Plan 5.1–5.3 · D8 | Two engineers, ten days, and neither waits on the other |
| 10 | 5d Measure | Plan 5.4 · D10–D11 | V1 is measured against the price the user acted on, and tuned by config |
| 11 | 5e Roadmap | Plan 5.5–5.8 · D9, D12 | Each version has to earn the next one |
| 12 | 6 Doubts | Reasoning: assumptions · plan 1.7 | What would change my mind |

**Footer `Next:` lines** (16px, in this wording):

| Board | Next line |
|---|---|
| 01 | none |
| 02 | Next: the problem, reframed |
| 03 | Next: what the 50% measures |
| 04 | Next: who owns a fact |
| 05 | Next: the three options |
| 06 | Next: fitting it to 20 days |
| 07 | Next: the V1 system |
| 08 | Next: who builds it, in what order |
| 09 | Next: how I'd know it worked |
| 10 | Next: what V1 leaves open |
| 11 | Next: what would change my mind |
| 12 | Appendix follows |

Board 02's "halves" refers to the sizing (about 50% to 25–32%). Its evidence tag *Sizing, not forecast* must sit next to that figure on the board.

If an element on a board does not serve this sequence, cut it or move it to the appendix.

---
## 6 · Board by board (main deck)

Each board gives: the chapter, the layout as panels (y positions are on the 1920 × 1080 page), what goes in each panel, the kit pieces, the one red element and the speaker notes. Where a panel says "copy", copy the plan or reasoning wording.

### 01 · Cover

**Ground:** stage + `stage-signal.svg`. Layout from `kit/13_DECK_ASSETS/title-slide.svg`. No chapter bar, no footer `Next:` line.

**Right side:** `assistant-lockscreen.svg` about 700px tall, level, inside a `mask-arch.svg` window of light with `accent-arc.svg` behind it, and a 1px divider hairline under it as a floor. `contours.svg` at 6% on the ground.

**Left side:**

- Eyebrow: `GLANCE26 · AI PRODUCT MANAGER INTERN · CASE STUDY`
- Title (Instrument Serif 104): **Make it check before it speaks**, with `highlight-underline.svg` under the word "check" (white 72%).
- Lede (Inter 30 / 42, 72% white): A travel-booking assistant quotes wrong fares, sold-out hotels and wrong visa rules. This is how I'd fix it in four engineer-weeks.
- Name line (Inter 22, 64% white): Prithwish Chakraborty · f20240470@pilani.bits-pilani.ac.in · 30/09/2026

**Red:** the lock-screen mockup's "See fare" button.

> **Notes:** The fix isn't a smarter model. It's a rule about which facts the model is allowed to state, and a way to prove the rule is working. I'll give you the answer first, on one board, and then the five steps that got me there.

### 02 · The answer on one board

**Chapter:** Answer. Eyebrow `THE ANSWER FIRST`. Title: **One rule, shipped in four engineer-weeks, halves the error rate**. Layout from `kit/13_DECK_ASSETS/summary-slide.svg`.

**Panels**

- **P1 · `THE BRIEF`** (icon `info`), y 256–336, full width. One line copied from plan 1.1: what the case asks (an AI travel-booking assistant that states wrong prices, hotel availability and visa, baggage and meal information; about 50% trip booking error; four engineer-weeks; Options A, B and C). `section-separator.svg` below it.
- **P2 · `THE RULE`** (icon `shield-check`), y 360–700, 600px wide. **Card A · hero** over `illustrations/plane.svg` with `scrim-bottom.svg`. Rule text, Inter 600 32 / 42, white: No price, availability or policy claim reaches the user without evidence from the source that owns it. **Option C is cut.**
- **P3 · `WHAT I COMMIT TO`** (icon `check`), y 360–700, 700px wide. Four content-module stat tiles in a 2 × 2 grid, `--color-surface-muted`, radius 16. Label in Inter 600 18 secondary, figure in Inter 700 tabular 48, one line under it in 16px tertiary. Copy from the reasoning, "What we commit to":

| Tile | Figure | Line under it |
|---|---|---|
| Capacity | 20 engineer-days | 2 engineers × 2 weeks · 18.5 planned, 1.5 held as buffer |
| North star | ~50% → ≤ 30% | Trip booking error rate · V2 ≤ 15% · tag *Sizing, not forecast* |
| Evidence | ≥ 99% | of price, availability and policy claims carry their evidence |
| Guardrails | +1.5 s · −5% | Time to price p90 over baseline · booking conversion drop limit |

- **P4 · `THE SIZING`** (icon `trending`), y 360–700, 444px wide. A **step-down chart**: three vertical bars from zero, `~50%` (white 72%), `≤ 30%` and `≤ 15%` (24% white), each labelled at its top, with V0, V1 and V2 beneath. The `≤ 30%` bar is the board's red. Tag *Sizing, not forecast* beside it. One bold line under the chart: **About half the errors go in V1, most of the rest in V2.**
- **P5 · `HOW I GOT HERE`** (icon `forward`), y 724–988, full width. Five numbered cells in a row joined by hairline arrows, each linking to its board in the PDF. Number in Inter 700 tabular 32, step name in Inter 600 20, one line in 16px secondary, and the board numbers in tertiary:

| # | Step | One line | Boards |
|---|---|---|---|
| 1 | Reframe the problem | "Hallucination" is three failures in three layers | 03 |
| 2 | Read the 50% | Errors multiply; the costliest ones are counted late | 04 |
| 3 | Derive the principle | Who owns a fact decides how it may be stated | 05 |
| 4 | Test the options | A and B fit the principle; C breaks it | 06 |
| 5 | Fit it to 20 days | Gate by severity, rank by RICE, cut at capacity | 07–11 |

**Red:** the `≤ 30%` bar in P4.

> **Notes:** I diagnosed before I compared options, so each option is judged against a cause, not against the other options. If you remember one board, it's this one: the rule on the left, what I commit to in the middle, and the sizing on the right, which is a sizing, not a forecast. Everything after this is the reasoning, in five steps. It starts with what the problem statement actually says.

### 03 · Four complaints are three failures, and nothing checks a claim before the user sees it

**Chapter:** 1 Reframe. Eyebrow `1.1–1.3 · WHAT THE PROBLEM STATEMENT ACTUALLY SAYS, AND HOW THE ASSISTANT WORKS`. Layout from `kit/13_DECK_ASSETS/architecture-slide.svg`. Lede: The assistant acts as the source of truth for facts it does not own, and sounds equally sure reading live data, a stale cache or its own memory.

**Panels**

- **P1 · `WHO OWNS EACH CLAIM`** (icon `search`), hero, y 256–636, full width. A **claim-ownership grid**. Rows: the six claims with their recurring icons. Columns: Who owns the truth · How fast it changes · Cost if wrong. Copy the cells from plan 1.2.
  - Group the rows under three margin labels, each with a 48px illustration cropped with `mask-pill.svg`, copied from reasoning step 1: *Transactional* (`plane.svg`; flight price, hotel availability): changes in minutes, owned by supplier inventory. *Regulatory* (`temple.svg`; visa and entry rules, refund terms): changes in days or weeks, owned by governments and airlines. *Fare attribute* (`bag.svg`; baggage allowance, in-flight meal): owned by the fare record of this exact ticket.
  - **Speed bar** in its own narrow column: filled at a width proportional to speed (minutes = full, per fare = half, weeks = a quarter), one neutral colour.
  - **Cost meter**: three pips per row, filled 1, 2 or 3 in white 72% (Low = 1, a fee or a failed booking = 2, stranding, fraud or liability = 3). Say the wording from the plan beside the pips.
  - `focus-brackets.svg` frames the Visa and entry rules row.
  - One bold line under the grid: **Three owners, three speeds, three costs. One fix cannot cover all three.**
- **P2 · `TODAY'S PIPELINE`** (icon `forward`), y 660–988, 1100px wide. The **request pipeline**, a horizontal flow of hairline boxes with 1.5px arrows: User request → Intent parsing → Router → Data path (three stacked sub-boxes: Cache · Live supplier call · Document store) → Prompt assembly → Model → Checkout.
  - Between Model and Checkout, a dashed box with the `alert` icon (amber), labelled **"Missing: check the reply against its source"**. `scan-lines.svg` at 8% behind it and `focus-brackets.svg` around it.
  - **Trace one stale fare through it**: a dotted white path from the Cache box, through Prompt assembly and Model, to Checkout, with a small fare chip that keeps the same value at every stop and the label "The same number, never checked".
  - Under each real box, a small tertiary label with the layer name.
  - One bold line: **The model sounds the same whether it read a live fare, a forty-minute-old cache or nothing at all.**
- **P3 · `WHERE EACH ONE BREAKS`** (icon `alert`), y 660–988, 668px wide. Three **Card F · editorial** rows, each with a headline, one line and the F-numbers as the source tag:
  - **Stale or wrongly keyed prices** · Data path and cache key · F-12, F-15, F-31
  - **Policy answered from memory** · Router never fires retrieval · F-04
  - **Attributes from the wrong source** · Router sends meal and bag questions to policy docs · F-05, F-25
  - Caption: *F-numbers refer to the 40 failure modes in the Travel Assistant Failure Map.*

**Red:** the dashed "missing check" box outline in P2, in `--color-primary`.

> **Notes:** "Hallucination" is one word for three failures in three layers: transactional facts, regulatory facts and fare attributes. A bigger model or a better prompt still has no live price and still has a training date. The pipeline shows why nobody notices: nothing between the model and checkout checks a claim. What would change my mind: week-0 logs showing most errors come from one layer, say the model misreading a correct supplier response. So the next question is what the 50% actually measures.

### 04 · Errors multiply, and the costliest ones are found after the number is counted

**Chapter:** 2 Read the 50%. **The only light board**: `data-theme="light"`, `light-iris.svg` at 40%, chapter bar inverted (#0C0C10 current, 48% and 24% of #0C0C10 for the others). Eyebrow `1.4 · 2A · WHY 50%, AND WHERE IT IS COUNTED`. Lede: A trip succeeds only if every component is right, and the 50% is counted at checkout, before four of the six claim types go wrong.

**Panels**

- **P1 · `THE TRIP RATE IS A PRODUCT`** (icon `trending`), y 256–536, 880px wide. **Two multiplication chains**, each four white tiles joined by `×` and `=`, figures in Inter 700 tabular 56:

| Row | Flight price | | Hotel availability | | Fees and ancillaries | | Whole trip |
|---|---|---|---|---|---|---|---|
| Today | `60%` | × | `92%` | × | `92%` | = | `50.8%` |
| If flight price is fixed | `98%` | × | `92%` | × | `92%` | = | `82.9%` |

  Caption, tertiary: *Illustrative inputs, chosen to reproduce the brief's 50%. What holds for any plausible inputs: the weakest component dominates.*
- **P2 · `WHAT FIXING ONE PART BUYS`** (icon `compare`), y 256–536, 888px wide. Four horizontal bars from zero, each labelled at its end, using the same illustrative inputs with the fixed part raised to 98%:

| Bar | Trip rate |
|---|---|
| Today | 50.8% |
| Fix hotel availability | 54.1% |
| Fix fees and ancillaries | 54.1% |
| Fix flight price | 82.9% |

  The flight-price bar is #0C0C10 at full strength; the other three are #0C0C10 at 32%. Caption: *Same illustrative inputs. Raising any single part to 98% shows where the trip rate is won.*
- **P3 · `MADE EARLY, FOUND LATE`** (icon `clock`), hero, y 560–988, full width. A **journey chart** in the manner of a day-in-the-life path.
  - Left column, 300px: the example request in a `mask-ticket.svg` card, in Inter 18: Delhi to Bangkok, 2 adults, 24–28 October, under ₹60,000, and a Jain meal for my mother. Beneath it, the six claim rows with their recurring icons.
  - Eight stage columns, 150px each, headed 1 Ask · 2 Quote · 3 Compare · 4 Pre-trip questions · 5 Checkout · 6 Prepare · 7 Travel · 8 After the trip. Above each header, a 120px **screen-template thumbnail** (see 2b), unedited `<img>`, at 64% opacity except stage 5, at full brightness. A dotted 1px path runs through the eight headers.
  - Per row, a hollow dot where the error is made, a filled dot where it is found, a hairline arrow between them and a faint band (white, 8%) over the stages in between, so the hidden period is visible. Stages from plan 2a:

| Claim | Made at | Found at |
|---|---|---|
| Flight price | 2–3 | 5 |
| Hotel | 2 | 5 |
| Entry rules | 4 | 7 |
| Baggage | 4 | 7 |
| Meal | 1 and 4 | 7 |
| Refund | 4 | 8 |

  - A vertical line at stage 5 labelled "The 50% is counted here". Arrows that cross it (the four late-surfacing claims) are white; the two that end at 5 are 24% white.
  - A **detection-lag number** at the right of each row: the found stage minus the earliest made stage, in Inter 700 tabular, with "stages" under the column head.
  - One bold line: **Four of the six claim types go wrong after the number is counted.** Full happy and unhappy paths: A10.

**Red:** the vertical line at stage 5 in P3 (it is the point of the board).

> **Notes:** The trip rate is a product, so the weakest component dominates it. Fixing flight price lifts the trip rate far more than its own share suggests, which is why it gets most of the budget. But the 50% is counted at checkout, and four of the six claim types go wrong after it. The metric over-counts price and under-counts the errors that strand people, so I steer the policy work with leading indicators, grounded claim rate and deflection, instead of waiting for outcome data that arrives weeks late. So the next question is who owns each of these facts, and what happened to others who got it wrong.

### 05 · Who owns a fact decides how the assistant may state it

**Chapter:** 3 Principle. Eyebrow `2B · WHAT HAPPENED TO OTHERS, AND THE PRINCIPLE`. Lede: Every fix that held moved the fact back to a source that could be checked. Ownership, speed of change and cost of error decide how a claim may be stated.

**Panels**

- **P1 · `WHAT HAPPENED TO OTHERS`** (icon `news`), y 256–988, 880px wide.
  - A **timeline hairline** across the top with six dots: Dec 2023, Feb 2024, May 2025, Aug 2025, Feb 2026, May 2026, each labelled by company only.
  - Six **Card C · compact** cases in a 3 × 2 grid, chronological left to right and top to bottom, so each sits under its dot. Each has a 56px illustration cropped with `mask-rounded.svg`, company and date in Inter 600 18, one line of what happened (16 / 22, secondary) and a chip with the feature it gives us. Keep the six that map to our complaints:

| Case | What happened | Chip |
|---|---|---|
| Air Canada, Feb 2024 | Invented a bereavement-refund rule; tribunal held the airline liable, about C$650 | B2 |
| ChatGPT and Puerto Rico, Aug 2025 | "No visa needed"; the couple needed an ESTA and was denied boarding | B6 |
| Booking.com and Accor in ChatGPT, Feb 2026 | Stated rates didn't match the booking card; euros for a US user | A1, A8 |
| CCPA probe, May 2026 | Agoda showed ₹4,764 where Akasa Air charged ₹299 | A6 |
| Chevrolet dealer bot, Dec 2023 | Agreed to sell a Tahoe for $1, "a legally binding offer" | A1 |
| Klarna, May 2025 | AI push "had gone too far"; human agents brought back | B4 |

  - **"What worked"**, four rows under the cards, each with `check` in success and a chip:
    - KAYAK.ai · real-time provider pricing in chat · A2
    - Booking.com AI Trip Planner · prices as cards from inventory · A1
    - Expedia Rapid Price Check · matched, changed or unavailable before booking · A3
    - IATA Timatic · the database airlines check at boarding · B5
  - A **big-number tile** (content module): `8%` of travellers comfortable booking through AI (Expedia/YouGov, 2026), Inter 700 tabular 56, with one line beside it: Trust is scarce, so each visible error costs more than one booking.
  - No logos.
- **P2 · `WHO OWNS A FACT`** (icon `shield-check`), hero, y 256–988, 888px wide.

  **Infographic: a claim map with three regions.** A 2D plot filling the top of the panel, about 888 × 500.

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

  **Under the plot: the rule, derived.** Three short lines, Inter 22 / 32, stacked with hairlines:

  - Fast facts are fetched.
  - Slow, high-stakes facts are cited.
  - Nothing high-stakes comes from model memory.

  Caption: *Fare attributes (baggage, meals) sit on the fetch side: they come from this ticket's fare record, not from policy documents.*

**Red:** the Visa and entry rules dot in P2. `dot-grid.svg` at 4% behind the plot; `focus-brackets.svg` (white 72%) around the Visa dot; a faint 1px arrow from each dot to its region's verb, so the plot reads as a sorting machine.

> **Notes:** None of the deployments that worked used a fine-tuned model as the source of truth. Every fix that held did one thing: it moved the fact back to whoever owns it. Ownership, speed of change and cost of a wrong answer give three regions on one map: fetch it, cite it, say it. This is the whole method on one board. I didn't pick the principle to suit an option; the options come next, and I test each one against it.

### 06 · One rule, two evidence providers: A fetches, B cites, C is cut

**Chapter:** 4 Options. Eyebrow `4 · THE THREE OPTIONS, AGAINST THE PRINCIPLE, AND THE DECISION`. Layout from `kit/13_DECK_ASSETS/component-slide.svg`. `highlight-underline.svg` under "One rule" in the title. Lede: A and B each fit the principle for one kind of fact, and each needs a missing piece to work. C breaks it. So the decision is one rule.

**Panels**

- **P1 · `A · B · C, TESTED AGAINST THE PRINCIPLE`** (icon `compare`), hero, y 256–748, full width. Three **Card B · standard** columns, each with an illustration on top (`plane.svg`, `temple.svg`, `iris.svg` at 40%), the option's name, a verdict badge, the scorecard, paired bars and a "needs" block.
  - Verdict badges: A "Fits · fetches fast facts" (success); B "Fits · cites slow facts" (success); C "Breaks it · memorises slow facts" (white outline with the `close` icon).
  - **Rated scorecard.** Tint each cell as a rated cell (section 3): yes = success tint with `check`, partial = warning tint with `alert`, no = neutral with `close`. Then a last row, **Fits the principle**, in Inter 700: A "for fast facts", B "for slow facts", C "no".

| | A · live price and inventory | B · cite-or-deflect for policy | C · fine-tuned policy model |
|---|---|---|---|
| Fixes the main driver (flight price) | ✓ | ✗ | ✗ |
| Fixes the stranding risk (visa) | ✗ | ✓ | ⚠ goes stale |
| Fits 20 engineer-days | ✓ | ✓ | ✗ uses all of it |
| RICE as written · confidence | 96,000 · 80% | 54,000 · 60% | 4,500 · 30% |

  - Replace the RICE row with **paired bars**: a thin bar from zero for RICE (96,000 · 54,000 · 4,500, one scale, so C's bar is nearly invisible; caption *One scale. C's bar is that short*), and below it a confidence bar from 0 to 100% (80% · 60% · 30%). All bars white 72%.
  - **"What it needs to work"**, one short block under each card, copied from the reasoning:
    - **A, rebuilt around decisions, not mentions (D4).** A live call on every mention adds 1–2 s a turn. Re-price at the decision, bind prices to an offer ID, add the supplier fallback. The split package costs 1.7 engineer-weeks and covers more mechanisms.
    - **B, plus a router rule (D6).** If a visa question is classed as chat, the gate never runs. B1 lifts B from 60% to 80% confidence for 0.3 engineer-weeks.
    - **C, nothing fixes it (D3).** It moves staleness from a cache, where it has an age, into weights, where it has none. It cannot cite a source, and fixes none of the price errors.
- **P2 · `THE DECISION`** (icon `check`), y 772–988, full width, a band on `--color-primary-subtle` #3A0716, radius 24, with `iris-aurora.svg` at 25% top right and `signal-blob.svg` at 20% behind the rule. Left, 560px: the rule in Inter 600 32 / 42, white: No price, availability or policy claim reaches the user without evidence from its source. Under it, a small **gate picture** (320px): three claim streams (a price, a policy line, a memorised answer) run right; two pass through a narrow gate labelled "evidence" and reach a "Reply" node; the third stops at the gate, marked with the `close` icon. Right: three lane cells, 380px each, separated by 12%-white hairlines, each with a label (Inter 600 22), an evidence icon, one sentence (Inter 18 / 26, 80% white) and an option badge:

| Label | Icon | Sentence | Badge |
|---|---|---|---|
| **Volatile facts are fetched** | `clock` | Prices render from a live offer at the moment the user decides. | "Option A, rebuilt as A1–A6" |
| **Regulatory facts are cited** | `passport` | Policy answers quote a retrieved official snippet, or hand off to the page and a person. | "Option B, plus the router rule that makes it fire" |
| **Nothing is memorised** | `close` | Option C is cut. | "Cut" |

**Red:** the "Cut" badge in P2, outlined in `--color-primary`. Nothing else on the board is red.

> **Notes:** A alone leaves the stranding risk open, and that harm is irreversible. B alone leaves the 50% untouched. C would move staleness from a cache, where it has an age, into weights, where it has none, so it cannot be cited or dated. The answer isn't A, B or C. It's the rule, and A and B are the two ways the rule gets its evidence. What would change my mind: if A's core needed more than about 14 days, B would shrink to B1, B2 and B4. Now the rule has to fit in 20 engineer-days.

### 07 · Severity decides first, then RICE ranks

**Chapter:** 5 Fit to 20 days · 5a Prioritise. Eyebrow `3 · PRIORITISATION`. Lede: RICE measures expected value, so it can't see irreversibility. Many ₹500 gaps would outscore one stranded traveller.

**Panels**

- **P1 · `WHICH FEATURE, AND WHY`** (icon `filter`), hero, y 256–988, 1100px wide. `dot-grid.svg` at 4% behind the plot. **A severity × effort selection matrix.** It shows why each feature was picked, not just its score. Every feature from plan section 3 is one dot.

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

  **Two annotations** (16px tertiary, with a 1px leader line):

  - **On A9:** "Fits a lane, but flights drive the 50%. Hotels lead V2."
  - **On A6,** which sits low but carries a Tier 0 ring: "Tier 0 by legal exposure (drip pricing), so it jumps the queue."

  **How to read it** (one line under the chart, Inter 18, secondary): The top-left quadrant ships first. The bottom-left ships in RICE order until the 20 days run out. Everything on the right waits for data, a contract, or V2.

  Caption: *Effort is on a log scale. Severity is the RICE impact score. RICE = reach × impact × confidence ÷ effort. Reach uses the plan's assumptions: 100,000 trip sessions a month reach a quote. Full table: A01.* Put the tag *Assumption* beside it.
- **P2 · `THE GATE`** (icon `lock`), y 256–476, 668px wide. **Card E · recommendation**: the recommendation with its reason. Tier 0 = prevents an irreversible harm (stranding, denied boarding, fraud) or a legal exposure (drip pricing). **V1 takes every Tier 0 feature that needs no outside contract, then the highest RICE until 20 engineer-days run out.**
- **P3 · `WHAT V1 TAKES`** (icon `grid`), y 500–988, 668px wide. A **priority stack** of three cards, each with a badge, feature chips and one reason line:
  - **P1 · Tier 0, no contract.** A6, B1, B2, B4. They prevent stranding or money lost, or legal exposure, and need nothing from outside.
  - **P2 · Highest RICE until capacity.** A4, A1, A2, A3, A5. A5 rides with A2, because A2 can't ship without it.
  - **P3 · Held.** A8 and B3 are the buffer and stamp; A9, A7, T1, B5, B6, B7 are V2, some waiting on a data contract; T2, T3, A10 are V3. Option C is cut.

**Red:** the Option C dot in P1, filled `--color-primary`, labelled "C · 4,500 · cut: 30% confidence, the whole budget". It is the lone dot at the far right.

> **Notes:** Severity first is a value judgement, and I'm naming it as one. RICE is right about expected value and blind to irreversibility, so I use it for the first and a gate for the second. The stack on the right is the outcome: Tier 0 without a contract goes first, then the highest RICE, and the rest waits. Two Tier 0 items wait for V2 on purpose, because the visa feed needs a data contract with lead time. So what does the V1 system look like?

### 08 · Two independent nets check every claim, so the assistant can't make up a fare

**Chapter:** 5 Fit to 20 days · 5b System. Eyebrow `4 · ARCHITECTURE · EXPERIENCE`. Layout from `kit/13_DECK_ASSETS/interaction-model-slide.svg` and `card-anatomy-slide.svg`. Lede: V1 closes 14 of 40 failure modes and narrows 13 more. The options as written fully covered 8.

**Panels**

- **P1 · `THE V1 EVIDENCE PATH`** (icon `shield-check`), hero, y 256–596, full width. A flow of hairline boxes, radius 12: User asks → **Router** (claim type, the first net) → three evidence sources, stacked (Live offer record · Retrieved official snippet · None needed, for travel concepts) → **Validator** (scans every reply for prices, dates and policy terms, whatever the router said; the second net) → a **fan of four output widgets**, each about 240px wide, offset like a stack, each joined by a hairline to the evidence source that produced it:
  - *Fetched*: the live **fare card** (Card D) with `live-signal.svg`.
  - *Cited*: the cited policy answer.
  - *Re-validated at checkout*: the "Fare changed since you looked" bottom sheet from `overlays/`.
  - *Handed off*: the deflect card.
  - `iris-sparkle.svg` in lavender marks the assistant's text on each. A second, curved hairline runs from the Router straight to the Validator, labelled "general chat still passes the validator". The Validator carries a 6px white dot labelled "second net".
  - Two short notes under the flow (Inter 16): **The model never writes a price (D5).** Every figure renders from an offer record; the validator strips any currency figure in the model's text that has no offer ID. **The weak point is named.** The claim classifier is a single point of failure, which is why the validator runs independently of the router. Caption: *Freshness budget per claim type: A04.*
- **P2 · `WHAT THE USER SEES`** (icon `chat`), y 620–988, 1200px wide. **Three phones side by side**, each about 330px tall, `iris-night.svg` at 30% behind the assistant phone: `assistant-lockscreen.svg` (a live fare on the lock screen, with the time it was checked), `assistant-chat.svg` (the fare card renders from the API; the model never types the number; add the **chat input bar** from `inputs/` beneath it), `assistant-policy.svg` (rules cite a source and last-verified date, or hand off to a person). If it reads at 16px or more, place `travel-assistant-flow.svg` as a thin strip under the phones. Put **numbered callouts** (small white circles, 1 to 4) at the exact spots on the phones, measured from the SVGs: 1 the offer ID chip on the fare card, 2 the "Live · checked 9:41" line, 3 the source row of the policy answer, 4 the human-handoff button.
- **P3 · `FOUR RULES`** (icon `lock`), y 620–988, 568px wide. The same numbers 1 to 4, each with an icon and one sentence:
  - 1 · `shield-check` · Every price is bound to an offer ID.
  - 2 · `clock` · Every price says when it was checked: "Live · checked 9:41" in green, "Cached 9:32" in amber.
  - 3 · `passport` · Every rule shows its source and last-verified date.
  - 4 · `chat` · No source, no answer. Visa and airport cases get a person.
  - Foot line (Inter 18, secondary): Glance users are mostly on mobile, in short sessions. A "Checking live fares…" state covers the 1–2 s supplier call instead of a blank screen.

**Red:** inside the mockups only (the fare card's and lock screen's primary button). Every other mark on the board is white, green, amber or lavender.

> **Notes:** Models restate, round and total numbers; the $1 Tahoe and the Accor mismatch both came from model-written prices. So there are two independent nets: the router decides where the evidence comes from, and the validator checks every reply whatever the router said. What would change my mind: the validator blocking honest replies at a rising rate. Then I fix patterns; I don't remove the rule. On the phones, live calls fire only at decisions, identical calls share one request, and time to price has a hard limit of baseline plus 1.5 seconds. That's my answer to the latency worry. Next: who builds this, in what order.

### 09 · Two engineers, ten days, and neither waits on the other

**Chapter:** 5 Fit to 20 days · 5c Execute. Eyebrow `5.1–5.3 · EXECUTION`. Lede: 18.5 of 20 engineer-days planned, 1.5 held back until week-one data says where they're needed.

**Panels**

- **P1 · `CAPACITY`** (icon `calendar`), y 256–340, full width. One horizontal bar from zero to 20 engineer-days, 1200px wide, split into Engineer 1 (9.5), Engineer 2 (9) and Buffer (1.5), each labelled at its start. Engineer bars white 72% and 48%; the buffer hollow with a dashed ring. It answers "how much is planned" before the Gantt does.
- **P2 · `THE TEN DAYS`** (icon `clock`), hero, y 364–794, full width.

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
  - Feature IDs are chips inside the bars. `focus-brackets.svg` frames the Gate 1 diamond. The milestone diamond is the same shape as Gate 2 on board 11.
- **P3 · `BUFFER RULE · DAY 7`** (icon `refresh`), y 818–988, 884px wide. Price gaps track party size or currency → A8. Hotels above 25% of trip errors → start A9. Otherwise, harden the validator.
- **P4 · `CUT LINE · DAY 6`** (icon `alert`), y 818–988, 884px wide. If behind, drop B3's stamp first, then the buffer item. Never drop A5 (A2 can't ship without it) or B4 (the stranding path).

**Red:** the Gate 1 diamond in P2.

> **Notes:** "4 engineer workweeks" together with "2 weeks" under Option C reads as two engineers. Every dependency stays inside one lane, so neither waits. The cut line is decided in advance, so a slip on day 6 is a rule, not a debate. What would change my mind: a different team shape from the eng lead in week 0. I'd keep the rule and re-cut at the same cut line. Then, how do we know it worked?

### 10 · V1 is measured against the price the user acted on, and tuned by config

**Chapter:** 5 Fit to 20 days · 5d Measure. Eyebrow `5.4 · THE V1 SANDBOX`. Layout logic from `kit/12_UI_EXAMPLES/dashboard.svg`. Lede: The metric compares the payment price with the price the user acted on, and V1 exposes its trade-offs as knobs, so improving it means turning a knob and reading the result.

**Panels**

- **P1 · `NORTH STAR`** (icon `trending`), hero, y 256–556, 700px wide. A content-module stat tile, radius 24. **Trip booking error rate**, measured against the decision price (the total on the card when the user tapped Book). Three figures in Inter 700 tabular 72: `~50%` today → `≤ 30%` after V1 → `≤ 15%` after V2. Tag: *Sizing: 25–32% after V1, about 11% after V2. Sizing, not forecast.*
- **P2 · `THREE DRIVERS`** (icon `compare`), y 256–556, 1068px wide. Three **bullet-chart** tiles, one per driver, joined by hairlines to P1. Each is a track from 0 to 100%, a hollow marker for the baseline and a solid marker for the target. Direct labels only.

| Driver | Baseline → target |
|---|---|
| Decision-price accuracy, flights | ~60% → ≥ 85% |
| Grounded claim rate | measured in week 1 → ≥ 99% |
| Policy deflection rate | 0% → a 10–30% band. Caption: "a band, not a ceiling: a gate that deflects everything scores 100% grounded" |

  Grounded claim rate has no baseline yet, so draw its baseline as a dashed marker with no position, labelled "week 1". The deflection band is a shaded stretch from 10% to 30%, labelled "the band".
- **P3 · `THE KNOBS`** (icon `settings`), y 580–800, 1100px wide. Four slider tracks (slider styling from `kit/07_COMPONENTS/inputs/`), each with its range, a marker at the start value and the trade-off in 16px tertiary underneath:

| Knob | Start | Range |
|---|---|---|
| K1 re-price window | 10 min | 0–30 min |
| K2 supplier timeout | 1.5 s | 0.8–3 s |
| K3 fallback age | 30 min | 0–60 min |
| K6 entry-rule freshness | 7 days | 1–14 days |
- **P4 · `GUARDRAILS`** (icon `lock`), y 580–800, 668px wide. Two tiles with 24% white borders: Time to price (p90) ≤ baseline + 1.5 s. Assistant booking conversion: no drop beyond 5%.
- **P5 · `WHAT I READ EACH WEEK`** (icon `info`), y 824–988, full width. Five health checks as chips with a `check` icon: unwarned change rate ≈ 0 · fallback < 5% · live checks per booking inside the supplier allowance · validator block rate stable · handoff wait within target. Caption: *KPI definitions and the "if this happens, do this" rules: A05.*

**Red:** the `≤ 30%` figure in P1.

> **Notes:** The metric compares the payment price with the decision price, not the last price shown. Otherwise the disclosure feature would make every checkout match and the number would look fixed when users still paid more than they chose. Complaints are read alongside, never used as a target, and deflection is a band, because a gate that deflects everything scores 100% grounded. Last step: what V1 leaves open.

### 11 · Each version has to earn the next one

**Chapter:** 5 Fit to 20 days · 5e Roadmap. Eyebrow `5.5–5.8 · ROADMAP`. Lede: V1 ships in four engineer-weeks. What it leaves open is named, and V1's own data chooses what comes next.

**Panels**

- **P1 · `ROADMAP`** (icon `calendar`), hero, y 256–598, full width. A **tab bar** V1 · V1.1 · V2 · V3 across the top of the panel (`tabs/`), V1 active. Below it, a **phase table** in the manner of a strong case deck: columns are the phases, rows are Timeline, Primary goal and Key activities (feature IDs as chips, at most 12 words per cell). Between V1 and V1.1, the Gate 2 diamond. Width follows duration where the plan gives one (V1 four weeks; V2 next four engineer-weeks) and is equal otherwise; if the rail is not to scale, the caption says so. Copy the content from plan 5.5–5.8:

| Phase | Content |
|---|---|
| **V1** (weeks 1–4) | build, shadow 2–3 days, then 10% · 50% · 100% of users, split by user |
| **Gate 2** | 7 days at 100% · error rate ≤ 30% · grounded ≥ 99% · deflection 10–30% · guardrails hold |
| **V1.1** | tuning only, no new features |
| **V2** (next 4 engineer-weeks, target ≤ 15%) | A9 hotels · B5 + B6 entry-rules feed and checklist · T1 baggage and meals · B3 change detection · B7 contacts. The lead item switches on V1's data |
| **V3** | A10 holds · T2 constraints in code · T3 post-booking alerts · a confirmation gate before any agentic booking, nothing pre-selected |
- **P2 · `KNOWINGLY NOT IN V1`** (icon `alert`), y 622–988, 1100px wide. The pitfall-and-mitigation pair, drawn as a **carousel** (`carousels/`) of four cards, a fifth peeking at the right edge, with pagination dots. Each card names the gap (D9) and its V1 mitigation:
  - Hotel live availability · shown with its time, "confirmed at booking"
  - Fare jumps before payment · disclosed before the payment page
  - Meal and baggage answers · deflected to the fare details
  - Authoritative visa feed · cite-or-deflect plus human handoff
- **P3 · `WHAT I TRADED AWAY`** (icon `refresh`), y 622–988, 668px wide. A trade-off box with three rows, each "I chose … over …, and it costs …". Take D3 (cut Option C), D7 (severity before RICE) and D9 (known gaps in V1) from the reasoning's decision log, copy "Chose" and "Rejected" and shorten each to one line, changing "we" to "I".

**Red:** the Gate 2 diamond in P1.

> **Notes:** Naming what V1 still gets wrong is deliberate; a plan that claims to fix everything hasn't looked closely. Seven mechanisms produce "wrong price", and telemetry fingerprints which one dominates, so V2's first item is chosen by data (A03). Option C comes back only as a phrasing layer over retrieved text, never as a source. What have I assumed to get here, and what would I do if I'm wrong?

### 12 · What would change my mind

**Chapter:** 6 Doubts. **Ground:** stage + `stage-signal.svg`, `contours.svg` at 6%. Layout from `kit/13_DECK_ASSETS/closing-slide.svg`. Eyebrow `THE ASSUMPTIONS, AND THE FIRST QUESTION`. `highlight-underline.svg` under "mind" in the title (white 72%). Lede (Inter 24 / 34, 85% white): The rule survives every assumption below. Only the order of work changes.

**Panels**

- **P1 · `WHAT I ASSUMED, AND WHAT I'D DO IF WRONG`** (icon `refresh`), hero, y 256–800, 1100px wide. A **hypothesis-and-validation table**: copy the full six-row assumptions table from the reasoning (Assumption · Value used · Checked by · If wrong, I…), each row tagged *Assumption*. Header row 14 uppercase; cells Inter 16 / 22. The four with the biggest effect are set in white, the other two in 72% white:

| Assumption | If wrong, I… |
|---|---|
| Team is 2 engineers × 2 weeks | Keep the rule; re-cut V1 at the same cut line |
| Price errors come mostly from aged or restated quotes | Spend the buffer on A8, or pull A7 or A10 into V2 first |
| Hotels are under 25% of trip errors | Start A9 in the buffer and lead V2 with it |
| A policy document store exists | Build a minimal index of official pages first; B2 deflects more at the start |

- **P2 · `THE FIRST QUESTION FOR DAY ONE`** (icon `search`), y 256–800, 668px wide. In Inter 600 28, white: **What changed 4–6 weeks ago?** Then, in Inter 18 / 26 secondary: A model or prompt change, a cache TTL change, a new supplier, traffic past rate limits or seasonal demand each points to a different first fix. Under it, the five week-0 questions copied from plan 1.7, as a numbered list in 16 / 22.
- **P3 · closing line** (no tab), y 824–988, full width. Instrument Serif italic 44, white: Volatile facts are fetched. Regulatory facts are cited. Nothing is memorised. Contact (Inter 20, 64% white): Prithwish Chakraborty · f20240470@pilani.bits-pilani.ac.in. `section-separator.svg` above it.

**Red:** `kit/11_SVG_ASSETS/decorative/live-signal.svg` at 64px, bottom right.

> **Notes:** Every assumption is checked in week 0 or week 1, and each has a stated response. None of them reopens Option C. Happy to take questions; the appendix has the full tables, the decision log and the questions I expect.

---
## 7 · Appendix (backup, shown only when asked)

The divider `A00` comes first. Appendix pages use the content ground, carry no chapter bar, keep the footer (with a "Back to board NN" link in place of `Next:`), and may be denser than the main deck (tables down to 16px), but still one topic per page. Each gets a title that states its point.
| Page | Title | Content |
|---|---|---|
| **A01** | How the ranking was scored | Full RICE table, all rows from plan section 3, including the options as written. A method strip on top with the impact, confidence, effort and Tier 0 scales, copied from the plan. |
| **A02** | Twenty-two fixes for fourteen problems | Problem → feature coverage map. Left: P1–P14 (copy from plan 2b "The problem list"). Right: four families as chip stacks, E · Measure (E1, E2), A · Prices and availability (A1–A10), B · Policy (B1–B7), T · Fare attributes and the trip (T1–T3). Draw it as the grouped matrix in L5 (problem rows × family columns, chips in the cells), no connecting lines; copy the mapping from the "Solves" column of plan 2c, do not guess. V1 chips white on `--color-surface-muted`; V2 and V3 at 24% white. Red: the B1 chip in P5's row. |
| **A03** | Seven ways a price goes wrong, each with its own fingerprint | Seven small-multiple schematic charts, 4 + 3 grid, one per mechanism (quote aged, fee-shaped gap, fare bucket closed, wrong cache key, model-restated number, partial supplier results, demand spike), each with its fingerprint and "Fixed by" chip, from plan 1.5. Caption: *Schematic shapes, not data.* Right column: the four causes the brief doesn't name, from plan 1.6. Red: the "quote aged" line. |
| **A04** | Every claim has a freshness budget | Six vertical cards, each headed by its recurring claim icon and an illustration (`plane`, `hotel`, `temple`, `bag`, `food`, `city`), one per claim type: evidence required, budget at V1 start as a stat, and "if missing or too old" in amber. Copy from plan 4, "Freshness budget per claim type". |
| **A05** | Every metric is computed from what users see and do | KPI definitions table from the plan, the health checks (unwarned change rate ≈ 0 · fallback < 5% · live checks per booking inside supplier allowance · validator block rate stable · handoff wait within target), and the "if this happens → do this" table from plan 5.4. Note: price tolerance ₹100 or 1%, whichever is larger, to agree with finance. |
| **A06** | 39 tickets, TRV-10 to TRV-48 | The four epics (TRV-1 to TRV-4) with done-when criteria. The sprint rhythm on one line: Sprint 1 Days 1–5 (20 of 20 points) · Sprint 2 Days 6–10 (17 + 3 buffer) · Sprint 3 weeks 3–4, sandbox, no points. |
| **A07** | Twelve decisions, and what would reverse each | Decision log D1–D12 as one table (Inter 16 / 22): Decision · Chose · Rejected · What would change my mind. Copy from the reasoning, shortening each cell to one line. Change "we" to "I". |
| **A08** | Questions I expect | Six jury questions from the reasoning, each as the question in Inter 600 18 and a two-sentence answer in 16 / 24 secondary, in a 2 × 3 grid: "Why spend any budget on visas?" · "Aren't you ignoring your own RICE?" · "Why not C?" · "Won't deflection lose users?" · "Doesn't A's latency lose bookings?" · "If you had only one week?" Put the other five questions and full answers in this page's speaker notes. |
| **A09** | Forty failure modes, and what V1 does to each | An 8 × 5 grid of the plan's failure modes F-01 to F-40, each cell a tile with its ID and a short name. Colour by status, copied from the plan's failure map: closed by V1 (white), narrowed (48% white), left open or in V2 and V3 (hollow). Beside it, a two-bar comparison from zero: options as written fully cover 8, V1 closes 14. Copy the exact counts and statuses from the plan; if they differ from 14 and 13, use the plan's. Red: the figure `14`. |
| **A10** | Two paths through the same trip | Plan 2a as a picture. Eight stage columns with the screen-template thumbnails from board 04. Row 1, the happy path: what the user sees at each stage, one short line. Row 2, the unhappy path: where each error is made (hollow dot) and found (filled dot). The example request in a `mask-ticket.svg` card at the left. Red: the entry-rules error found at stage 7. |
| **A11** | Sources | The plan's source list, titles only, 16px, in two columns. |

The six-row assumptions table that used to sit in the appendix now lives on board 12, and the five week-0 questions with it.

---

## 8 · Final checks before rendering

1. **Numbers copied, not computed.** Every figure matches `ref/Full plan.pdf` or the reasoning file. Check that 60% × 92% × 92% = 50.8%, 98% × 92% × 92% = 82.9%, 60% × 98% × 92% = 54.1% and 60% × 92% × 98% = 54.1% still multiply, but do not change the inputs.
2. **Every assumption is tagged.** Every volume, share, target and sizing carries its tag.
3. **Titles tell the story.** Read the 12 titles alone. They must match section 5 exactly, and read as one argument.
4. **The flow holds.** The chapter bar shows the right chapter (and sub-label on boards 07 to 11). The `Next:` lines match the table in section 5. Board 02's agenda board numbers match the deck. Every set of speaker notes ends with a hand-off to the next board.
5. **Density.** Every board has three to five panels, one picture per panel, at most about 220 words of prose outside picture labels and tables, and visible empty ground (at least 8%). Run a Playwright check that no text node overflows its panel (`scrollWidth <= clientWidth` and `scrollHeight <= clientHeight` on every `.panel`) and that no computed font size is under 16px (14px only in table headers, the chapter-bar sub-label and axis ticks). Record word counts in the README.
6. **One red per board.** Fill the README table. Any board with two, remove one.
7. **Colour and kit discipline.** Lavender only on assistant output. No logos. "Glance" in plain text. Every colour is a token; every icon comes from the sprite; every illustration, mask, pattern and phone screen comes from `kit/`; no photos of people; no fonts beyond Inter and Instrument Serif.
8. **Type.** No serif outside titles, the ghost numeral and the closing line. Stats in Inter 700 tabular.
9. **Voice.**
   - Search all board text and notes for the banned words and for "—". There must be zero hits.
   - Count "not X, but Y" constructions. There must be at most one, in board 06's notes.
   - Decisions are in the first person.
10. **Kit coverage.** The README kit table lists every row of section 2b with its board. Grep `deck.html` for each component and asset path to confirm it is really referenced: `card-a` to `card-f`, `assistant-cards`, `badges`, `chips`, `tabs`, `carousels`, `overlays`, `inputs`, `navigation`, `content-modules`, `media-modules`, `iris-aurora`, `light-iris`, `dot-grid`, `contours`, `scan-lines`, `section-separator`, `focus-brackets`, `highlight-underline`, `accent-arc`, `signal-blob`, `iris-sparkle`, `mask-ticket`, `mask-pill`, `mask-arch`, `mask-rounded`, `live-signal`, `iris-night`. Any miss is either fixed or explained in the README.
11. **PDF checks.** `deck.pdf` has 24 pages, a bookmark tree (seven chapters plus Appendix), working internal links (extract the link annotations and click-test the chapter bar, agenda, `Next:` and "Full table" links), embedded fonts, selectable text and a size under 20 MB. `deck-notes.pdf` matches the board order and page numbers.
12. **Flow read.** Read only the 12 titles, the label tabs and the `Next:` lines in order. They must tell the story without the panel bodies. Then flip through the PNGs at speed: the recurring anchors (section 3) must be recognisable from one board to the next.
13. **Plan coverage.** The README has a table with every section of `ref/Full plan.pdf` (1.1 to 1.7, 2a, 2b, 2c, 3, 4, 5.1 to 5.8) and the board or appendix page that carries it. No section may be blank.
14. **Visual review.** Render and look at every PNG at 50% zoom next to `kit/13_DECK_ASSETS/png/` and, if `ref/inspiration/` exists, next to those decks. A board should be as well organised as they are and as finished as the kit. Then look at the three densest boards (04, 07, 10) at 100%: nothing may collide, clip or float free of its panel. Fix anything that looks like a different system or looks crowded.
15. **Automated layout QA (mandatory, run before delivering; fix and re-run until clean).** Write `qa.mjs` (Playwright) that opens each `slides/*.html` at 1920 × 1080 and fails on any of these, printing the page, selector and numbers:
    - **Overlap:** any two text elements, or a text element and a mark that is not its own label, whose bounding boxes intersect (use `getBoundingClientRect` on every `text`, `tspan`, `.label`, `.chip`, `.badge`, `td`, `th` and SVG `text`; allow parent/child containment only).
    - **Overflow:** any element extending beyond its `.panel` (with 24px padding) or beyond the page; any `scrollWidth > clientWidth` or `scrollHeight > clientHeight`; any SVG text whose box leaves its SVG.
    - **Empty panel:** a panel whose union of child bounding boxes covers less than 75% of its inner area.
    - **Misalignment:** in each table or matrix, cells of one column with different left edges (for text) or right edges (for numbers) by more than 1px; rows with heights differing from the fixed row height.
    - **Small text:** any computed font size under 16px (14px only in table headers, the chapter-bar sub-label and axis ticks).
    - **Second red:** more than one element with the brand red fill or stroke on a board.
    Save the report as `qa-report.txt` and paste a clean summary into `README.md`. A board is not done until the report shows zero failures for it.
16. **Look at every PNG.** After the QA passes, view each of the 24 PNGs yourself. For each board write one line in `README.md`: "clean", or what you fixed. Compare against `kit/13_DECK_ASSETS/png/` and the inspiration decks: aligned edges, equal gaps, filled panels, readable at 50% zoom. If a picture is tangled or hard to read at 50% zoom, redraw it using its recipe in L5 instead of tweaking it.
