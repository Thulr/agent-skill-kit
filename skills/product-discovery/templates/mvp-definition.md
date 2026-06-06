# MVP Definition: <product / bet>

Output shape for the `scope-mvp` intent. Work top-down through the product-market-fit pyramid;
the MVP is the smallest build that tests the value hypothesis.

## Pyramid (top-down)

- **Target customer:** <specific segment>
- **Underserved need:** <the high-importance, low-satisfaction need this serves>
- **Value proposition:** <how we meet that need better than the alternatives they use now>

## Value hypothesis

- **We believe** <target customer> **will** <behavior / value> **because** <need>.
- **The MVP tests this by** <what the MVP exposes them to>.

## Minimal feature set

<Only what's needed to test the value hypothesis. Justify each; defer the rest explicitly.>

| Feature | Why it's needed for the value test | In MVP? |
|---|---|---|
| <feature> | <serves the hypothesis> | yes |
| <feature> | <nice but not tested> | **deferred** |

## Fit signal & loop

- **Product-market-fit signal (set before building):** <metric + threshold — e.g. % who'd be
  very disappointed without it; retention; activation>
- **Build-measure-learn loop:** <what we ship, what we measure, what decision the result drives>

> If the riskiest assumption can be tested without code, run that first (see assumption-test-plan).
