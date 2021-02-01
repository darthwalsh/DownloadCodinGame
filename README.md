# Download CodinGame

Download all your CodinGame solutions to your computer!

## Setup

Create file `~/.dcg/config.json`

    { "email": "your@gmail.com",  "pw": "yourPW" }

*If you use OAuth to sign in to codingame, then you can use the reset password link to create your password.*

## Run

Pick a folder where the app will write. Run with:

    python3 ./app.py path/to/where/to/Download/CodinGame

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
