# Linux-SDM-Downloader 1.0.0
Downloader SDM files via SDX file (DreamSpark) on Linux (primary)

## What is it?
Linux-SDM-Downloader is Python script for download SDM files and joining to one file. For downloading these files is needed SDX file. SDM file is possible unpacking via [xSDM](https://github.com/v3l0c1r4pt0r/xSDM).

## Prerequisites
- BeautifulSoup
- Lxml

### Installing dependencies on Linux (debian):
```
# aptitude install python-beautifulsoup python-lxml
```
or
```
# apt-get install python-beautifulsoup python-lxml
```

## How to use
Download actual source code (unpacking) and run:
```
git clone https://github.com/RadekSimkanic/Linux-SDM-Downloader.git
cd Linux-SDM-Downloader
python main.py <SDX file>
```

Next step after successful process for unpacking SDM package is unpacking via [xSDM](https://github.com/v3l0c1r4pt0r/xSDM).

## News
28-10-2015:
- Version 1.0.0
- Enable downloading also ISO files (and maybe others files) via .SDX
- List of tested OS and status whether works ok or not.

29-01-2015:
- Created first beta version

## Tested
Version 1.0.0:
- **Linux Mint 17.1 Rebecca** | Python 2.7.6: **OK** (Radek Simkanič)
- **Linux Debian Wheezy** | Python 2.7.3: **OK** (Dominik Chrastecký)
- **Windows 10** | cygwin | Python 2.7.8: **OK** (Dominik Chrastecký)
- **Arch (4.2.5-1)** | Python 2.7.10: **OK**

Please tell me whether you work Linux-SDM-Downloader on your distribution.
