# isensus

isensus, contraction between '(MPI-)IS and census' is a tool for the IT systems admins of the Max Planck Institute for Intelligent System to track the status of their users.

It is no much more than a fancy todo list reading a database of users encapsulated in a JSON formated file.


## Requirements

`Python 3.5` or higher.

## Installation

```bash
pip install isensus
```

## Tests

To run the tests:

```bash
git clone https://github.com/MPI-IS/isensus.git
cd isensus
python3 -m pytest ./tests/tests.py
```

## Documentation

To build the documentation:

```bash
pip install sphinx sphinx-bootstrap-theme
git clone https://github.com/MPI-IS/isensus.git
cd isensus
cd doc
make html
```

The html documentation will be built in the `build` folder.

## Author

Vincent Berenz, Max Planck Institute for Intelligent Systems

## License

BSD-3-Clause (see LICENSE.md).


## Copyright

© 2020, Max Planck Society