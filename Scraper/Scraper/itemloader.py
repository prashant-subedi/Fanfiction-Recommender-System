from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst
import re
from w3lib.html import remove_tags

def number_loader(self,value):
    for v in value:
        yield int(v.replace(",",""))

class MinimalItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    pairings_regex = re.compile(r'\[.*?\]')
    character_regex = re.compile(r'\w[\w\s]*\w\.?')
    genere_out = Identity()

    chapters_count_in = number_loader
    word_count_in = number_loader
    review_count_in = number_loader
    fav_count_in = number_loader
    follow_count_in = number_loader
    publish_date_in = number_loader
    update_date_in = number_loader
    
    def completion_status_in(self,value):
        return [True]

    def  main_characters_out(self,value):
        v = remove_tags(value[0])
        characters = []
        pairings = self.pairings_regex.findall(v)
        for pairing in pairings:
            v = v.replace(pairing,"")
            characters.extend(self.character_regex.findall(pairing))
    
        characters.extend(self.character_regex.findall(v))
        
        return characters
