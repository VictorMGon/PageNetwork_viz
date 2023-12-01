from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.utils.timezone import localtime
from .models import Page,Link
from crochet import setup
import scrapy

setup()


process = None

class TestSpider(scrapy.Spider):
    name = "testspider"
    custom_settings = {
        "DEPTH_LIMIT":1,
        "DEPTH_PRIORITY":1
    }
    start_urls = []

    def parse(self, response):
        cur_page = Page.objects.filter(url=response.url)
        url_list = response.css("a::attr(href)").getall()
        for url in url_list:
            if not(Page.objects.filter(url=response.urljoin(url)).exists()):
                p = Page()
                p.url = response.urljoin(url)
                p.scrapped = False
                p.date_scrapped = localtime()
                p.save()
                l = Link()
                l.source_page = cur_page.get()
                l.target_page = p
                l.save()
                yield scrapy.Request(response.urljoin(url), self.parse)


@shared_task()
def run_spider():
    process = CrawlerProcess(get_project_settings())
    TestSpider.start_urls = list(Page.objects.filter(scrapped=False).values_list('url', flat=True))
    process.crawl(TestSpider)