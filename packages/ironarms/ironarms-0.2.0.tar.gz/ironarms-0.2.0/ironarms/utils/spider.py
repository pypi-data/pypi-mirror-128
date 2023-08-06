__all__ = ["tables_from_spider"]


def tables_from_spider(spider):
    """Returns tables, e.g. models, used in the spider.

    According to the attribute ``iron_items``and ``iron_models`` of ``spider``.

    Returns
    ---------
    list
    """
    lst = []
    if hasattr(spider, "iron_items"):
        items = spider.iron_items
        if not isinstance(items, (tuple, list)):
            items = [items]
        for item in items:
            try:
                lst.append(item._model_cls)
            except AttributeError:
                pass
    if hasattr(spider, "iron_models"):
        models = spider.iron_models
        if not isinstance(models, (tuple, list)):
            models = [models]
        lst.extend(models)
    lst = list(set(lst))
    return lst
