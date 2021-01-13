"""
  Run with py ./app.py /Users/you/path/to/where/to/Download/CodinGame 
"""

import json
import os
import re
import requests
import sys
from os import path

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

def api(service, body):
  response = session.post(f'https://www.codingame.com/services/{service}', json=body)
  if response.ok:
    return response.json()
  print(service, body, response.status_code)
  raise ValueError(response.text) 


def login():
  with open(path.expanduser("~/.dcg/config.json"), 'r') as f:
    config = json.load(f)
  return api('CodingamerRemoteService/loginSiteV2', [config["email"], config["pw"], True])['success']['userId']

def get_levels(user_id):
  levels = {}
  for l in api("Puzzle/findAllMinimalProgress", [user_id]):
    levels.setdefault(l['level'], []).append(l)
  return levels

def load_code(difficulty, levels):
  print(f'Starting {difficulty}...')
  level_ids = [level['id'] for level in levels]
  findProgressByIds = api('Puzzle/findProgressByIds', [level_ids, user_id, 2])
  level_details = {progress['id']:progress for progress in findProgressByIds}
    
  for level in levels:
    level_detail = level_details[level['id']]
    pretty_id = level_detail['prettyId']
    folder = path.join(dcg_path, difficulty, re.sub('[^a-zA-Z0-9_-]', '_', pretty_id))
    os.makedirs(folder, exist_ok=True)

    findProgressByPrettyId = api('Puzzle/findProgressByPrettyId', [pretty_id, user_id])
    readme_file = code_file = path.join(folder, 'index.html')
    with open(readme_file, 'w') as f:
      f.write(f"<h1>{findProgressByPrettyId['title']}</h1>\n\n")
      href = f"https://www.codingame.com" + findProgressByPrettyId['detailsPageUrl']
      f.write(f'<a href="{href}">{href}</a>\n\n')
      f.write(findProgressByPrettyId['statement'])
  
    by_lang = {}
    try:
      solutions = api('Solution/findMySolutions', [user_id,level['id'],None])
    except ValueError as e:
      print(f'Skipping {pretty_id}')
      print(e)
      continue
    for s in solutions:
      time = s['creationTime']
      lang = s['programmingLanguageId']
      if lang not in by_lang or time > by_lang[lang]['creationTime']:
        by_lang[lang] = s

    for lang, s in by_lang.items():
      solution = api('Solution/findSolution', [user_id,s['testSessionQuestionSubmissionId']])
      extension = extensions.get(lang.lower(), "txt")
      code_file = path.join(folder, f'{lang}.{extension}')

      with open(code_file, 'w') as f:
        f.write(solution['code'])

      time = s['creationTime'] // 1000
      os.utime(code_file, (time, time))
      
      print(code_file)
         

def main():
  global session, user_id, dcg_path

  _, dcg_path = sys.argv # dcg_path is where to write all your solutions

  session = requests.Session()

  user_id = login()

  all_levels = get_levels(user_id)

  for name, levels in all_levels.items():
    load_code(name, levels)

if __name__ == "__main__":
    main()
