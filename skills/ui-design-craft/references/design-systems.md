# Design Systems

## System-First Rule

A design system is a binding contract. If it exists, every visual decision has
a default answer: documented colors, type, spacing, radius, motion, components,
content rules, and examples. Compose those defaults before extending them.

## First Contact

When a system is referenced:

- Read the guide, including side notes, examples, and "do not" rules.
- List the folder or package to find tokens, components, UI kits, assets, and
  preview pages.
- Read high-fidelity example screens. Forking a kit beats rebuilding from
  memory.
- Copy only the token files, assets, and components actually used by the
  artifact; avoid broad noisy imports.

## Honoring the System

- Use documented palette roles. If a tint is missing, derive it from a system
  color with `color-mix(in oklch, ...)` rather than adding a new hex.
- Use documented type stacks and casing rules.
- Use the spacing and radius scales; odd one-off values are a tell.
- Use component vocabulary. If the system has a pill, chip, banner, or row,
  use its name and structure.
- Read voice rules. Sentence case, punctuation, pronouns, emoji policy, and
  forbidden words are part of the system.

## Extensions

Extend only when the product needs something the system does not cover. The
extension must reuse the system's density, radii, type logic, color roles, and
state behavior. Add a short note: what was missing, why the extension exists,
and what existing component could replace it if preferred.

Never silently invent a component because you did not look long enough.

## Authoring a New System

A usable system includes:

- README with audience, personality, contents, usage, and extension rules.
- Tokens for color, type, radius, spacing, and motion.
- Assets: logo mark, wordmark, and a single icon family.
- UI kit or preview screens proving the tokens work in real product contexts.
- Preview pages for color, type, components, brand, and voice.
- Voice rules with "bad -> good" examples.

Ship 8-12 useful neutrals, 1-2 accents, and 3-4 semantic colors. Huge palettes
create drift. Build the kit screen-by-screen, including boring states: empty,
loading, error, dense lists, and forms. A system that cannot compose a new
screen using only its tokens and components is too small.

## IP Boundary

Do not recreate a distinctive company UI unless the user is plausibly working
for that company or owns the rights. Offer an original design in a similar
spirit instead.
