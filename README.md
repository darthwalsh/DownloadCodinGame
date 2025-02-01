# Download CodinGame

Download all your CodinGame solutions to your computer!

* Uses the CodinGame "API" to search your progress and download your code
* Saves the latest solution for each language, with an appropriate file extension
* Solution files have the filesystem modified date set to the actual time the puzzle was solved
* Creates an `index.html` for each puzzle including puzzle text

## Setup

```bash
git clone https://github.com/darthwalsh/DownloadCodinGame.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run

`python3 ./app.py -h`

shows help.

### Download through CodinGame unofficial API to a local folder

Follow [login instructions](https://codingame.readthedocs.io/en/stable/user_guide/quickstart.html#login) from the `codingame` library.

The script will attempt to read the read the session cookie from the Chrome browser, otherwise manually enter cookie at the prompt.

Pick a folder where the app will download files to:

`python3 ./app.py download path/to/where/to/Download/CodinGame`

*Reuse this folder path and the script will skip downloading old solutions.*


### List of each solution

*The rest of these commands will load from the downloaded folder.*

`python3 ./app.py list path/to/Downloaded/CodinGame`

```
2015-10-17         C# tutorial  onboarding
2015-10-18         C# easy      power-of-thor-episode-1
2015-10-18         C# codegolf  power-of-thor
2015-10-18         C# easy      temperatures
2015-10-18         C# easy      mars-lander-episode-1
2015-10-19         C# medium    mars-lander-episode-2
...
```

### Monthly summaries of difficulty and languages

`python3 ./app.py monthly path/to/Downloaded/CodinGame`

```
2022-01-01   8 easy, 2 medium                         6 Python3, 3 C++, 1 C
2022-02-01   20 medium, 8 easy                        18 Python3, 9 C++, 1 TypeScript
2022-03-01   8 medium, 6 easy, 1 hard                 10 Python3, 2 C, 2 C++, 1 Javascript
...
```

### CSV report

`python3 ./app.py csv path/to/Downloaded/CodinGame`

```csv
id,difficulty,url,last_date,Javascript,Python3,C,C#,C++,TypeScript
mars-lander-episode-2,medium,https://www.codingame.com/ide/puzzle/mars-lander-episode-2,2015-10-19,,,,2015-10-19,,
there-is-no-spoon-episode-1,medium,https://www.codingame.com/ide/puzzle/there-is-no-spoon-episode-1,2015-10-19,,,,2015-10-19,,
shadows-of-the-knight-episode-1,medium,https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-1,2015-10-19,,,,2015-10-19,,
...
```

# TODO

- [ ] [Progress bar](https://chatgpt.com/share/679e360d-fb08-8011-b74d-a1dd3367a353) showing remaining progress
