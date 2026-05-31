# Auth Playbook

## Scope

Token UX, credential rotation, scope errors, OAuth flows, API key handling,
expiry, and revocation. Routes to `errors.md` for auth-failure message copy,
`cli.md` if the CLI configures or stores credentials, and `api.md` for
auth-related response shapes.

## Grounding

- **OWASP Foundation — Application Security Verification Standard (ASVS)** —
  standard checklist for authentication, session management, and access control;
  concrete per-level requirements for token lifecycle, storage, and revocation.
- **NIST — Digital Identity Guidelines: Authentication and Lifecycle Management
  (SP 800-63B)** — authenticator assurance levels, token lifecycle rules, and
  normative guidance on password and token handling.
- **Stripe — public docs on API Key Management** — concrete operational patterns
  for scoped keys, test vs live separation, rotation UX, and revocation.

## Good signals

- Expired-token errors say "token expired" and name the refresh or re-auth path.
- Scope errors name which scope is missing and describe how to grant it.
- Key rotation has a documented dual-key window — old and new are both valid
  during rollover so deploys are zero-downtime.
- Secrets never appear in logs, error messages, or `--verbose` output.
- Revocation is documented and propagates within a stated time bound.
- New keys start with least-privilege scope; broadening requires an explicit
  action.
- Test and live keys carry distinct prefixes or visual formatting that makes
  cross-environment paste errors obvious before the request fires.
- Expiry warnings are issued before failure — users get notice (e.g. 7 days
  ahead) so they can rotate without an outage.

## Common failures

- "Unauthorized" with no detail — was it the key, the scope, the expiry, or a
  clock skew? The caller has no path forward.
- No rotation path — replacing a key means downtime because there is no overlap
  window.
- Secrets appear in `--verbose` output, structured logs, or error context objects.
- OAuth callbacks break on localhost or when the port shifts during development.
- Expired tokens fail silently or produce cryptic backend errors with no
  indication that re-auth is needed.
- Test and production keys are visually identical; developers paste the wrong
  one and wonder why charges are real.
- Scopes default to over-broad permissions ("admin"); least-privilege is not
  offered as a starting point.
- Revocation takes hours to propagate; a credential marked revoked still
  authenticates requests.

## Heuristics

- **Named auth-failure cause** *(audit, design, debug)* — every auth failure
  names the cause class: expired, wrong scope, revoked, wrong audience, clock
  skew. "Unauthorized" alone is never enough.
- **Documented scope errors** *(audit, design)* — scope-mismatch errors name
  the missing scope and the path to grant it. The developer should not need to
  open a docs page to understand what is blocked and why.
- **Dual-key rotation window** *(design)* — rotating credentials allows both
  old and new to work during a documented overlap window. Zero-downtime rotation
  is a first-class requirement, not an afterthought.
- **Secret hygiene** *(audit, design)* — secrets are masked in all output paths:
  logs, error objects, and `--verbose` output. Audit every log sink and serializer
  when adding debug context.
- **Working revocation** *(audit, design)* — revoking a credential actually
  invalidates it within a stated time bound. "Revoked" is not cosmetic.
- **Expiry warning before failure** *(design)* — users receive advance notice
  before a credential expires. Failure without warning is an avoidable outage.
- **Visually-distinct environment keys** *(design)* — keys carry a prefix or
  structural marker that prevents cross-environment paste errors. Test and live
  keys should be impossible to confuse at a glance.
- **Least-privilege default** *(design)* — new keys start with minimal scope.
  Broadening permissions requires an explicit deliberate step, not an implicit
  default.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does every auth failure name a cause? | Opaque "unauthorized" | Add cause classification to auth error responses |
| Is there a documented rotation window? | Rotation means downtime | Implement dual-key overlap and document the window |
| Are secrets masked in all error paths? | Credential leakage | Audit log sinks and verbose output serializers |
| Does revocation propagate within a time bound? | Ghost tokens remain valid | Add and document invalidation propagation |
| Are test and live keys visually distinct? | Cross-environment paste errors | Add a prefix or format distinction between environments |
| Are scopes least-privilege by default? | Blanket admin permissions | Re-default new keys to minimum required scope |

## Cross-references

- → `errors.md` for auth-failure message copy and recovery hints.
- → `cli.md` if the CLI configures or stores credentials.
- → `api.md` for auth-related response shapes.
