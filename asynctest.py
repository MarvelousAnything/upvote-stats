import asyncio
import asyncpraw

subs = {}


async def init():
    async with asyncpraw.Reddit("upvote_stats") as reddit:
        user = await reddit.redditor('')
        async for up in user.upvoted():
            sub = await reddit.submission(up)
            subreddit = str(sub.subreddit)
            if subreddit in subs.keys():
                subs[subreddit] += 1
            else:
                subs[subreddit] = 1
            print(repr({key: value for (key, value) in sorted(subs.items(), key=lambda x: x[1], reverse=True)}))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.close()

