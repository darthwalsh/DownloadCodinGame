const functions = require("firebase-functions");
const Feed = require("feed").Feed;

const recentPuzzles = require("../index");

const refreshHours = 4;

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

  console.log();
  console.log(feed.rss2());
});
