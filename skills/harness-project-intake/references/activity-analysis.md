<!-- Activity analysis by language — used by project-analyzer agent -->
<!-- Extract project activity information from git log, package management files, and configuration files -->

## Activity Dimensions

| Dimension | Data Source | Command/Method |
|---|---|---|
| Recent Commits | git log | `git log --oneline -10` |
| Commit Frequency | git log | `git log --oneline --since="30 days ago"` |
| Contributors | git shortlog | `git shortlog -sn --no-merges` |
| Version | Package manifest / git tag | `git describe --tags --abbrev=0` |
| CHANGELOG | CHANGELOG.md / CHANGES.md | File existence + last update |
| Dependency Updates | Lock file modification time | File metadata |
| Issue Activity | GitHub CLI | `gh issue list --limit 5` |
| PR Activity | GitHub CLI | `gh pr list --limit 5` |

## Git Analysis Commands

### Basic Activity

```bash
# Last 10 commits
git log --oneline -10

# Commit frequency in last 30 days
git log --oneline --since="30 days ago" | wc -l

# Latest commit date
git log -1 --format="%ai"

# Contributor ranking
git shortlog -sn --no-merges | head -10

# Most active commit times (hourly distribution)
git log --format="%ad" --date=format:"%H" | sort | uniq -c | sort -rn
```

### Version Info

```bash
# Latest tag
git describe --tags --abbrev=0 2>/dev/null

# All tags (sorted by version)
git tag --sort=-v:refname | head -10

# Latest tag date
git log -1 --format="%ai" $(git describe --tags --abbrev=0 2>/dev/null) 2>/dev/null
```

### Code Volume Statistics

```bash
# Line count by language (requires cloc)
cloc --json .

# Simple count (by extension)
find . -name "*.ts" -o -name "*.js" | xargs wc -l | tail -1
```

## Language-Specific Version Detection

### Node.js / TypeScript

```bash
# Extract version from package.json
cat package.json | jq '.version'

# Extract Node version from .nvmrc or .node-version
cat .nvmrc 2>/dev/null || cat .node-version 2>/dev/null

# Extract from package.json engines
cat package.json | jq '.engines.node'
```

### Python

```bash
# Extract version from pyproject.toml
grep '^version' pyproject.toml

# Extract version from setup.py
grep 'version=' setup.py

# Extract version from __init__.py
grep '__version__' src/*/__init__.py 2>/dev/null
```

### Go

```bash
# Extract module name and version from go.mod
head -3 go.mod

# Extract version from git tag
git describe --tags --abbrev=0 2>/dev/null
```

### Rust

```bash
# Extract version from Cargo.toml
grep '^version' Cargo.toml

# Extract version from git tag
git describe --tags --abbrev=0 2>/dev/null
```

### Java / Kotlin

```bash
# Maven project: extract version from pom.xml
grep '<version>' pom.xml | head -1

# Gradle project: extract version from build.gradle
grep 'version' build.gradle | head -1
```

### PHP

```bash
# Extract version from composer.json
cat composer.json | jq '.version'

# Get version from Laravel
php artisan --version 2>/dev/null
```

### Ruby

```bash
# Extract version from gemspec
grep 'version' *.gemspec 2>/dev/null

# Get version from Rails
rails --version 2>/dev/null
```

## CHANGELOG Detection

```bash
# Check CHANGELOG file existence
ls CHANGELOG.md CHANGES.md HISTORY.md CHANGES.rst 2>/dev/null

# Extract recent entries (first 20 lines)
head -20 CHANGELOG.md 2>/dev/null

# Check last update date
head -5 CHANGELOG.md | grep -i "date\|version\|##" 2>/dev/null
```

## GitHub Activity (if GitHub CLI is available)

```bash
# Recent 5 issues
gh issue list --limit 5 --json title,createdAt,state

# Recent 5 PRs
gh pr list --limit 5 --json title,createdAt,state

# Recent releases
gh release list --limit 5

# Repository statistics
gh repo view --json stargazerCount,forkCount,createdAt,pushedAt
```

## Activity Rating

| Metric | Active | Normal | Inactive |
|---|---|---|---|
| Recent Commit | < 7 days | 7-30 days | > 30 days |
| Monthly Commits | > 20 | 5-20 | < 5 |
| Contributors | > 5 | 2-5 | 1 |
| Version Update | < 3 months | 3-12 months | > 12 months |
| CHANGELOG | Present & updated | Present but outdated | None |

## Output Format

Activity information is output to the project card in the following format:

```markdown
### Recent Activity

- Recent commit: `2024-01-15 — fix: resolve auth middleware bug`
- Version: `v2.1.0` (2024-01-10)
- Contributors: 5 people (last 30 days)
- Monthly commits: 23
- Activity: Active

### Known Constraints / Notes

- CHANGELOG last updated 2023-06, may be outdated
- Dependency `lodash` version is old, upgrade recommended
```

## Edge Case Handling

### No Git History

**Scenario**: Project has no git repository or git history is empty
**Handling**: Mark activity dimensions as "No git history"

### Single-Commit Project

**Scenario**: Project has only one initial commit
**Handling**: Mark as "Single-commit project, possibly a template or example"

### Fork Project

**Scenario**: Project is a fork with an upstream repository
**Handling**: Check for independent commits, note the fork source

### Empty Repository

**Scenario**: Repository exists but has no meaningful code
**Handling**: Mark as "Empty repository or still initializing"
