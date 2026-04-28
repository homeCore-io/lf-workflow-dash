# homeCore Workflow Dashboard

[![Live dashboard](https://img.shields.io/badge/dashboard-homecore.io-blue?style=flat-square)](https://homecore.io/lf-workflow-dash/)

CI / Release status across every active homeCore-io repo, refreshed every
15 minutes. Forked from
[lincc-frameworks/lf-workflow-dash](https://github.com/lincc-frameworks/lf-workflow-dash).

## What's tracked

`config/tracked_workflows.yaml` lists each repo + the workflows the dashboard
shows. Today: `homeCore` + 10 plugins + `hc-tui`, with `ci.yml` shown as
"Live Build" and `release.yml` listed under "Other Workflows".

To add a repo, add a block to `tracked_workflows.yaml`:

```yaml
- repo: hc-newthing
  owner: homeCore-io
  live-build: ci.yml
  other_workflows:
    - release.yml
```

…then either push to `main` (next cron tick picks it up) or force a refresh
with:

```sh
gh workflow run main.yml --repo homeCore-io/lf-workflow-dash --ref main
```

## How it deploys

- `*/15 * * * *` cron in `.github/workflows/main.yml` runs `update_dashboard.py`,
  which writes `html/index.html`.
- `JamesIves/github-pages-deploy-action@v4` pushes `html/` to the `gh-pages`
  branch.
- GitHub Pages serves `gh-pages` at the org's custom domain `homecore.io`,
  which redirects to https://homecore.io/lf-workflow-dash/.

## Per-repo badges

Every tracked repo's README header carries three badges — CI status,
Release status, and a "builds → dashboard" link to this dashboard. See the
`docs(readme): add CI/Release status + Dashboard badges to header` commit
across the tracked repos for the canonical pattern.

## Upstream changes

This is a hard fork (no longer in GitHub's fork network). To pull future
upstream improvements:

```sh
git remote add upstream https://github.com/lincc-frameworks/lf-workflow-dash.git
git fetch upstream
git merge upstream/main   # or cherry-pick
```
