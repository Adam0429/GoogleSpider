# GoogleSpider
Spider Use Selenium Remote Control WebDrive And Download Images From Gooogle
谷歌图片爬虫。要解决的关键问题在于:搜索的图片不会一次性打出来,需要手动拉滚轮,利用selenium类可模拟对浏览器的操作,实现自动化下载。
开启爬虫之前要先启动selenium-server.jar








1.安装chrome

sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

如果上面运行 
sudo dpkg -i google-chrome*.deb命令之后报错，使用如下命令修复一下： 
sudo apt-get install -f,之后再次运行sudo dpkg -i google-chrome*.deb命令就可以了

安装后确认/usr/bin目录下是否有google-chrome文件
2.安装python、安装Selenium、安装requests(可选)

sudo apt-get install python-pip
sudo pip install selenium
#requests模块，可选安装
sudo pip install requests

3.安装chromedriver

建议安装最新版本的chromedriver，下载页面： 
http://chromedriver.storage.googleapis.com/index.html

在这个页面里列出了chromedriver的各个版本，我们选择目前最新的版本（2.29），使用命令行安装：

wget -N http://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

安装后确认/usr/bin目录下是否有chromedriver文件

由于时效性，在安装时应当先去网站查看最新版本，然后替换命令行中的2.29版本信息
4.简单示例

这时候就可以在图形界面的终端运行python自动化测试脚本了。 
示例脚本，打开网址并截图：

#coding:utf-8
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://zhaoyabei.github.io/")
driver.save_screenshot(driver.title+".png")