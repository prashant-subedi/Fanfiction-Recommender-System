# TODO HANDLE PAIRINGS IN main_characters_out function

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst
import re
from w3lib.html import remove_tags

def number_loader(self,value):
    for v in value:
        yield int(v.replace(",",""))

class MinimalItemLoader(ItemLoader):
    # MOST FEILDS ONLY HAVE ONE VALUE
    default_output_processor = TakeFirst()
    genere_out = Identity()

    # REGEX TO HANDLE CHARACTERS
    pairings_regex = re.compile(r'\[.*?\]')
    character_regex = re.compile(r'\w[\w\s]*\w\.?')
    
    # ID IS AN INTEGER
    fanfic_id_in = number_loader
    author_id_in = number_loader
    
    # METRICS ARE INTEGERS
    chapters_count_in = number_loader
    word_count_in = number_loader
    review_count_in = number_loader
    fav_count_in = number_loader
    follow_count_in = number_loader
    
    # WE EXTRACTED EPOCH TIME
    publish_date_in = number_loader
    update_date_in = number_loader

    # COMPLETION STATUS IS A BOOLEAN
    def completion_status_in(self,value):
        return [True]

    # HANDING CHARACTERS REQUIRE A LOT OF REGEX
    def  main_characters_out(self,value):
        v = remove_tags(value[0])
        characters = []
        pairings = self.pairings_regex.findall(v)
        for pairing in pairings:
            v = v.replace(pairing,"")
            characters.extend(self.character_regex.findall(pairing))
    
        characters.extend(self.character_regex.findall(v))
        
        return characters
