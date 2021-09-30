# Aircraft ADS-B

## Installing RTL-SDR

Install RTL-SDR linux libraries

```
sudo apt install rtl-sdr
```

## Installing Python Build Tools

Install VENV for the virtual environment and PIP for package management

```
sudo apt install python3-venv python3-pip
```

Ensure that Python tools are up to date

```
python3 -m pip install --upgrade pip setuptools wheel
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

Activate the Python virtual environment. To leave the virtual environment shell at any point, run the `exit` command.

```
pipenv shell
```

Now run any of the python files.

```
python AdsbStreamer.py
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

