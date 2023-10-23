import csv
import datetime
from collections import defaultdict
from scrapy.exceptions import DropItem

from .constants import BASE_DIR, FORMAT_DATE


class PepParsePipeline:
    def open_spider(self, spider):
        self.status = defaultdict()

    def process_item(self, item, spider):
        if 'status' not in item:
            raise DropItem('Статус отсутствует')
        self.status['status'] = self.status.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        result_dir = BASE_DIR / 'results'
        result_dir.mkdir(exist_ok=True)
        date = datetime.datetime.now().strftime(FORMAT_DATE)
        result = (('Статус', 'Количество'),
                  *self.status.items(),
                  ('Total', sum(self.status.values())))
        with open(
                result_dir / f'status_summary_{date}.csv',
                mode='w',
                encoding='utf-8'
        ) as file:
            writer_csv = csv.writer(file)
            writer_csv.writerow(result)
