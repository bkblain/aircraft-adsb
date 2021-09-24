# Aircraft ADS-B

## Configure RTL-SDR

Install RTL-SDR linux libraries

```
sudo apt install rtl-sdr
```

## Installing Python Build Tools

Install PIP for package management

```
sudo apt install python3-venv python3-pip python3-tk
```

Don't install packages through pip, instead install pipenv which can be used to generate an environment for the project much like npm.

```
pip3 install pipenv
```

Ensure tools are up to date

```
python3 -m pip install --upgrade pip setuptools wheel
```

Install pipenv

```
python3 -m pip install --user pipenv
```

Restart your computer or user profile to refresh the `PATH` for the `pipenv` command.

## Install Dependencies

Inside the project directory, install the python rtlsdr library which wraps the librtlsdr.

```
pipenv install
```

Activate the Python virtual environment.

```
pipenv shell
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
