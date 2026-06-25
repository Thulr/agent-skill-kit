# Browser Verification

**Do not skip this step.** Reading source code is not the same as seeing the rendered page. Automate a visual check using your browser tools before declaring the artifact done.

## Required Checks

### 1. Load the artifact

Start a dev server or open the artifact file, then use your browser tool to navigate to it:

- `browser_navigate(url)` — load the page
- `browser_console(clear=True)` — clear any existing console noise first

### 2. Visual inspection

Use `browser_vision()` to take a screenshot and inspect the rendered output. Check:

- **Layout hierarchy** — is the primary action visible first? Does spacing match the design system scale?
- **Typography** — is the type readable at target sizes? Is the type stack actually loading?
- **Color** — does contrast pass? Are semantic roles applied correctly?
- **Anti-slop tropes** — any visual tropes from the anti-slop review that slipped through in the code but are obvious when rendered?
- **Content** — are placeholders still showing? Is copy cut off or overflowing?

Ask the vision tool specific questions like:
- *"Does this match the design brief layout?"*
- *"Is any text clipped or overlapping?"*
- *"Does the color contrast pass for the primary action button?"*

### 3. Console errors

After the page has rendered, read the browser console:

```
browser_console()
```

Flag any:
- JS runtime errors
- 404s for assets (fonts, images, icons)
- CSS parsing warnings
- Mixed content or network errors

### 4. Responsive viewports

If the brief calls for responsive behavior:

1. Take a full-width screenshot.
2. Resize the viewport and use `browser_vision` again. On most platforms, resize with a script like `browser_console(expression="window.resizeTo(768, 900)")` then re-snapshot.
3. Check for horizontal scroll, broken grids, missing mobile navigation, or text overflow at 768px and 375px widths.

### 5. Interaction states

If the artifact includes interactive elements (buttons, links, inputs):

- Use `browser_console(expression='document.querySelector(...)')` to verify hover/focus/press states exist in the CSS, or navigate through elements with keyboard tab order.
- Verify focus rings are visible.
- Verify disabled states render correctly.

### 6. Reduced motion

Check that the page respects `prefers-reduced-motion`. If motion is present, verify it either:
- Is removed or simplified under `@media (prefers-reduced-motion: reduce)`
- Uses only duration/transform combinations that are safe

## When to Rebuild

If any of the following are found during browser verification, **do not hand off** — rebuild or fix before proceeding:

- A layout issue visible on screen that was not visible in code (e.g. overlapping elements, broken grid)
- Console errors that affect functionality
- Anti-slop tropes that are obvious in the rendered page but weren't caught by code review
- Responsive breakpoint failures
- Missing or broken interaction states

## Tool Reference

| Check | Tool to use |
|---|---|
| Load the page | `browser_navigate(url)` |
| See what it looks like | `browser_vision(question="...")` |
| Read JS console | `browser_console()` |
| Run JS in page context | `browser_console(expression="...")` |
| Interact with elements | `browser_click(ref)` / `browser_type(ref, text)` |
| Resize viewport | `browser_console(expression="window.resizeTo(w, h)")` |
