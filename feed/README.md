# RSS Feed

Cloud function that polls CodinGame and publishes RSS feed: https://download-codingame.appspot.com.storage.googleapis.com/recent/feed.rss

## Deploying

```bash
$ cd functions
$ npm run deploy
```

## Testing

```bash
$ cd functions
$ npm run
> scheduledFunction()
```

Then check the updated https://download-codingame.appspot.com.storage.googleapis.com/recent/feed.rss content.

- [ ] Figure out how to get the RSS file to only print to stdout
