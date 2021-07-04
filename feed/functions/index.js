const functions = require("firebase-functions");

const recentPuzzles = require("../index");

exports.scheduledFunction = functions.pubsub.schedule("every 4 hours").onRun(async context => {
  // TODO does it work?
  const puzzles = await recentPuzzles();
  for (const p of puzzles) {
    const {level, title, url, created} = p;
    console.log(created, level, title, url);
  }
});

