# JSON-TO-Table

Convert JSON File to CSV or XLSX File.

## Installation

Install JSON-TO-Table using pip:

```bash
pip install json-to-table
```

## Usage/Examples

```bash
# Show Header
$ j2t head data/example.json --n 5
    name  age  married
0   Mike   18     True
1    Tom   25    False
2   Jane   20     True
3    Bob   30    False
4  Alice   22     True
# Convert JSON to CSV
$ j2t convert data/example.json
# Convert JSON to XLSX
$ j2t convert data/example.json --t xlsx
```

## Authors

- [@duyixian1234](https://www.github.com/duyixian1234)
