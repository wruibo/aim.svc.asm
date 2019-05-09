"""
    field
"""
from venus.orm import model, field, db
from . import config


# setup database
def setup(mode):
    """
        setup database service
    :param mode: str, dev/test/online
    :return:
    """
    db.setup('arm', 'mysql', **config.DATABASES['arm'][mode])


# tb_config_group
class ConfigGroup(model.Model):
    __table__ = 'tb_config_group'

    id = field.AutoField()
    code = field.StringField(max_length=32)
    name = field.StringField(max_length=32)
    brief = field.StringField(default='')
    ctime = field.IntegerField()
    mtime = field.IntegerField()


# tb_config
class Config(model.Model):
    __table__ = 'tb_config'

    id = field.AutoField()
    group_id = field.IntegerField()
    gcode = field.StringField(max_length=32)
    code = field.StringField(max_length=32)
    name = field.StringField(max_length=32)
    value = field.StringField()
    format = field.StringField(max_length=16, default='text')
    ctime = field.IntegerField()
    mtime = field.IntegerField()


# tb_news_category
class NewsCategory(model.Model):
    __table__ = 'tb_news_category'

    id = field.AutoField()
    code = field.StringField(max_length=16)
    name = field.StringField(max_length=16)
    brief = field.StringField(max_length=64, default='')
    order = field.IntegerField(default=0)
    disabled = field.BooleanField(default=True)
    ctime = field.IntegerField()
    mtime = field.IntegerField()


# tb_news
class News(model.Model):
    __table__ = 'tb_news'

    id = field.AutoField(primary_key=True)
    category_id = field.IntegerField()
    code = field.StringField(max_length=32)
    title = field.StringField(max_length=64)
    brief = field.StringField()
    body = field.StringField()
    images = field.StringField(null=True)
    tags = field.StringField(null=True)
    source = field.StringField(max_length=16, null=True)
    site = field.StringField(max_length=16)
    sid = field.StringField(max_length=32)
    disabled = field.BooleanField(default=True)
    ptime = field.IntegerField()
    ctime = field.IntegerField()
    mtime = field.IntegerField()


# tb_news
class NewsList(model.Model):
    __table__ = 'tb_news'

    id = field.AutoField(primary_key=True)
    code = field.StringField(max_length=32)
    title = field.StringField(max_length=64)
    brief = field.StringField()
    images = field.StringField(null=True)
    disabled = field.BooleanField(default=True)
    ptime = field.IntegerField()
    ctime = field.IntegerField()
    mtime = field.IntegerField()
