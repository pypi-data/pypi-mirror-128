# DataWhys Python SDK

DataWhys Python SDK is a python wrapper for the DataWhys API that provides additional functionality such as dataframe ingest and one-off processing

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install datawhys.

```bash
pip install datawhys
```

## Dependencies

- [python3](https://www.python.org/downloads/)

## Install from source

In the `mondobrain-python` directory (same directory as this README.md file), run this command in your terminal:
```bash
pip install -e .
```

## Usage
```python
import datawhys as dw

# Set your credentials
dw.api_key = "<API-KEY>"
dw.api_secret = "<API-SECRET>"

# Build a pandas dataframe and store in `df` (not shown)

# Convert your pandas df to a datawhys df
dwf = dw.DataWhysFrame(df)

# Select a column as your outcome column & specify a target class
outcome = dwf["column_name"]

# for a discrete column
outcome.target_class = "Some_modality"

# for a continuous column the value should be `min` or `max`
outcome.target_class = "max"

# Get a dataframe of all columns you want to explor
explorable = dwf[["column_a", "column_b"]]

# Create a solver instance
solver = dw.Solver()

# Fit your data
solver.fit(explorable, outcome)

# Check your results
solver.rule
```

See documentation and `SDK Example.ipynb` in the `mondobrain-python` directory for more in depth examples.

The package includes documentation to provide explanation and examples of usage.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Take a look at `CONTRIBUTING.md` for more info

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)