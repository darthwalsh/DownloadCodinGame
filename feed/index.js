const debug = require("debug");
const fetch = require("node-fetch");

const log = debug("downloadcodingame");

/**
 * @typedef {Object} Puzzle
 * @property {number} id - immutable ID
 * @property {string} title - i.e. name of the puzzle
 * @property {Date} created - when puzzle created TODO UTC?
 * @property {string} level - i.e. easy/hard
 * @property {string} url - codingame.com puzzle details
 */

async function api(endpoint, body) {
  const method = "POST";
  log(method, endpoint, body);
  const res = await fetch(`https://www.codingame.com/services/${endpoint}`, {
    method,
    headers: {
      accept: "application/json, text/plain, */*",
    },
    body: JSON.stringify(body),
  });

  log(res.status);
  return res.json();
}

/** @returns {Promise<Puzzle[]>} */
async function run() {
  const minimalProgress = await api("Puzzle/findAllMinimalProgress", [null]);

  const top = minimalProgress.sort((a, b) => b.creationTime - a.creationTime).slice(0, 10);

  const details = await api("Puzzle/findProgressByIds", [top.map(p => p.id), null, 2]);

  return details
    .sort((a, b) => b.creationTime - a.creationTime)
    .map(p => {
      // Could do more with Topics, Description, Cover banner, Contributor, Type, XP, etc.
      const {id, level, title, detailsPageUrl, creationTime} = p;
      const created = new Date(creationTime);
      const url = `https://www.codingame.com${detailsPageUrl}`;
      return {id, title, created, level, url};
    });
}

async function main() {
  const puzzles = await run();
  for (const p of puzzles) {
    const {level, title, url, created} = p;
    console.log(created, level, title, url);
  }
}

if (require.main === module) {
  main();
}

module.exports = run;
