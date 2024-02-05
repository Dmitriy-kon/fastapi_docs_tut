import asyncio

import httpx

from fastapi import APIRouter


DEFAULT_SUBREDDITS = ["memes", "ProgrammerHumor", "GymMemes"]

router = APIRouter(tags=["async_httpx"])


def get_reddit_top_sync_httpx(subreddit: str) -> list:
    response = httpx.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limi",
            headers={"User-Agent": "Mozilla/5.0"},
    )
    subreddit_memes = response.json()
    
    subreddit_data = []
    for entry in subreddit_memes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{score}: {title} ({link})")
    return subreddit_data[:5]

async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limi",
            headers={"User-Agent": "Mozilla/5.0"},
        )
    subreddit_memes = response.json()

    subreddit_data = []
    for entry in subreddit_memes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{score}: {title} ({link})")
    return subreddit_data[:5]


async def get_tasks():
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(get_reddit_top_async(subreddit))
            for subreddit in DEFAULT_SUBREDDITS
        ]

    results = {name: res.result() for res, name in zip(tasks, DEFAULT_SUBREDDITS)}
    return results

def get_tasks_sync():
    results = {
        name: get_reddit_top_sync_httpx(subreddit) for name, subreddit in zip(DEFAULT_SUBREDDITS, DEFAULT_SUBREDDITS)
    }
    return results

@router.get("/reddit_top/")
async def get_reddit_top(subreddit: str = "memes") -> dict:
    res = await get_tasks()
    return res

@router.get("/reddit_top_sync/")
def get_reddit_top_sync(subreddit: str = "memes") -> dict:
    res = get_tasks_sync()
    return res