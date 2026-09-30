# Travel Assistant: Decision Reasoning

Sep 30, 2026 · @Sayantika

## The decision

We ship Options A and B together as one rule, in a 20 engineer-day V1: no price, availability or policy claim reaches the user without evidence from the source that owns it. Option C is cut.

We did not pick A or B as written. We broke each into its parts, kept the parts that fix a named cause, and added the few pieces each option needs to work: a fallback for A, a router rule for B, and telemetry for both. V1 runs in a sandbox, and V2 is chosen from what V1 measures.

| What we commit to | Number |
| --- | --- |
| Capacity | 2 engineers × 2 weeks = 20 engineer-days; 18.5 planned, 1.5 held as buffer |
| North star | Trip booking error rate, about 50% today; V1 target ≤ 30% (sizing 25–32%); V2 ≤ 15% |
| Evidence | ≥ 99% of price, availability and policy claims carry their evidence |
| Guardrails | Time to price p90 ≤ baseline + 1.5 s; assistant booking conversion drops no more than 5% |

**The line for the jury:** volatile facts are fetched, regulatory facts are cited, nothing is memorised, and every claim carries its evidence.

## How we got there

We reached the decision in five steps, and each step removed options before the next one began. The order matters: we diagnosed before we compared options, so the options were judged against causes, not against each other.

1. **Reframe the problem.** "Hallucination" is one word for three failures. The assistant acts as the source of truth for facts it does not own, and it sounds equally sure reading live data, a stale cache or its own memory.
   - Transactional facts (flight price, hotel availability) change in minutes and are owned by supplier inventory.
   - Regulatory facts (visa, baggage rules, refund terms) change in days or weeks and are owned by governments and airlines.
   - Fare attributes (meals, fare-specific baggage) are owned by the fare record of this exact ticket.
2. **Read the 50% correctly.** It is a trip-level rate, so component errors multiply. With flight price right 60% of the time and hotels and fees right 92% each, a trip succeeds 50.8% of the time. Fix flights to 98% and the trip rate rises to 82.9%. The weakest component dominates.
3. **Derive the principle.** For each claim, ask who owns the truth, how fast it changes, and what a wrong answer costs. Fast facts must be fetched; slow, high-stakes facts must be cited; nothing high-stakes may come from model memory.
4. **Test each option against the principle.** A fetches fast facts. B cites slow facts. C memorises slow facts, which is the defect we are removing.
5. **Fit it to 20 engineer-days.** Break A and B into features, gate by severity, rank by RICE, and cut at capacity. What does not fit is named, mitigated in V1 and scheduled for V2.

## Decision log

Twelve choices make up the plan. Each entry states what we chose, what we rejected, why, and the evidence that would reverse it.

### D1. Treat the complaints as three failures, not one

- **Chose:** split by who owns the truth: transactional, regulatory, fare attribute.
- **Rejected:** one "reduce hallucinations" workstream, such as a better prompt or a bigger model.
- **Why:** each failure sits in a different layer and needs a different fix. A better model still has no live price and still has a training date.
- **Would change our mind:** week-0 logs showing most errors come from one layer, such as the model misreading a correct supplier response.

### D2. Ship A and B together, not either alone

- **Chose:** A for prices and availability, B for policy, under one evidence rule.
- **Rejected:** A alone, because price drives the 50%.
- **Rejected:** B alone, because it is cheapest and the brief calls policy the highest-liability bucket.
- **Why:** A alone leaves the stranding risk open; that harm is irreversible and a legal exposure (Air Canada was held liable for its chatbot's refund answer). B alone leaves the 50% untouched. Together they fit in 20 days once each is scoped to its core.
- **Would change our mind:** if A's core needed more than about 14 days, B would shrink to B1 + B2 + B4 and B3 would wait.

### D3. Cut Option C

- **Chose:** no fine-tuned policy model in V1, V2 or V3 as a source of facts.
- **Rejected:** C now, or C as the long-term policy engine.
- **Why:** C moves staleness from a cache, where it has an age, into model weights, where it has none. Visa rules change often (Thailand's visa-free stay for Indians fell from 60 to 30 days in 2026). C also cannot cite a source, needs a refresh pipeline the brief doubts we can build, uses the whole budget, and fixes none of the price errors. RICE: 4,500, lowest of all.
- **Would change our mind:** nothing in this brief. C returns in V3 only as a phrasing layer over retrieved text, never as the source.

### D4. Rebuild A around decisions, not mentions

- **Chose:** A1 price cards bound to an offer ID, A2 re-price at the decision point, A3 checkout re-validation and disclosure, A5 supplier fallback, A6 total price with fees.
- **Rejected:** A as written, a live call on every price mention.
- **Why:** a live call on every mention adds 1–2 s per turn and multiplies supplier calls, yet the price only matters when the user shortlists, taps Book or returns. A as written also leaves the model free to restate an old number and shows no change before payment. The split package costs 1.7 engineer-weeks and covers more mechanisms.
- **Would change our mind:** shadow data showing prices drift within the 10-minute re-price window (K1) often enough to matter; then K1 tightens, which is config, not code.

### D5. The model never writes a price

- **Chose:** every figure renders from an offer record; a validator strips any currency figure in the model's text without an offer ID.
- **Rejected:** trusting the model to copy the API number correctly.
- **Why:** models restate, round and total numbers. The Chevrolet $1 Tahoe and the Booking.com and Accor mismatches inside ChatGPT both came from model-written prices.
- **Would change our mind:** the validator blocking honest replies at a rising rate; we fix patterns, we do not remove the rule.

### D6. Add a router rule to B

- **Chose:** B1, where visa, baggage, refund, meal and contact questions always trigger retrieval, backed by a keyword net; then B2 cite-or-deflect.
- **Rejected:** B as written, a gate on retrieved snippets only.
- **Why:** if a visa question is classified as chat, retrieval never fires, the gate never runs and the model answers from memory. That is the likeliest origin of the visa complaints. B1 lifts B's confidence from 60% to 80% for 0.3 engineer-weeks.
- **Would change our mind:** replay-set recall on policy questions already at 98% without B1.

### D7. Severity gates first, RICE ranks second

- **Chose:** Tier 0 items (prevent stranding, fraud or drip-pricing exposure) enter V1 whenever they need no outside contract; RICE orders the rest.
- **Rejected:** pure RICE.
- **Why:** RICE measures expected value and cannot see irreversibility. Many ₹500 gaps outscore one stranded traveller, and that ranking would be wrong.
- **Would change our mind:** nothing; this is a stated value judgement, and we name it as one.

### D8. Read capacity as 2 engineers × 2 weeks

- **Chose:** 20 engineer-days, two parallel tracks (price; policy and platform), 1.5 days of buffer assigned on day 7.
- **Rejected:** one engineer for four weeks, or all 20 days pre-allocated.
- **Why:** the brief says 4 engineer-weeks and, under C, "2 weeks", which reads as two engineers. Two independent tracks mean no one waits on the other. The buffer is spent where week-1 data points: A8 cache key if gaps track party size or currency, A9 if hotels exceed 25% of errors, else validator hardening.
- **Would change our mind:** a different team shape from the eng lead in week 0.

### D9. Leave four things out of V1, on purpose

- **Chose to defer:** hotel live availability (A9), price holds (A10), meal and baggage answers from fare data (T1), an authoritative visa feed (B5, B6).
- **Why:** flights drive the 50%; holds and fare data need supplier work; a visa feed needs a contract with outside lead time.
- **Mitigation in V1:** hotels show availability with its time and "confirmed at booking"; fare changes are disclosed before payment; meal and baggage questions deflect to the fare details; visa questions cite or deflect, with a human handoff (B4).

### D10. Measure against the decision price

- **Chose:** a booking counts as an error when the payment price differs from the price on the card when the user tapped Book, beyond ₹100 or 1%.
- **Rejected:** comparing with the last price shown.
- **Why:** A3 shows the new price before payment. Measured against the last price shown, every checkout would match and the metric would report success while users still paid more than they chose.
- **Would change our mind:** finance agreeing a different tolerance; the principle stays.

### D11. Give deflection a band, not a ceiling

- **Chose:** policy deflection held between 10% and 30%.
- **Rejected:** minimising deflection, or ignoring it.
- **Why:** above 30%, the corpus has gaps and the assistant feels useless; below 5%, the gate may be leaking. A gate that deflects everything scores 100% grounded, so grounded rate alone can be gamed.
- **Would change our mind:** audit data showing answered replies are accurate at a lower deflection rate; the band moves, and V2 targets 5–20%.

### D12. Roll out safely, and let V1 choose V2

- **Chose:** shadow for 2–3 days, then 10%, 50%, 100% of users, split by user; B1 and B2 first because they only remove risky answers; tuning by config knobs K1–K7, no new features mid-sandbox.
- **Rejected:** a fixed V2 roadmap, or a big-bang launch.
- **Why:** the cause mix behind "wrong price" is unknown until telemetry runs. Seven mechanisms produce the same complaint and each leaves a different fingerprint, so V2's first item depends on which fingerprint dominates.

## Questions the jury will ask

Each answer leads with the claim, then the evidence. Most are one or two sentences on purpose: a short, specific answer reads as conviction.

**"Price drives the 50%. Why spend any of the budget on visas?"** Because the two errors are not on the same scale. A wrong price costs a booking; a wrong visa answer can strand a family at the airport, and a tribunal has already held an airline liable for its chatbot's answer. B's core (B1, B2, B4) costs about 5 engineer-days, and A still gets 9.5 of Engineer 1's 10.

**"B scores lower on RICE than several A features. Aren't you ignoring your own framework?"** No. We use RICE for what it measures, expected value, and a severity gate for what it cannot see, irreversibility. Saying where a framework breaks is part of using it well.

**"Why not C? It has the higher accuracy ceiling."** Its ceiling is measured on the day it is trained. The day a visa rule changes, C is confidently wrong and cannot tell anyone; B is either right with a dated source or says it does not know. For a stranding risk, "I don't know" beats "confidently wrong".

**"Deflecting makes the assistant less useful. Won't users leave?"** Some might, which is why deflection has a 10–30% band and conversion is a guardrail with a 5% limit. Surveys in 2026 found only 8% of travellers comfortable booking through AI; one confident wrong answer costs more trust than one honest pointer to the official page.

**"A adds 1–2 seconds. On a mobile, lock-screen surface, that loses bookings."** That is why we rejected A as written. Live calls fire only at decisions, identical calls share one request, the user sees "checking the live fare" instead of a blank screen, and p90 time to price has a hard limit of baseline + 1.5 s.

**"How confident are you in 50% to 25–32%?"** It is sizing, not a forecast. It comes from a multiplication model whose inputs are illustrative; the range reflects the unknown cause mix. What holds for any plausible inputs is that fixing the weakest component lifts the trip rate most, and E1 replaces the inputs with measured ones in week 1.

**"What if the price errors aren't stale caches at all?"** Then V1 still helps and tells us what to do next. Seven mechanisms produce "wrong price"; A1, A2, A3 and A6 cover four of them, and telemetry fingerprints the rest: fee-shaped gaps point to A7, step-shaped gaps to A10 holds, key-shaped gaps to A8. If the spike tracks the festive-season demand peak, holds matter more than freshness.

**"Can you really build all this in 20 engineer-days?"** The plan uses 18.5 and holds 1.5. It has a written cut line: drop the B3 stamp first, then the buffer item. A5 (A2 cannot ship without it) and B4 (the stranding path) are never cut.

**"How do you know it worked, and not just that complaints moved?"** The north star is measured against the decision price, so disclosure cannot game it. Grounded claim rate must reach 99%. Complaints are read alongside, never used as a target, because A3 will briefly raise "price changed" notices before errors fall.

**"What does V1 still get wrong?"** Four named gaps: hotel live availability, fare jumps between decision and payment, meal and baggage answers, and an authoritative visa feed. Each has a V1 mitigation and a V2 slot. Naming them is deliberate; a plan that claims to fix everything has not looked closely.

**"If you had only one week?"** E1 telemetry, A1 price cards with the validator, A4 honest quote language, B1 and B2. That stops the model writing prices, stops policy answers from memory, and measures the rest.

## Assumptions, and what would change the plan

The decision rests on six assumptions; each is checked in week 0 or week 1, and each has a stated response if it proves wrong. The core rule (evidence before any claim, and no Option C) survives all of them; only the order of work changes.

| Assumption | Value used | Checked by | If wrong, we |
| --- | --- | --- | --- |
| Team shape | 2 engineers × 2 weeks | Eng lead, week 0 | Keep the rule; re-cut V1 at the same cut line |
| Price errors come mostly from aged or restated quotes | Implied by the brief | E1 gap fingerprints, day 7 | Spend the buffer on A8, or pull A7 or A10 into V2 first |
| Hotels are a minority of trip errors | Below 25% | E1, day 7 | Start A9 in the buffer and lead V2 with it |
| The assistant hands off to a checkout page | User confirms there | Week-0 question 5 | Add the V3 confirmation gate before any agentic booking |
| A policy document store exists | Yes, freshness unknown | Week-0 question 4 | Build a minimal index of official pages first; B2 deflects more at start |
| Volumes and mix | 100,000 quoted sessions a month; 90% flight, 45% hotel, 30% policy, 12% entry rules | Week-1 logs | Re-run RICE; Tier 0 items stay in regardless |

One question matters most: what changed 4–6 weeks ago. A model or prompt change, a cache TTL change, a new supplier, traffic past rate limits or seasonal demand each points to a different first fix.

## The argument in five sentences

1. The assistant's errors are not one hallucination problem but three: it states prices, policies and fare details it does not own, in one confident voice, with nothing checking a claim against its source.
2. The 50% is a trip-level rate, so the weakest component, flight price, dominates it, while the costliest errors (visa, refunds) surface too late to show up in it.
3. We therefore ship A and B as one rule, rebuilt around where each fails: prices fetched at the moment of decision and never written by the model, and policy answered only from a cited source, with a person for the stranding cases.
4. We cut C because it relocates staleness into model weights, where it cannot be seen, dated or cited.
5. V1 is measured against the price the user acted on, tuned by config in a sandbox, and its telemetry, not our assumptions, decides V2.

*Sources: Glance26 PM Intern case brief; Full plan (Travel Assistant Accuracy Plan, 30 Sep 2026) and its cited sources; V1 sprint plan; Travel Assistant Failure Map.*
