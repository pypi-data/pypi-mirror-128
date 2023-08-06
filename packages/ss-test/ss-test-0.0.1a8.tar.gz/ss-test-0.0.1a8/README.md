# ss-test

test pypi publish

Install

```bash
pip install -i https://test.pypi.org/simple/ ss-test --extra-index-url https://pypi.org/simple
```

## Usage

```
usage: ss-test [-h] [--type {ratio,numeric,boolean}] [--effect EFFECT]

optional arguments:
  -h, --help            show this help message and exit
  --type {ratio,numeric,boolean}
                        The type
  --effect EFFECT       The effect, should be a number/float
```

example:
```bash
ss-test --type numeric --effect 0.5

# output
# Welcome to test pacakage!
# Calculating effect 0.5 of metric type numeric
# And Here's your secret result: 64.0
```