## 设计初衷

```

python setup.py sdist bdist_wheel
twine upload dist/*

SpiderKo依赖统一的状态管理数据库（Redis、ZooKeeper），SpiderKo采用二分搜索定位网页路由，
SpiderKo存储提供Elasticsearch、MongoDB、MySQL（sqlalchemy）为存储载体。


爬虫(spider) ---> 数据治理(process) ---> 数据存储（rpc、db、http） store

可以快速接入 无需关心数据存储

所有爬虫写入   日本爬虫可以直接用   异步任务调用  下载  通知
```