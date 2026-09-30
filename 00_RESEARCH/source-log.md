# Source log

Research date: 30 September 2026. ● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation

## Method and limits
- Sources were read through public pages, press, store listings and a brand registry. **The production stylesheet, font files and
  screenshots could not be inspected directly from this environment** (direct network access to glance.com was blocked by policy), so:
  - no pixel value, font or spacing is labelled ● Observed unless a source states it;
  - the two brand hues (#FF0049, #DDBEF0) are ● observed via a brand registry (S3), not via Glance's own CSS;
  - everything else visual is ◐ inferred from described behaviour, ○ reconstructed, or ◇ original.
- Store-listing claims (ratings, MAU) are company-reported and were not independently verified.
- Glance ships different experiences by market (India lock screen with games, video and ads; US lock screen as a news widget; Glance AI
  app for shopping). This package treats them as one family and says which surface an observation comes from.

| ID | Source | Type | What it established |
|---|---|---|---|
| S1 | [Glance homepage](https://glance.com/) | Primary | Taglines ('Glance it. Shop it.', 'Shopping that Understands You'), single 'Download The App' CTA, dark hero-first layout, sections for AI agents. |
| S2 | [Glance · About us](https://glance.com/us/about-us) | Primary | Agentic commerce positioning; surfaces: lock screen, app, connected TV, brand sites; 'Shopping, minus the heavy lifting'; US MAU claims. |
| S3 | [Brandfetch · glance.com](https://brandfetch.com/glance.com) | Secondary (brand registry) | Brand colours #FF0049 / #FC034D (red), #DDBEF0 (lavender), #000000. No font listed. |
| S4 | [TechCrunch · Glance launches gen-AI shopping on the lock screen (Feb 2025)](https://techcrunch.com/2025/02/26/lockscreen-platform-glance-launches-gen-ai-led-shopping-experience-gets-fresh-backing-from-google) | Secondary (press) | Selfie-based avatar; outfits on the lock screen; CEO: like a fashion magazine where you are the model; tap reveals products from ~400 partners. |
| S5 | [Android Central · Glance AI lock-screen visuals](https://www.androidcentral.com/apps-software/glance-ai-allows-to-shop-fashion-via-personalized-ai-generated-lock-screen-visuals) | Secondary (press) | Save / share / set as wallpaper; one tap to explore looks and products; 1.5M active users in US trials, half returning weekly. |
| S6 | [Forbes · Glance AI and Samsung (Jun 2025)](https://www.forbes.com/sites/charliefink/2025/06/04/glance-ai-and-samsung-bring-personalized-shopping-to-the-lock-screen/) | Secondary (press) | Opt-in; 'you're reacting to an image of yourself'; purchase from the screen; seasonal and limited-time highlights. |
| S7 | [Glance press release · AI-native commerce platform](https://glance.com/us/newsroom/pressrelease/glance-ai-launches-ai-native-commerce-platform-for-hyper-real-visual-shopping) | Primary | Three-model architecture; looks styled on the user; save/share/wallpaper; plans to expand to beauty, accessories and travel. |
| S8 | [App Store · Glance – My Personal Shopper](https://apps.apple.com/us/app/glance-my-personal-shopper/id6742974181) | Primary (store listing) | Personalised feed, moodboards, shoppable collections by colour/style, chat to refine, weather/trend/occasion awareness, Siri entry, home-screen widget. |
| S9 | [Google Play · Glance – Shop with AI](https://play.google.com/store/apps/details?id=com.glance.ai) | Primary (store listing) | 'Styled around you'; editorial-quality imagery 'starring you'; reviews complain about forced installs and hard-to-remove behaviour. |
| S10 | [Google Play · Glance AI Lockscreen](https://play.google.com/store/apps/details?id=com.glance.ailockscreen) | Primary (store listing) | AI Looks, live widgets (weather, steps), curated news and scores 'without even unlocking your phone'. |
| S11 | [InMobi · Partner with Glance](https://go.inmobi.com/partner-with-glance/) | Primary (advertiser page) | Ad formats: Impact (full-screen imagery), Engagement (video, interactive), Promotion (one-click installs); content before unlock; ~200M Indian users. |
| S12 | [9to5Google · Glance lock screen in the US (Apr 2024)](https://9to5google.com/2024/04/26/glance-android-lockscreen-motorola-turn-off/) | Secondary (press) | Persistent news widget with category tags; weather appears when conditions change; full-screen prompts to re-enable. |
| S13 | [Medium · Samsung Glance news stories](https://androidlockscreeen.medium.com/swipe-to-stay-updated-exploring-the-news-stories-on-the-samsung-glance-lock-screen-b2d7d2eac614) | Tertiary (blog; lower reliability) | Horizontal swiping between stories; ~10 category tabs starting with 'For You'; 'catch up in seconds'. |
| S14 | [Glance blog · Smart AI shopping platform features](https://glance.com/us/blogs/glanceai/fashion/smart-ai-shopping-platform) | Primary (company blog) | Natural-language + visual search; feeds from saves and dwell time; context-aware (time, location, events); fit-confidence percentages; single-tap checkout. |

## Reference material not used as design primitives
The Glance name, logo and wordmark, product photography and AI-generated imagery are Glance's property. They were used only as
reference. This package's wordmark ("wake"), icons, placeholder imagery and screens are original.
