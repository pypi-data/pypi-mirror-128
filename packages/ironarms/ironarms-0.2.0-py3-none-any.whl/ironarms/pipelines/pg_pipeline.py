# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from ironarms import utils

__all__ = ["PGPipeline"]


class PGPipeline(object):
    """Saves items to corresponding pg tables.

    The corresponding pg table is located by comparing the name of the item class with
    the name of the model class, then the table name.  :meth:`process_item`

    **Usages**

    ``settings.py``::

        import ironarms

        ITEM_PIPELINES = {
            "ironarms.pipelines.PGPipeline": 500,
        }

        # uncomment the DATABASE_URL to override the DATABASE
        # DATABASE_URL = os.environ["DATABASE_URL"]
        DATABASE = {
            "drivername": "postgresql",
            "host": os.environ["PG_HOST"],
            "port": os.environ["PG_PORT"],
            "username": os.environ["PG_USER"],
            "password": os.environ["PG_PASSWORD"],
            "database": os.environ["PG_DB"],
        }

        # a list of sqlalchemy models,
        #   which will be created if not exists in the database
        #   when ironarms.pipelines.PGPipeline open_spider
        # attributes iron_items and iron_models of a spider would be used by
        #   ironarms.pipelines.PGPipeline too
        DATA_TABLES = []

    """

    def __init__(self, db_url, db_tables):
        self.db_url = db_url
        self.db_tables = db_tables

    @classmethod
    def from_crawler(cls, crawler):
        """Returns an instance of :class:`PGPipeline` with settings of the ``crawler``.

        Method required by scrapy.
        """
        db_url = utils.get_db_url(settings=crawler.settings)
        if db_url is None:
            raise ValueError("no database url.")
        # print(f'DATABASE_URL: {db_url}')
        db_tables = crawler.settings.get("DATA_TABLES", [])
        return cls(db_url=db_url, db_tables=db_tables)

    def open_spider(self, spider):
        """Create a session and make sure related tables exist.

        :attr:`db_tables` would be updated if there is any new tables found from the
        spider instance.
        """
        tbls = [x for x in utils.tables_from_spider(spider) if x not in self.db_tables]
        self.db_tables.extend(tbls)
        self.session = utils.create_session(self.db_url, ensure_tables=self.db_tables)

    def close_spider(self, spider):
        """commit and save all items to DB when spider finished scraping."""
        utils.close_session(self.session)

    def process_item(self, item, spider):
        """Save item to database.

        Locates proper pg table of ``item``, and saves it to the pg table, drops if
        exists already, or no target table found.
        """
        tbl = self.locate_table(item)
        if tbl is None:
            raise DropItem(f"no table for item: {item}")
        utils.add_via_session(tbl(**item), session=self.session)

    def locate_table(self, item):
        """Locates the corresponding table, e.g. model, of the item.

        Returns
        --------
        Model, or None
        """
        try:
            return item._model_cls
        except AttributeError:
            pass
        item_name = item.__class__.__name__.replace("Item", "")
        for tbl in self.db_tables:
            tbl_name = (
                tbl.__class__.__name__.replace("Table", "")
                .replace("Tbl", "")
                .replace("Model", "")
            )
            if tbl_name == item_name or tbl.__tablename__ == item_name:
                return tbl
        return None
