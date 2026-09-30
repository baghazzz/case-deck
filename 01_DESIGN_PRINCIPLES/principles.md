# Design principles

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation

Ten principles, validated against the source log. Each lists its evidence and confidence.

## 01 · Wake-first ●

**Every surface must deliver its value in the first two seconds, before a tap and ideally before unlock.**

- **Why it exists:** Glance's origin is the lock screen: content that reaches people 'before they unlock the phone', with one-click engagement. Sessions are glances, not visits.
- **What it looks like:** A full-bleed image, one headline of at most two lines, one metadata line, one action. No navigation chrome.
- **What it means for interaction:** The first interaction is a tap or a swipe to the next story, never a menu. Deep interaction starts only after the user opts in.
- **Do:** Write headlines that stand alone. Put the answer, not the teaser, in the hook.
- **Don't:** Don't require a tap to understand what a story is about. Don't put two competing CTAs on a hook.
- **Example:** Lock-screen story: 'Monsoon's over. Six beaches worth a long weekend' + Explore.
- **Evidence:** InMobi's Glance advertiser page (content 'before they unlock', one-click); Samsung lock-screen news coverage ('catch up in seconds').

## 02 · Media is the layout ●

**Images and video are structural elements, not decoration around text.**

- **Why it exists:** Glance's products are visual first: full-screen 'Impact' formats, AI-generated looks 'starring you', video and live formats.
- **What it looks like:** Media fills cards edge to edge; ratios are chosen by job (9:16, 4:5, 3:2, 16:9); text sits on a bottom scrim.
- **What it means for interaction:** Media is the shared element in transitions: the card's image grows into the detail hero.
- **Do:** Crop for a focal point in the upper-middle third. Use a scrim under every overlaid word.
- **Don't:** Don't box media inside padded cards. Don't use stock imagery that could belong to any app.
- **Example:** Hero card A: 4:5 image, scrim-bottom, headline-media on top.
- **Evidence:** Glance ad formats (full-screen imagery, video); Glance AI looks and wallpapers; TechCrunch/Android Central launch coverage.

## 03 · One hook, one action ◐

**A surface makes one promise and offers one obvious next step.**

- **Why it exists:** The brand line is literally two verbs ('Glance it. Shop it.'). Short sessions punish choice.
- **What it looks like:** One primary button per view, in signal red. Everything else is secondary, tertiary or the card itself.
- **What it means for interaction:** The whole card is the tap target; the button is reserved for the commitment (plan, book, buy).
- **Do:** Name the action with a verb and its object: 'Plan a trip', 'Book at ₹5,842'.
- **Don't:** Don't stack primaries. Don't use red for anything that isn't the action or live.
- **Example:** Product detail: one 'Buy on Northline' button; save is an icon.
- **Evidence:** Glance homepage taglines and single 'Download The App' CTA; one-tap shopping flow in launch coverage.

## 04 · Red means now, lavender means you ○

**Colour carries meaning: signal red for action and live, iris lavender for personalisation.**

- **Why it exists:** The observed brand uses a hot red (#FF0049) with a lavender secondary (#DDBEF0) on black. Giving each a job keeps a loud palette calm.
- **What it looks like:** A dark stage, imagery doing most of the colour work, red on one element per screen, iris on reasons and AI.
- **What it means for interaction:** Iris elements are explainable: tapping an iris line opens 'why'. Red elements act.
- **Do:** Budget the red to about 0.5% of the screen. Use iris for every 'because you…' line.
- **Don't:** Don't use red for errors (use orange-red with an icon). Don't use iris decoratively.
- **Example:** Recommendation card E: iris reason chip; hero card: red Plan a trip.
- **Evidence:** Brandfetch brand registry colours for glance.com; dark homepage. The meaning mapping is a reconstruction.

## 05 · Starring you ●

**Personalisation is shown in the content itself, not described in settings.**

- **Why it exists:** Glance AI's core idea is 'you are the model on each page': looks rendered on the user's own image, feeds tuned to weather, trends and occasions.
- **What it looks like:** The user's likeness, city, weather or saved trips appear inside the hook; a single iris line names the signal.
- **What it means for interaction:** Every personalised element has three controls within one tap: more, less, why.
- **Do:** Show the personal detail that made the pick. Let people remove inferred interests.
- **Don't:** Don't claim to know identity ('Because you are…'). Don't hide the off switch.
- **Example:** Commerce feed: 'Starring you' badge; For you feed: 'Because you saved Goa'.
- **Evidence:** TechCrunch (CEO quote on fashion magazine), Android Central, Glance press release and App Store description.

## 06 · Discovery over navigation ●

**People find things by scrolling a tuned stream, not by opening menus.**

- **Why it exists:** Lock-screen news is a swipeable playlist with topical tabs starting at 'For You'; the app replaces 'manual searching and scrolling' with AI-led discovery.
- **What it looks like:** Category tabs, rails that peek, masonry discovery, a search that can hand off to an assistant.
- **What it means for interaction:** Horizontal swipe = next item in this topic; vertical scroll = next topic. Tabs switch in place.
- **Do:** Keep 'For you' first. Make every rail peek at 40% so it reads as scrollable.
- **Don't:** Don't add a hamburger menu. Don't auto-scroll rails.
- **Example:** Home: tabs → hero → reason rail → trending.
- **Evidence:** Samsung Glance news article (10 category tabs, horizontal swiping); Glance about page.

## 07 · Context is a primitive ●

**Time, place, weather and occasion are inputs to layout, not afterthoughts.**

- **Why it exists:** Glance describes feeds that shift with 'the weather around you, what's trending' and time of day (gym wear at 7am, loungewear at 7pm).
- **What it looks like:** The hero changes by time of day; utility widgets appear when their data changes; metadata carries the context ('26° forecast').
- **What it means for interaction:** Utility enters the feed only when relevant, then leaves. It never becomes permanent chrome.
- **Do:** Put context in metadata. Insert utility modules on change, not on a schedule.
- **Don't:** Don't show a weather widget on every screen. Don't hard-code a morning layout.
- **Example:** Look card: 'Saturday brunch · 26°'. Fare alert only when the saved route drops.
- **Evidence:** Glance blog (context-aware recommendations); App Store description; 9to5Google (weather shown when conditions change).

## 08 · Dense, not cluttered ○

**Carry a lot of content with strong hierarchy and few visual devices.**

- **Why it exists:** A feed with news, video, looks and products in one scroll only works if each unit is instantly legible.
- **What it looks like:** Two type families, one card grammar, one metadata style, 16px margins, no borders on media cards, no shadows on dark.
- **What it means for interaction:** Density rises as the user commits: hook → feed → detail. Never the reverse.
- **Do:** Use one metadata line with middle dots. Cap text on cards at three lines.
- **Don't:** Don't add dividers, boxes and shadows to create order; use spacing and type.
- **Example:** Trending module: five ranked compact cards, no dividers.
- **Evidence:** Reconstruction from observed feed surfaces; no public density metrics exist.

## 09 · Editorial voice ◇

**Content is written and set like a magazine: a serif hook, short sentences, specific facts.**

- **Why it exists:** The product positions itself as a fashion magazine starring the user; the tone is inspiration-led.
- **What it looks like:** Instrument Serif appears once per screen for the editorial moment; everything functional is Inter.
- **What it means for interaction:** Editorial moments are calm: no autoplay, no counters, generous leading.
- **Do:** Write specific, sentence-case headlines with numbers ('Six beaches', '₹4,120').
- **Don't:** Don't use the serif for UI, numbers or labels. Don't write clickbait teasers.
- **Example:** Editorial card F: kicker + serif headline + dek + byline.
- **Evidence:** Interpretation of the observed 'fashion magazine' positioning; the typeface choice is original.

## 10 · Show your sources ◇

**Anything that changes or has consequences shows where it came from and when.**

- **Why it exists:** Commerce and AI surfaces fail when facts are stale or invented; public reviews also show trust is fragile when users feel out of control.
- **What it looks like:** Freshness stamps ('Live · checked 9:41'), cited source rows, 'Sponsored' badges, 'Why this' explanations, delete controls for likeness.
- **What it means for interaction:** When the system can't verify, it says so and hands off; it never guesses.
- **Do:** Bind every price to its quote; cite every rule; label every ad.
- **Don't:** Don't let a model write a price. Don't bury the off switch.
- **Example:** Fare card with offer-bound price; policy card with source row; deflect card.
- **Evidence:** Original principle; motivated by public Play Store reviews about control and by the case study's hallucination problem.

## Principles considered and rejected or merged
- "High information density without clutter" → merged into **Dense, not cluttered** (08).
- "Rich media as a structural element" → **Media is the layout** (02).
- "Strong visual hierarchy" → treated as a property of every principle and of the 5-level hierarchy, not a principle on its own.
- "Contextual utility" → **Context is a primitive** (07).
