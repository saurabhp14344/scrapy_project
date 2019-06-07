import scrapy

class GoodReads(scrapy.Spider):
    #identity
    name = 'goodreads'

    #request

    def start_requests(self):
        url = 'https://www.goodreads.com/quotes?page=1'

        yield scrapy.Request(url=url, callback=self.parse)

    #respone

    def parse(self, response):
        for quote in response.selector.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//div[@class='quoteText']/text()").extract_first(),
                'author': quote.xpath(".//span[@class='authorOrTitle']/text()").extract_first(),
                'tags': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract()
            }
        next_page = response.selector.xpath("//a[@class='next_page']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)