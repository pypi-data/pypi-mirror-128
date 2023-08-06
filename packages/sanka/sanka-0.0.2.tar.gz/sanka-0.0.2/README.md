# sanka
> a function decorator for surfacing dead code

[![tests](https://github.com/withtwoemms/sanka/workflows/tests/badge.svg)](https://github.com/withtwoemms/sanka/actions?query=workflow%3Atests)
[![publish](https://github.com/withtwoemms/sanka/workflows/publish/badge.svg)](https://github.com/withtwoemms/sanka/actions?query=workflow%3Apublish)

# Setup
Ensure `nox` is installed.
```
pip install nox
```
Run `nox` to install `sanka` and run tests.

# Usage
Decorate any funciton with `@Sanka`.
```python
@Sanka
def function():
    pass
```
The decorator instance tracks function calls so the call count can be gotten as follows:
```
function(Sanka.YaDead)
```
