# Download CodinGame

Download all your CodinGame solutions to your computer!

## Setup

```bash
git clone https://github.com/darthwalsh/DownloadCodinGame.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run

Follow [login instructions](https://codingame.readthedocs.io/en/stable/user_guide/quickstart.html#login) from the `codingame` library.

The script will attempt to read the read the session cookie from the Chrome browser, otherwise manually enter cookie at the prompt.

Pick a folder where the app will download files to.

    python3 ./app.py path/to/where/to/Download/CodinGame

Reuse this file path and the script will optimize by not downloading existing solutions.

## Features

* Uses the CodinGame "API" to search your progress and download your code
* Saves the latest solution for each language, with an appropriate file extension
* Solution files have the filesystem modified date set to the actual time the puzzle was solved
* Creates an `index.html` for each puzzle including puzzle text

### Example queries to run on code database

```powershell
function info($f) {
  $a = $f.FullName.split('\')
  [array]::Reverse($a)
  $null, $t, $n, $null = $a

  $f.LastWriteTime.ToString("yyyy-MM-dd")
  $f.BaseName.PadLeft(10)
  $n.PadRight(9)
  $t
}

gci -file -recurse . | `
  where Extension -ne .html | `
  sort LastWriteTime | `
  % { (info $_) -join " " }
```
