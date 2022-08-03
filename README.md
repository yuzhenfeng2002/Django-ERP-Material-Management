# Material Management System (Using `Django`)

## 环境配置

1. 打开命令行窗口，创建新环境: `conda create --name djangolatest`
2. 激活环境: `conda activate djangolatest`
3. 安装`Django`: `python -m pip install Django`
4. 安装MySQL相关包: `conda install pymysql`
   > 您可以选择使用其他数据库管理系统。具体请参考[官方文档](https://docs.djangoproject.com/en/4.0/topics/install/#database-installation)。
5. 运行: `python3 manage.py runserver`
6. 在浏览器中打开`http://127.0.0.1:8000/mm/register/`即可开始注册账号；在浏览器中打开`http://127.0.0.1:8000/mm/login/`即可登录账号。可以使用测试用户名（Erp2022）、邮箱（erp2022@tongji.edu.cn）和密码（Admin2022）登录。

## URL

### 用户管理

#### `mm/login/`

若请求为GET方法，无请求参数，使用模板`user/login.html`直接返回。

若请求为POST方法，请求参数包括：
- 邮箱: `email`
- 密码: `password`
若用户名与密码正确，则重定向至`mm/home/`；否则，使用模板`user/login.html`载入错误提示信息`message`返回。

#### `mm/logout/`

登出用户后，重定向至`mm/login/`。

#### `mm/register/`

若请求为GET方法，无请求参数，使用模板`user/register.html`直接返回。

若请求为POST方法，请求参数包括：
- 用户名: `username`
- 名: `first_name`
- 姓: `last_name`
- 密码: `password`
- 再次输入密码: `password1`
- 邮箱: `email`
- 部门: `sector`
- 手机: `phone`
- 密保问题1: `question1`
- 回答1: `answer1`
- 密保问题2: `question2`
- 回答2: `answer2`
注册信息符合要求，则重定向至`mm/login/`；否则，使用模板`user/register.html`载入错误提示信息`message`返回。

### 供应商管理

#### `mm/vendor/create/`

若请求为GET方法，无请求参数，使用模板`vendor/vendor.html`载入表单`form`并返回，`form`包括的字段有：
- 供应商名称: `vname`
- 城市: `city`
- 国家: `country`
- 地址: `address`
- 邮编: `postcode`
- 语言: `language`
- GL账户: `glAcount`
- TP类型: `tpType`
- 公司编号: `companyCode`
- 货币: `currency`

若请求为POST方法，请求参数为表单中的各字段。若创建成功，则重定向至`mm/vendor/display/<int:pk>/`，并发送`messages`，只包括一条`"Successfully created!"`；否则，使用模板`vendor/vendor.html`载入原表单`form`（包括错误信息）返回。

#### `mm/vendor/display/<int:pk>/`

请求为GET方法，请求参数为供应商的主键`pk`，使用模板`vendor/vendor.html`载入表单`form`和主键`pk`并返回，`form`包括的字段同上，`form`中的初始值是主键为`pk`的供应商的对应数据。

#### `mm/vendor/update/`

请求为POST方法，请求参数为同上表单中的各字段、主键`pk`。若修改该供应商信息的用户与创建用户不同，则重定向至`mm/vendor/display/<int:pk>/`，发送`messages`，只包括一条`"You do not have access to the vendor."`；若修改成功，则重定向至`mm/vendor/display/<int:pk>/`，发送`messages`，只包括一条`"Successfully updated!"`；否则，使用模板`vendor/vendor.html`载入原表单`form`（包括错误信息）和主键`pk`返回。

#### `mm/vendor/search/`

若请求为GET方法，无请求参数，使用模板`vendor/search.html`直接返回。

若请求为POST方法，请求参数为字段（均为**正则表达式**，考虑后期改进）：
- 供应商主键: `pk`
- 供应商名称: `vname`
- 创建者ID: `uid`
- 城市: `city`
- 国家: `country`
- 公司编号: `companyCode`

若检索成功，则使用模板`vendor/search.html`载入搜索结果`vendors`返回，发送`messages`，只包括一条`"Succeed to get {:} results."`；否则，直接使用模板`vendor/search.html`返回，发送`messages`，只包括一条`"There is no matched result."`。