"""
  Run with py ./app.py /Users/you/path/to/where/to/Download/CodinGame 
"""

from collections import Counter
import csv
import os
import re
import sys
from argparse import ArgumentParser
from datetime import datetime
from os import path
import traceback

import browser_cookie3
import codingame

extensions = {
    'bash': 'sh',
    'c': 'c',
    'c#': 'cs',
    'c++': 'cpp',
    'clojure': 'clj',
    'd': 'd',
    'dart': 'dart',
    'f#': 'fs',
    'go': 'go',
    'groovy': 'groovy',
    'haskell': 'hs',
    'java': 'java',
    'javascript': 'js',
    'kotlin': 'kt',
    'lua': 'lua',
    'objectivec': 'm',
    'ocaml': 'ml',
    'pascal': 'pas',
    'perl': 'pl',
    'php': 'php',
    'python3': 'py',
    'ruby': 'rb',
    'rust': 'rs',
    'scala': 'scala',
    'swift': 'swift',
    'typescript': 'ts',
    'vb.net': 'vb',
}

class PuzzleClient:

  def __init__(self, client: codingame.Client, dcg_path: str):
    self.client = client
    self.dcg_path = dcg_path
    self.user_id = client.codingamer.id

  def get_levels(self):
    levels = {}
    for l in self.client.request('Puzzle', 'findAllMinimalProgress', [self.user_id]):
      levels.setdefault(l['level'], []).append(l)
    return levels

  def load_code(self, difficulty, levels):
    if difficulty == 'multi':
      return

    print(f'Starting {difficulty}', end='.')
    level_ids = [level['id'] for level in levels]
    findProgressByIds = self.client.request('Puzzle', 'findProgressByIds', [level_ids, self.user_id, 2])
    level_details = {progress['id']: progress for progress in findProgressByIds}

    for level in levels:
      level_detail = level_details[level['id']]
      pretty_id = level_detail['prettyId']
      folder = path.join(self.dcg_path, difficulty, re.sub('[^a-zA-Z0-9_-]', '_', pretty_id))
      os.makedirs(folder, exist_ok=True)

      findProgressByPrettyId = self.client.request('Puzzle', 'findProgressByPrettyId', [pretty_id, self.user_id])
      print(end='.', flush=True)
      readme_file = code_file = path.join(folder, 'index.html')
      with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(f"<h1>{findProgressByPrettyId['title']}</h1>\n\n")
        href = f'https://www.codingame.com' + findProgressByPrettyId['detailsPageUrl']
        f.write(f'<a href="{href}">{href}</a>\n\n')
        f.write(findProgressByPrettyId['statement'])

      by_lang = {}
      try:
        solutions = self.client.request('Solution', 'findMySolutions', [self.user_id, level['id'], None])
      except codingame.http.httperror.HTTPError as e:
        if e.status_code == 422:
          print()
          print(f'Skipping {pretty_id}')
          print(e)
          continue
        else:
          raise
      for s in solutions:
        time = s['creationTime']
        lang = s['programmingLanguageId']
        if lang not in by_lang or time > by_lang[lang]['creationTime']:
          by_lang[lang] = s

      for lang, s in by_lang.items():
        extension = extensions.get(lang.lower(), 'txt')
        code_file = path.join(folder, f'{lang}.{extension}')
        time = s['creationTime'] // 1000

        try:
          modified = os.stat(code_file).st_mtime
          if int(modified) == time:
            continue
        except FileNotFoundError:
          pass

        solution = self.client.request('Solution', 'findSolution', [self.user_id, s['testSessionQuestionSubmissionId']])
        with open(code_file, 'w', encoding='utf-8') as f:
          f.write(solution['code'])
        os.utime(code_file, (time, time))

        print()
        print(code_file)
    print()
      

def get_cookie():
  try:
    cj = browser_cookie3.chrome()
    rememberMe = next((c for c in cj if 'codingame' in c.domain and c.name == 'rememberMe'), None)
    if rememberMe:
      return rememberMe.value
  except Exception:
    bug_message = "Loading Chrome with browser_cookie3 failed, please report this issue: https://github.com/darthwalsh/DownloadCodinGame/issues/new"
    traceback.print_exc()
    # Maybe use colorize=True, but that requires python 3.13
    print()
    print("!" * len(bug_message))
    print(bug_message)
    print("!" * len(bug_message))
    print()
  return input('Session cookie from: https://codingame.com -> devtools -> Cookies -> rememberMe\n: ')

def download(dcg_path):
  client = codingame.Client()
  client.login(remember_me_cookie=get_cookie())
  puzzles = PuzzleClient(client, dcg_path)

  all_levels = puzzles.get_levels()

  for name, levels in all_levels.items():
    puzzles.load_code(name, levels)

def get_cache(dcg_path):
  return [[(datetime.fromtimestamp(path.getmtime(path.join(root, file))), file.split('.')[0], difficulty, id)
           for file in files
           if not file.endswith('.html')
           for *_, difficulty, id in [root.split(os.sep)]]
          for root, _, files in os.walk(dcg_path)
          if any(not file.endswith('.html') for file in files)]

def listall(dcg_path):
  for modified, lang, difficulty, id in sorted(sol for sols in get_cache(dcg_path) for sol in sols):
    print(f'{modified.date()} {lang:>10} {difficulty:9} {id}')

def monthly(dcg_path):
  buckets = {}
  for sols in get_cache(dcg_path):
    for modified, lang, difficulty, id in sols:
      bylang, bydiff = buckets.setdefault(modified.date().replace(day=1), (Counter(), Counter()))
      bylang[lang] += 1
      bydiff[difficulty] += 1

  def fmt_counter(c):
    return ", ".join(f'{v} {k}' for k, v in sorted(c.items(), key=lambda o: o[1], reverse=True))

  for date, (bylang, bydiff) in sorted(buckets.items()):
    print(date, ' ', fmt_counter(bydiff).ljust(40), fmt_counter(bylang))

def print_csv(dcg_path):
  puzzles = get_cache(dcg_path)
  langs = Counter()
  for sols in puzzles:
    for _, lang, _, _ in sols:
      langs[lang] += 1
  lang_cols = sorted(langs, key=langs.get, reverse=True)

  writer = csv.writer(sys.stdout)
  writer.writerow('id difficulty url last_date'.split() + lang_cols)

  for sols in sorted(puzzles, key=max):
    lang_dates = ['' for _ in lang_cols]

    for modified, lang, difficulty, id in sols:
      lang_dates[lang_cols.index(lang)] = modified.date()
    last_date = max(date for date in lang_dates if date)

    writer.writerow([id, difficulty, f'https://www.codingame.com/ide/puzzle/{id}', last_date] + lang_dates)

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('command', help='Command to run', choices='download list monthly csv'.split())
  parser.add_argument('dcg_path', help='Path to where to download CodinGame')
  args = parser.parse_args()

  if args.command == 'download':
    download(args.dcg_path)
  elif args.command == 'list':
    listall(args.dcg_path)
  elif args.command == 'monthly':
    monthly(args.dcg_path)
  elif args.command == 'csv':
    print_csv(args.dcg_path)
  else:
    raise ValueError(f'Unknown command: {args.command}')
