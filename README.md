# Aircraft ADS-B

## Installing Python Build Tools

Install PIP for package management

```
sudo apt install python3-venv python3-pip
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

Create the virtual environment

```

```

## Configure RTL-SDR

Install RTL-SDR linux libraries

```
sudo apt install rtl-sdr
```

Install the python rtlsdr library which wraps the librtlsdr

```
pipenv install pyrtlsdr
```
