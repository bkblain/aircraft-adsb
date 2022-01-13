# Aircraft ADS-B

## Installing RTL-SDR

Install RTL-SDR linux libraries

```
sudo apt install rtl-sdr
```

## Installing Python Build Tools

Install VENV for the virtual environment, PIP for package management, and PyLint for code linting

```
sudo apt install python3-venv python3-pip pylint
```

Don't install application packages directly through pip, instead install pipenv which can be used to generate a virtual environment.

```
python3 -m pip install --user pipenv
```

Restart your computer or user profile to refresh the `PATH` for the `pipenv` command.

## Installing Dependencies

Inside the project directory, install the python project dependencies.

```
pipenv install
```

## Execute Project Files

```
pipenv run python src/adsb_streamer.py
```

## Build Python Wheel

```
pipenv run python -m build
```

# References

https://inst.eecs.berkeley.edu/~ee123/sp14/lab/lab1-Time_Domain_III-SDR.html

https://mode-s.org/decode/misc/preface.html

https://pysdr.org/index.html

https://en.wikipedia.org/wiki/List_of_airline_codes

https://en.wikipedia.org/wiki/List_of_aircraft_type_designators#cite_note-ICAOcode-3

https://pyrtlsdr.readthedocs.io/en/latest/


To Read

https://junzis.com/files/pymodes.pdf

https://pyrtlsdr.readthedocs.io/_/downloads/en/latest/pdf/


Example how to demodulate signal

https://github.com/junzis/pyModeS


Main with CLI

https://softwareengineering.stackexchange.com/questions/418600/best-practice-for-python-main-function-definition-and-program-start-exit

