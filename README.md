# Material Management System (Using `Django`)

## 环境配置

1. 打开命令行窗口，创建新环境: `conda create --name djangolatest`
2. 激活环境: `conda activate djangolatest`
3. 安装`Django`: `python -m pip install Django`
4. 安装MySQL相关包: `conda install pymysql`
   > 您可以选择使用其他数据库管理系统。具体请参考[官方文档](https://docs.djangoproject.com/en/4.0/topics/install/#database-installation)。
5. 运行: `python3 manage.py runserver`
6. 在浏览器中打开`http://127.0.0.1:8000/mm/register/`即可开始注册账号；在浏览器中打开`http://127.0.0.1:8000/mm/login/`即可登录账号。可以使用测试用户名（Erp2022）、邮箱（erp2022@tongji.edu.cn）和密码（Admin2022）登录。