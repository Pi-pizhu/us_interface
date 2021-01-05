# us_interface

#### 简介
- loguru日志可以获取每个用例的请求信息、响应信息、每个阶段的操作信息；
- Template技术，实现请求体信息、断言等数据驱动；
- 利用数据库封装，解决数据关联、生成、清理等操作；
- 全局配置文件控制环境切换、敏感信息读取；
- 通过Charles抓包，har文件扫描生成api yml文件；
- 通过jinja2模板技术，扫描api yml文件，自动生成基础api page文件，减少中间环境花费的时间；
- 通过jsonpath技术，便捷提取响应数据。

#### 测试流程：
1.写入api yml文件

2.使用utils/make_template.py/make_api_page()函数批量生成api page

3.修改完善api page内容(例如接收处理接口参数)

4.测试用例根目录添加env_config.ini，配置全局变量

5.编写testcase测试测试用例

6.运行测试

#### 使用技术列表

- pytest：测试框架
- allure：报告框架
- requests：请求核心
- jsonpath：json数据提取
- loguru：日志框架
- pyyaml：yml文件操作框架
- configparser：ini文件操作框架
- jinja2：模板技术，生成模板
- pymysql：数据库操作

#### 基础文件格式
##### env_config.ini
```ini
[token]
corp_id = 
corp_secret = 
contact_secret =
meeting_room_secret =
schedule_secret =

[hosts]
domain_name = qyapi.weixin.qq.com
default = debug
debug = 127.0.0.1
formal = 127.0.0.2

[mysql]
host = None
port = None
user = None
password = None
charset = None
databse = None
```
基本用于全局变量数据提供：
- domain_name：提供域名，如果出现指定的域名则进行ip替换
- default：指定使用哪一个ip

##### api yml文件格式
```yaml
# 获取部门信息的api
get:
  "method": "get"
  "url": "/cgi-bin/department/list"
  "params": "access_token=${token}&id=${id}"

# 增加部门信息的api,每增加一次就会递增
add:
  "method": "post"
  "url": "/cgi-bin/department/create"
  "params": "access_token=${token}"
  "json":
      "name": "$name"
      "parentid": $parentid


# 删除部门信息的api
delete:
  "method": "get"
  "url": "/cgi-bin/department/delete"
  "params": "access_token=${token}&id=${id}"

# 更新部门信息的api
edit:
  "method": "post"
  "url": "/cgi-bin/department/update"
  "params": "access_token=${token}"
  "json":
    "name": "$name"
    "id": $id
```

通过api name来定义每个请求体，请求体格式与requests要求一致