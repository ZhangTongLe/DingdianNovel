from .sql import SQL
from DingdianNovel.items import DingdiannovelItem

class DingdianPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, DingdiannovelItem):
            name_id = item['name_id']
            ret = SQL.select_name(name_id)
            if ret[0] == 1:
                print('already existd')
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                SQL.insert_dd_name(xs_name, xs_author, category, name_id)
                print('开始存小说标题')