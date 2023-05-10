import re
import scrapy


class CrawlSpider(scrapy.Spider):
    name = "crawl"
    allowed_domains = ["127.0.0.1"]
    start_urls = ["http://127.0.0.1:5000/"]

    def parse(self, response):
        print(response.body)
        for url in _extract_ahref_urls(response):
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    # Whether to return the Playright page object; this will prob
                    # be useful for getting raw HTML back in the future
                    # "playwright_include_page": True,
                    "playwright_context": "persistent",
                },
            )


def _extract_ahref_urls(response):
    collected_full_urls = []
    for href in response.css("a::attr(href)"):
        relative_url = href.get()
        # Add the base URL of the current page
        full_url = response.urljoin(relative_url)

        # Avoid following mailto etc
        if re.match(r"^http", full_url):
            collected_full_urls.append(full_url)
    return collected_full_urls
