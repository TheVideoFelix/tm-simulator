# tm-simulator

`tm-simulator` is a small Python library and CLI for simulating **Turing machines** and **multi‑tape Turing machines** defined in a simple text format (`.TM` / `.MTTM` files).

The package exposes both a **Python API** and a **command‑line interface**.

## Features

- Single‑tape and multi‑tape Turing machines
- Load machines from `.TM` / `.MTTM` description files
- Step‑wise simulation with a textual tape view (state, head position, tape contents)
- Usable as:
  - a **Python library**
  - a **CLI tool** (`tm-simulator` entry point)

## Installation

```bash
pip install tm-simulator
```
## CLI Usage

After installation, you can run the simulator directly from the command line:
bash

```bash
tm-simulator path/to/machine.TM 1011
```

## Python API Usage

```py
from tm_simulator import load_tm, run_tm

run_tm("path/to/machine.TM", "1011")

# Or work with the TM
tm = load_tm("path/to/machine.TM")
tm.input(["1011"])
tm.run()
``
