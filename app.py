"""
  Run with py ./app.py /Users/you/path/to/where/to/Download/CodinGame 
"""

import os
import re
import sys
from os import path

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

  def __init__(self, client, dcg_path):
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

    print(f'Starting {difficulty}...')
    level_ids = [level['id'] for level in levels]
    findProgressByIds = self.client.request('Puzzle', 'findProgressByIds', [level_ids, self.user_id, 2])
    level_details = {progress['id']: progress for progress in findProgressByIds}

    for level in levels:
      level_detail = level_details[level['id']]
      pretty_id = level_detail['prettyId']
      folder = path.join(self.dcg_path, difficulty, re.sub('[^a-zA-Z0-9_-]', '_', pretty_id))
      os.makedirs(folder, exist_ok=True)

      findProgressByPrettyId = self.client.request('Puzzle', 'findProgressByPrettyId', [pretty_id, self.user_id])
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

        print(code_file)

def get_cookie():
  cj = browser_cookie3.chrome()
  rememberMe = next((c for c in cj if 'codingame' in c.domain and c.name == 'rememberMe'), None)
  if rememberMe:
    return rememberMe.value
  return input('Session cookie from: https://codingame.com -> devtools -> Cookies -> rememberMe\n: ')

def main(dcg_path):
  client = codingame.Client()
  client.login(remember_me_cookie=get_cookie())
  puzzles = PuzzleClient(client, dcg_path)

  all_levels = puzzles.get_levels()

  for name, levels in all_levels.items():
    puzzles.load_code(name, levels)

if __name__ == '__main__':
  _, dcg_path = sys.argv  # dcg_path is where to write all your solutions
  main(dcg_path)
