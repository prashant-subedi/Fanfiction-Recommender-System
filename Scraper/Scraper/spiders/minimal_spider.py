import scrapy
import re
from collections import OrderedDict
from Scraper.items import MinimalScraperItem
from Scraper.itemloader import MinimalItemLoader

NUMBER = "\d+(?:,\d{3})*"

class MinimalSpider(scrapy.Spider):

    name = "minimal"
    status_regex = OrderedDict()
    status_regex["rating"]=re.compile(r"Rated:\s*(K|K+|T|M)")
    status_regex["language"]=re.compile(r"(Afrikaans|Bahasa Indonesia|Bahasa Melayu|Dansk|Deutsch|Eesti|English|Español|Esperanto|Filipino|Français|Italiano|Język polski|LINGUA LATINA|Magyar|Nederlands|Norsk|Português|Română|Shqip|Suomi|Svenska|Tiếng Việt|Türkçe|čeština|Русский|עברית|देवनागरी|ਪੰਜਾਬੀ|ภาษาไทย|中文|日本語)")
    status_regex["genere"]=re.compile(r"(Angst|Crime|Drama|Family|Fantasy|Friendship|General|Horror|Humor|Hurt/Comfort|Mystery|Parody|Poetry|Romance|Sci-Fi|Spiritual|Supernatural|Suspense|Western)")
    status_regex["chapters_count"]=re.compile(r"Chapters:\s*(%s)"%NUMBER)
    status_regex["word_count"]=re.compile(r"Words:\s*(%s)"%NUMBER)
    status_regex["review_count"]=re.compile(r"Reviews:\s*(%s)"%NUMBER)
    status_regex["fav_count"]=re.compile(r"Favs:\s*(%s)"%NUMBER)
    status_regex["follow_count"]=re.compile(r"Follows:\s*(%s)"%NUMBER)
    status_regex["update_date"]=re.compile(r"Updated: <span data-xutime=\"(\d+)\">")
    status_regex["publish_date"]=re.compile(r"Published: <span data-xutime=\"(\d+)\">")
    status_regex["main_characers"]=re.compile("(?!Complete).*")
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
            fic_name,author = story.css("a::text").extract()[0:2]

            item_loader.add_value("fanfic_name",fic_name)
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
                    
