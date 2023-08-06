This script is solving set problems by brute-force. See [HOWTO](#HOWTO).

# HOWTO
Use python3.10 or newer. Download it [here](https://www.python.org/downloads/). 

```
"python.exe" -m pip install SetSolver1
```

First import the module:
```
import SetSolver1
```

Now you can use the method:
```
SetSolver1.search(const_sets: dict[str, set[frozenset | int]], result: set[frozenset | int]) -> list[set] | None
```

Where `const_sets` is a dictionary for the predefined constants and `result` is the wanted solution.
With the method `search` you can find the probably shortest way to this solution by the predefined constants
and normal set operations. With this method you will get a list of valid ways (mostly one way) back. 

Little example:
```
import SetSolver1

# Here you set your predefined constants.
# Please make sure that you do not assign a variable letter twice.
# Python dictionaries will otherwise only store the last value and overwrite the previous ones.
const_sets: dict[str, set[frozenset | int]] = {
    "A": {frozenset({2, frozenset()}), frozenset({5})},
    "B": {frozenset(), frozenset({3}), frozenset({5})}
}

# Here you set your wanted solution.
result = {frozenset(), frozenset({3}), frozenset({5}), frozenset({frozenset()})}

output = SetSolver1.search(const_sets, result)
```


See German examples [here](beispiele.md) with outputs.

# Requirements

- python3.10 required

# Credits

- https://stackoverflow.com/a/25823885
- https://stackoverflow.com/a/13149770
- https://stackoverflow.com/a/176921
- https://stackoverflow.com/a/24065533
- https://stackoverflow.com/a/33945518
- https://stackoverflow.com/a/56143543
- https://stackoverflow.com/a/40876432
- https://stackoverflow.com/a/30986796
- https://stackoverflow.com/a/24261311
- https://stackoverflow.com/a/3274100
- https://stackoverflow.com/a/26576036
- https://stackoverflow.com/a/1482316
- https://stackoverflow.com/a/16543406
- https://stackoverflow.com/a/28845328
- https://stackoverflow.com/a/5931299
- https://stackoverflow.com/a/15768778
