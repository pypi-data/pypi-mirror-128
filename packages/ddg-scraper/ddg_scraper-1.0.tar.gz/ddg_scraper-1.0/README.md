
# Asynchronous and Synchronous DuckDuckGo Search Engine Scraper

Scrapes the [duckduckgo](duck.com) search engine.

# Asynchronous Example
```py
from ddg_scraper import asearch
import asyncio


async def main():
    results = await asearch("Python")
    async for result in results:
        ...

asyncio.run(main())
```

# Synchronous Example
```py
from ddg_scraper import search


results = search("Python")
for result in results:
    ...
```

In both examples, `result` is [`ddg_scraper.Result`](ddg_scraper/_dataclasses.py)

# Attributes and Methods of [`ddg_scraper.Result`](ddg_scraper/_dataclasses.py)

Attributes

- `title`
- `description`
- `url`
- `icon_url`

Methods

- `as_dict()`
    - Converts the dataclass to a `dict` object and returns it.