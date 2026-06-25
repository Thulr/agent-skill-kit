# Components and Content

## Components

Use boring, legible structures and make them distinctive through tokens.

- **Buttons:** primary, secondary, ghost. One primary per surface when possible.
  Typical heights are 28, 32, and 36px; touch targets need 44x44px even when
  the visible button is smaller. Icon + label gaps sit around 6-8px.
- **Inputs:** 32-36px tall. Labels above, not placeholder-only. Error message
  below, one sentence, no apology. Required markers should not make the whole
  label red.
- **Cards and panels:** border or fill, not both by default. Use shadows only
  for surfaces floating above the page. Avoid cards inside cards.
- **Lists:** left rail, title/subtitle middle, metadata right rail. Use
  `minmax(0, 1fr)` so text can truncate.
- **Navigation:** top bar for global areas, side rail for deep IA, tabs for
  peer views, breadcrumbs only for real depth.
- **Badges and chips:** small, role-colored, compact. Counters cap gracefully.
- **Tooltips:** explain icon-only or unfamiliar controls; no obvious labels.
- **Modals:** use sparingly; inline edit, side panel, or full page often works
  better.
- **Tables:** right-align numbers, left-align text, sticky header when
  scrolling, no vertical lines unless the data requires them.

## Content Rules

Copy is part of visual quality. **Every element must earn its place.** If a
section feels empty, solve the composition rather than adding generic words.

Avoid filler of any kind:

- Fake metrics or decorative stats that have no real backing.
- Generic feature grids with no substantive content difference.
- Unnecessary icons placed just to fill visual space.
- Placeholder testimonials or fake customer names.
- AI-generated fluff sections (generic "Why Choose Us", "Our Mission" blocks).
- Stock-photo or generic decorative imagery that communicates nothing.

When real content is missing, use honest placeholders. Do not fabricate data
that implies claims about the product.

Default voice when no system exists:

- Sentence case for product UI.
- Short declarative labels.
- Body copy of one to three sentences.
- Empty state: one sentence plus one action.
- No exclamation marks, emoji, hedging, or cheerleading unless the brand uses
  them.
- Use product vocabulary exactly; do not rename a "notebook" into a "vault".

## Content Tropes to Cut

Avoid product chrome that says "Let's get started", "Awesome", "AI assistant
is ready", "Click here", "Discover", "Unlock", "Supercharge", or vague labels
like "Insights", "Growth", "Scale", "Optimize" without real content. Replace
generic actions with the action itself: "Open", "Save", "Connect runtime",
"Create note".

## Honest Placeholders

If real content is missing, use explicit placeholders such as `[Customer quote,
2 sentences]` or `[Usage metric from analytics]`. Do not invent fake customer
names, fake logos, fake quotes, or fake statistics. Fake data makes a polished
design feel cheap and creates cleanup work for the user.

## Component State Floor

For any component likely to ship, include resting, hover, focus, press,
disabled, empty, loading, and error states as applicable. State coverage is
where design systems and prototypes prove whether they are real.
