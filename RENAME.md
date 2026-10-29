# Renaming the project

The project is named `laservigil` (display name **Laservigil**). The runtime name
(used in the CLI prog name, `--version`, banner and error messages) comes from
**one constant**:

- `src/laservigil/_meta.py`: `NAME = "laservigil"`

Python packaging and import paths can't read that constant, so the name also
appears in the places below. This list was checked with
`grep -rniI laservigil --exclude-dir=.git .` (case-insensitive, so it catches
every casing).

The name appears in three casings, and each one needs its own replacement:

| Casing | Example | Where |
| --- | --- | --- |
| lowercase `laservigil` | `NAME = "laservigil"`, `python -m laservigil` | code, config, tests, CLI usage, paths |
| capitalised `Laservigil` | `# Laservigil` | display name in README prose |
| uppercase `LASERVIGIL` | `// LASERVIGIL :: ...` | sample banner output in README |

## Code and config (must change)

| File | Line(s) | Occurrence |
| --- | --- | --- |
| `src/laservigil/` | (directory) | Package directory name. Rename it to `src/<newname>/` |
| `src/laservigil/_meta.py` | 6 | `NAME = "laservigil"` |
| `pyproject.toml` | 6 | `name = "laservigil"` (distribution name) |
| `pyproject.toml` | 18 | `laservigil = "laservigil.cli:main"` (console script and module path) |
| `pyproject.toml` | 21 | `version = { attr = "laservigil._meta.VERSION" }` |
| `.github/workflows/ci.yml` | 25 | `python -m laservigil scan ...` (smoke test) |
| `tests/test_color.py` | 3, 4 | `from laservigil import color`, `from laservigil.color import ...` |
| `tests/test_fetchers.py` | 5 | `from laservigil.fetchers import ...` |
| `tests/test_checks.py` | 3, 4 | `from laservigil.checks ...`, `from laservigil.fetchers ...` |
| `tests/test_cli.py` | 5, 6 | `from laservigil import NAME, VERSION`, `from laservigil.cli import main` |

The source modules inside the package use relative imports, so they don't contain the name.

## Docs (prose and examples)

| File | Line(s) | Occurrence |
| --- | --- | --- |
| `README.md` | 1 | `# Laservigil` title (display name) |
| `README.md` | 10, 21, 55 | Prose mentions (display name `Laservigil`) |
| `README.md` | 30, 31, 45, 46 | Usage commands (`laservigil scan ...`, `python3 -m laservigil`) |
| `README.md` | 35 | Sample output banner `// LASERVIGIL :: ...` (uppercase) |
| `README.md` | 81 | Architecture tree `src/laservigil/` |
| `RENAME.md` | throughout | This file |

## Derived at runtime (follows `NAME` automatically)

- CLI banner `// <NAME upper> :: ...`, argparse `prog`, `--version` output and
  `<NAME>: error` messages in `src/laservigil/cli.py`.

## Rename recipe

`NEW` must be lowercase and a valid Python identifier (it becomes the import
name). The capitalised and uppercase forms are derived from it.

```sh
NEW=newname
NEW_CAP="$(printf '%s' "$NEW" | cut -c1 | tr '[:lower:]' '[:upper:]')$(printf '%s' "$NEW" | cut -c2-)"
NEW_UPPER="$(printf '%s' "$NEW" | tr '[:lower:]' '[:upper:]')"
git mv src/laservigil "src/$NEW"
grep -rliI laservigil --exclude-dir=.git . | xargs sed -i \
  -e "s/laservigil/$NEW/g" \
  -e "s/Laservigil/$NEW_CAP/g" \
  -e "s/LASERVIGIL/$NEW_UPPER/g"
python3 -m pytest -q
```

The `grep -i` is what makes sure files that only contain `Laservigil` or
`LASERVIGIL` are picked up. On macOS/BSD use `sed -i ''` instead of `sed -i`.

## Checklist

- [ ] `src/laservigil/` directory renamed
- [ ] lowercase: `grep -rnI laservigil --exclude-dir=.git .` returns nothing
- [ ] capitalised: `grep -rnI Laservigil --exclude-dir=.git .` returns nothing
- [ ] uppercase: `grep -rnI LASERVIGIL --exclude-dir=.git .` returns nothing
- [ ] any casing: `grep -rniI laservigil --exclude-dir=.git .` returns nothing
  (also catches any mixed casing, which the recipe does not replace)
- [ ] `python3 -m pytest -q` passes and `python3 -m <newname> --version` prints the new name
