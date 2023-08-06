# PITER - virtual environments management tool for Python projects

## Idea
While working on Python project you may need multiple virtual environments. You can divide your development and test environments, have multiple environments to test against different version of libraries or ony other use cases

## Minimal configuration

Install `piter` with

```bash
pip install piter
```

Create or update `pyproject.toml` file with following configuration

```toml
[tools.piter]

[tools.piter.env.test]
dependencies = [
	"pytest==6.2.4", 
]
scripts.test = "pytest"

[tools.piter.env.dev]
dependencies = [
	"black==21.5b1",
]

scripts.lint = "black ."
scripts.check = "black --check ."
```

Available commands with this configuration

```bash
# install, remove and reinstall env 
piter env dev --install
piter env dev -i

piter env dev --remove
piter env dev -r

piter env dev --reinstall
piter env dev -ri


# run script without specifying env
piter run test

# run script
piter run lint --environment dev
piter run check -e dev
```
