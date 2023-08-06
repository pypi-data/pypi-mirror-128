#DAS_UTILS
大众云学_工具箱


#库文件规范
- **das_utils** 项目文件夹名，可自定义，下划线+英文小写字母,有一个项目 只能有一个名字且要保证唯一性，das_开头.
    
    项目文件夹下必须要有**\_\_init__.py**

- **DAS-INFO** 补上必要信息

    如**type:1**(类型：0基础包1web服务包2web过滤器包)

- **MANIFEST.in** 可包含python库资源文件，如.txt等

- **README.md** 项目简介,及使用示例

- **requirements.txt** 补上所有依赖包

- **setup.py** 修改合适的版本号,如1.0.0
#库文件打包
```
sh sdist.sh
```

将在dist下文件生成 **“项目名-版本号.zip”** 包
