# The Scrapy project

- [`spiders`](./spiders): folder that contains all spiders of the project
- [`items.py`](./items.py): defines the different items that we will scrape from the site
- [`pipelines.py`](./pipelines.py): defines the pipelines of the project. Consider them as post-processing
unites that can be chained together.
- [`settings.py`](./settings.py): the scraping settings. Here you can configure things like a http cache, the download
delay and much more.