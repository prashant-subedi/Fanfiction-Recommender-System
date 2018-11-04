import scrapy
import re
from collections import OrderedDict
from Scraper.items import MinimalScraperItem
from Scraper.itemloader import MinimalItemLoader
from w3lib.html import remove_tags

NUMBER = "\d+(?:,\d{3})*"

class MinimalSpider(scrapy.Spider):

    name = "minimal"
    
    # THE DICT OF REGEX IS NECESSEARY TO PARSE STATUS OF EACH FIC 
    status_regex = OrderedDict()
    status_regex["rating"]=re.compile(r"Rated:\s*(K|K+|T|M)")
    status_regex["language"]=re.compile(r"(\w+)")
    status_regex["genere"]=re.compile(r"(Angst|Crime|Drama|Family|Fantasy|Friendship|General|Horror|Humor|Hurt/Comfort|Mystery|Parody|Poetry|Romance|Sci-Fi|Spiritual|Supernatural|Suspense|Western)")
    status_regex["chapters_count"]=re.compile(r"Chapters:\s*(%s)"%NUMBER)
    status_regex["word_count"]=re.compile(r"Words:\s*(%s)"%NUMBER)
    status_regex["review_count"]=re.compile(r"Reviews:\s*(%s)"%NUMBER)
    status_regex["fav_count"]=re.compile(r"Favs:\s*(%s)"%NUMBER)
    status_regex["follow_count"]=re.compile(r"Follows:\s*(%s)"%NUMBER)
    status_regex["update_date"]=re.compile(r"Updated: <span data-xutime=\"(\d+)\">")
    status_regex["publish_date"]=re.compile(r"Published: <span data-xutime=\"(\d+)\">")
    status_regex["main_characters"]=re.compile("(?!Completed).*")
    status_regex["completion_status"]=re.compile("Complete")
    
    def start_requests(self):
        urls = [
            'https://www.fanfiction.net/book/Harry-Potter/'
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        # For each story in the list
        for story in  response.css("div.z-list"):

            item_loader   = MinimalItemLoader(MinimalScraperItem(),story)
            fanfic_name,author = story.css("a::text").extract()[0:2]
            fanfic_id = story.xpath("""a[@class='stitle']/@href""").re("s/(\d+)")
            author_id = story.xpath("""a/@href""").re("u/(\d+)")

            item_loader.add_value("fanfic_id",fanfic_id)
            item_loader.add_value("author_id",author_id)
            item_loader.add_value("fanfic_name",fanfic_name)
            item_loader.add_value("author",author)
            
            
         
            item_loader.add_css("summary","div.z-padtop::text")
            status_selector = story.css("div.xgray").get()[len('<div class="z-padtop2 xgray">'):]
            
            feilds = status_selector.split(" - ")[::-1]
            entry = feilds.pop()
            for k,v  in self.status_regex.items():
                data = v.findall(entry)
                if data:
                    item_loader.add_value(k,data)
                    try:
                        entry = feilds.pop()
                    except IndexError:
                        break


                

            yield item_loader.load_item()
        next = response.xpath("""//center[@style="margin-top:5px;margin-bottom:5px;"]/a[contains(.,'Next')]/@href""").get() 
        if next is not None:
            yield response.follow(next,callback=self.parse)
