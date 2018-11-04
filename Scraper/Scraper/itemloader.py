from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst

def number_loader(self,value):
    for v in value:
        yield int(v.replace(",",""))

class MinimalItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    genere_out = Identity()
    main_character_out = Identity()

    chapters_count_in = number_loader
    word_count_in = number_loader
    review_count_in = number_loader
    fav_count_in = number_loader
    follow_count_in = number_loader
    publish_date_in = number_loader
    update_date_in = number_loader
    
    def completion_status_in(self,value):
        return [True]
