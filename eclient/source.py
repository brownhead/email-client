class Source:
	def __init__(self):
		self.config = None

	def set_config(self, config):
		"""config should be some dict"""
		self.config = config

	def sync(self):
		"""returns list of DSFSDF, is a coroutine"""
		pass

import feedparser, pprint, asyncio, aiohttp
class FeedSource(Source):
	@asyncio.coroutine
	def sync(self, metadata):
		future_raw_results = yield from aiohttp.request('GET', self.config["uri"])

		chunks = yield from future_raw_results.read()
		raw_results = feedparser.parse(chunks)

		# Detect the new shit
		result_ids = {i["id"] for i in raw_results["entries"]}
		new_ids = result_ids - metadata.get("received", set())

		# Record the new shit
		if "received" not in metadata:
			metadata["received"] = result_ids
		else:
			metadata["received"] |= result_ids


		results_by_id = {i["id"]: i for i in raw_results["entries"]}
		results = []
		for i in new_ids:
			entry = results_by_id[i]
			results.append({
				"title": entry["title"],
				"published": entry["published_parsed"],
				"summary": entry["summary"],
			})

		print(len(results))
		return results

glar = "http://www.reddit.com/message/inbox/.rss?feed=96014f6490c1cfab32a3e899a5eb4caf2e111ca9&user=brownhead"
x = FeedSource()
metadata = {}
x.set_config({"uri": glar})

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(x.sync(metadata))
finally:
    loop.close()

# foo(x.sync(metadata))
# foo(x.sync(metadata))

# datastore = defaultdict(list)

# def store(uri, entries):
# 	datastore[uri].append(entries)
