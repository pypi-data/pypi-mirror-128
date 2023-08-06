from setuptools import setup,find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name = 'SeleniumCommonSetting',
    version = '1.0.6',
    keywords = ('selenium'),
    description = '常用的selenium-webdriver设置',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT Licence',

    author = 'JoeYoung',
    author_email = '1022104172@qq.com',
    url = 'https://gitee.com/joeyoung18/SeleniumCommonSetting.git',

    py_modules = ['SeleniumCommonSetting'],
    packages = find_packages(),
    include_package_data = True,
)