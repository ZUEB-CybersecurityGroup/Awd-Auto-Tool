# AWD后门自动利用脚本

## 脚本介绍

> 该脚本所有的功能，全部依赖于php一句话木马，针对于部分携带后门的awd php题目，实现快速利用的效果。

脚本实现的功能：

- 生成目标ip地址
- 生成一句话木马
- 生成软链接
- 获取flag



## 使用方式

只需要输入相应的规则内容，来生成目标ip，并执行攻击

```python
    def __init__(self):
        self.param=input("请输入执行参数:")
        self.method=int(input("请输入请求方法的编号1:GET/2:PSOT :"))
        self.path=input("请输入后门地址如：/admin/config.php :")
        self.ip_method=int(input("请输入目标ip地址的方法,1 按网段生成,2 按端口生成:"))
        self.ip_con=[]
        self.flag=[]
```

