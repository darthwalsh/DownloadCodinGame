const fetch = require("node-fetch");

async function api(endpoint, body) {
  const method = "POST";
  console.error(method, endpoint, body);
  const res = await fetch(`https://www.codingame.com/services/${endpoint}`, {
    method,
    headers: {
      accept: "application/json, text/plain, */*",
    },
    body: JSON.stringify(body),
  });

  console.error(res.status);
  return res.json();
}

async function run() {
  const minimalProgress = await api("Puzzle/findAllMinimalProgress", [null]);
  console.log("Got", minimalProgress.length, "puzzles");

  const top = minimalProgress.sort((a, b) => b.creationTime - a.creationTime).slice(0, 10);

  const details = await api("Puzzle/findProgressByIds", [
    top.map((p) => p.id),
    null,
    2,
  ]);

  console.error(details.sort((a, b) => b.creationTime - a.creationTime))
  for (const p of details) {
    // Could do more with Topics, Description, Cover banner, Contributor, XP, etc.
    const { level, title, detailsPageUrl, type, creationTime } = p;
    const url = `https://www.codingame.com${detailsPageUrl}`;
    console.error(new Date(creationTime), type, level, title);
    console.error(url);
    console.error();
  }
}

run();
