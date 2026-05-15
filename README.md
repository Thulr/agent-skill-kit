# heuristic-skills

A collection of [Agent Skills](https://agentskills.io)—original work, forks, and experiments—installable with the open ecosystem CLI ([skills.sh](https://skills.sh)).

## Install

From GitHub (replace `owner/repo` once this repository is published):

```bash
npx skills add owner/heuristic-skills
```

Install specific skills or target agents:

```bash
npx skills add owner/heuristic-skills --list
npx skills add owner/heuristic-skills --skill my-skill --skill other-skill
npx skills add owner/heuristic-skills -a claude-code -a cursor -y
```

From a subdirectory URL (single skill):

```bash
npx skills add https://github.com/owner/heuristic-skills/tree/main/skills/my-skill
```

Local checkout:

```bash
git clone https://github.com/owner/heuristic-skills.git
cd heuristic-skills
npx skills add . --list
npx skills add .
```

Use `-g` / `--global` for user-wide installs; default is project scope. See `npx skills --help`.

## Layout

| Path | Purpose |
|------|---------|
| `skills/<name>/` | Shareable skills (`SKILL.md` + optional assets) |
| `skills/.experimental/<name>/` | Work-in-progress or caveat-heavy skills (still discovered by `npx skills`) |
| `THIRD_PARTY.md` | Attribution and licenses for skills not authored here |

Skills marked internal in frontmatter (`metadata.internal: true`) are hidden unless `INSTALL_INTERNAL_SKILLS=1` is set when using the CLI.

## Authoring

Create a new skill template:

```bash
npx skills init my-skill
```

Move the resulting folder under `skills/` or `skills/.experimental/` as appropriate. Each skill needs valid YAML frontmatter with at least `name` and `description`.

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).
