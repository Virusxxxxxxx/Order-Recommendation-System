# OrderRecommendationSystemBackend

    |项目根目录
    |----dao 数据持久层
    |----dataStructure 项目中使用到的数据结构
        |----requestDomain.py pydantic数据验证文件
        |----sqlDomain.py 数据库表结构文件
    |----rest REST api 文件
    |----utils 小工具
        |----validateUtil.py 验证用户登录相关工具
        |----itemCF.py 基于物品的协同过滤
    |----app.py 项目主文件
    |----fake_data.py 生成假数据 (users, meals, comments)
    |----requirement.txt 环境配置文件
    |----system.db sqlite数据库文件
    
app.py 中，```@app.post("/register")```为*函数路由*，下方 ```async def register(user: User):```为*函数内容*

## 查看API文档：

1、```python app.py```

2、访问```http://127.0.0.1:8000/docs```
   
