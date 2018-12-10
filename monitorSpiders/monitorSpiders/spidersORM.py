from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

engine = create_engine("mysql+pymysql://root:123456@10.25.116.62:3306/monitor")
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/monitor")
metadata = MetaData(engine)
DBSession = sessionmaker(bind=engine)

# 获取数据库中已经存在的表结构，声明为一个sqlalchemy的Table类
Table('SpiderDB_article', metadata, autoload=True)
Table('SpiderDB_author', metadata, autoload=True)
Table('SpiderDB_source', metadata, autoload=True)

metadata.create_all(engine)

# sqlalchemy的自动映射，通过metadata来获取所有已经声明了的Table类
Base = automap_base(metadata=metadata)
Base.prepare()

# 定义和数据库表自动映射的sqlalchemy类
Article = Base.classes.SpiderDB_article
Author = Base.classes.SpiderDB_author
Source = Base.classes.SpiderDB_source
