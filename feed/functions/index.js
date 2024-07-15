const functions = require("firebase-functions");
const admin = require("firebase-admin");
const Feed = require("feed").Feed;

admin.initializeApp();

const bucket = admin.storage().bucket();

async function api(endpoint, body) {
  const method = "POST";
  console.log(method, endpoint, body);
  const res = await fetch(`https://www.codingame.com/services/${endpoint}`, {
    method,
    headers: {
      accept: "application/json, text/plain, */*",
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });

  console.log(res.status);
  return res.json();
}

/**
 * @typedef {Object} Puzzle
 * @property {number} id - immutable ID
 * @property {string} title - i.e. name of the puzzle
 * @property {Date} created - when puzzle created TODO UTC?
 * @property {string} level - i.e. easy/hard
 * @property {string} url - codingame.com puzzle details
 */
/** @returns {Promise<Puzzle[]>} */
async function recentPuzzles() {
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

const refreshHours = 1;
function createFeed() {
  return new Feed({
    title: "DownloadCodinGame Latest Puzzles",
    description: "Recent puzzles from CodinGame https://github.com/darthwalsh/DownloadCodinGame",
    link: "https://www.codingame.com/training",
    language: "en",
    copyright: "See CodinGame ToS",
    ttl: refreshHours * 60,
  });
}

const cron = `every ${refreshHours} hours`;
exports.scheduledFunction = functions.pubsub.schedule(cron).onRun(async () => {
  const feed = createFeed();

  const puzzles = await recentPuzzles();
  for (const p of puzzles) {
    const {id, level, title, url, created} = p;
    console.log(id, created, level, title, url);

    feed.addItem({
      title: `[${level.toLocaleUpperCase()}] ${title}`,
      id,
      link: url,
      date: created,
    });
  }

  const rss = feed.rss2();

  const file = bucket.file("recent/feed.rss");
  await file.save(rss, {public: true});
  console.log("Upload to", file.publicUrl(), "done");
});
