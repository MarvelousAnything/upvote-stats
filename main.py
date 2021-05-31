import asyncio
import matplotlib.pyplot as plt
import asyncpraw

# plt.ion()
# plt.interactive(True)
# fig, axarr = plt.subplots(1)
# axarr.pie([50, 50], autopct='%1.1f%%')
# axarr.set_position([0.25, 0.4, .5, .5])

global reddit, uppy


async def init():
    global reddit, uppy
    reddit = asyncpraw.Reddit("upvote_stats")
    user = await reddit.redditor('')
    uppy = user.upvoted(limit=None)


subs = {}


async def update_subs_dict():
    async for up in uppy:
        sub = await reddit.submission(up)
        subreddit = str(sub.subreddit)
        print(f"Got post: \"{sub.title}\" by {sub.author} from {subreddit}")
        if subreddit in subs.keys():
            subs[subreddit] += 1
        else:
            subs[subreddit] = 1


async def do_update_chart(_subs):
    sorted_subs = {key: value for (key, value) in sorted(_subs.items(), key=lambda x: x[1], reverse=True)}
    print(repr(sorted_subs))
    # axarr.clear()
    # axarr.pie(sorted_subs.values(), labels=sorted_subs.keys(), autopct='%1.1f%%')
    # fig.canvas.draw_idle()
    # try:
    #     plt.table(cellText=[[str(x), str(y)] for x, y in sorted_subs.items()], colLabels=["Subreddit", "Upvote Count"], loc="bottom")
    # except IndexError:
    #     pass
    # plt.pause(2)
    # plt.draw()


async def update_chart(_subs):
    while True:
        await asyncio.sleep(15)
        print("Updating chart...")
        await do_update_chart(_subs)
        print("Chart updated!")


loop = asyncio.get_event_loop()


async def do_tasks():
    tasks = [loop.create_task(update_subs_dict(), name="update_subs_dict"),
             loop.create_task(update_chart(subs), name="update_chart")]
    await asyncio.gather(*tasks)


loop.run_until_complete(init())
loop.run_until_complete(do_tasks())
loop.close()
print(repr(subs))
