# Motion and Effects

## Functional Motion

Motion must explain something: spatial continuity, state change, loading,
focus, or narrative progression. Decorative movement should be cut.

Default UI durations:

- 120ms for hover, press, and color swaps.
- 180ms for menus, accordions, and panel reveals.
- 260ms for modals, command palettes, and page-level entrances.

One curve covers most UI motion: `cubic-bezier(0.2, 0.6, 0.2, 1)`. Avoid
bounce and spring unless the brand is explicitly playful.

## Reduced Motion

Always honor `prefers-reduced-motion`. For UI transitions, collapse duration.
For decorative atmosphere, remove the moving layers entirely. The still design
must remain composed without motion.

## Loading

- Under 200ms: no indicator.
- 200-1000ms: small spinner, pulse, or dot.
- 1-5s: determinate progress if known; indeterminate bar if unknown.
- 5s+: progress plus a written status line.
- Known layout: skeletons beat spinners.

## Narrative Animation

For animated explainers or demo loops, drive sprites from one `currentTime`
value. Include scrubber, play/pause, and keyboard controls. Persist position
when useful so refresh does not lose the review moment.

Layered motion reads richer than one big animation. Combine layers with
different duration, phase, opacity, and amplitude. Co-prime durations prevent
obvious loop repeats.

## Performance

Animate transform and opacity first. Use filter sparingly. Avoid animating
width, height, top, left, margin, padding, and large shadows. Use
`will-change` only when needed and remove it when the animation stops.

## Depth and Effects

Choose the lowest-cost tool that creates the scene:

- Hairline borders and banded surfaces for 2D depth.
- Subtle shadow or blur for floating surfaces.
- CSS perspective and small rotateX/rotateY values for cards and panels.
- Parallax layers for depth cues.
- Blur and saturation stacks for focal depth.
- Three.js or WebGL only for real geometry, high particle counts, shaders, or
  material lighting.

Atmospheric effects need a focal anchor. Particles, starfields, aurora washes,
and godrays should support one thing the eye lands on. Build the effect, then
halve opacity and amplitude; the quieter version usually reads better.

## Debugging

When motion feels wrong, slow all animations to one-fifth speed and watch the
sequence. Most issues become obvious: wrong easing, excessive stagger, competing
layers, or movement that distracts from the content.
