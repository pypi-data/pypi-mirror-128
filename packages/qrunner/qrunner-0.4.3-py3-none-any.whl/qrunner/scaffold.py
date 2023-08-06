import os.path
import sys

run_content = """
import argparse
import pytest
from qrunner import Browser


# 获取命令行输入的数据
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serial_no', dest='serial_no', type=str, default='', help='设备id')
parser.add_argument('-p', '--pkg_name', dest='pkg_name', type=str, default='', help='应用包名')

# 将数据写入配置文件
args = parser.parse_args()
Browser.serial_no = args.serial_no
Browser.pkg_name = args.pkg_name
Browser.alert_config = ['id/bottom_btn', 'id/ivLeadClose']

# 执行用例
pytest.main(['tests', '-sv', '--alluredir', 'allure-results',
             '--clean-alluredir', '--html=report.html', '--self-contained-html'])
"""

run_web_content = """
import argparse
import pytest
from qrunner import conf


# 获取命令行输入的数据
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--browser_name', dest='browser_name', type=str, default='', help='浏览器名称：ie、chrome、firefox、safari')

# 将数据写入配置文件
args = parser.parse_args()
conf.set_name('browser', 'browser_name', args.browser_name)

# 执行用例
pytest.main(['tests', '-s', '-v', '--alluredir', 'allure-results',
             '--clean-alluredir', '--html=report.html', '--self-contained-html'])
"""

conftest_adr_content = """
import pytest
from qrunner import Browser
from qrunner.core.android.driver import Driver


# 用例前后置
@pytest.fixture(autouse=True)
def init_case():
    driver = Driver.get_instance(Browser.serial_no)
    Browser.driver = driver

    driver.app_start(Browser.pkg_name, stop=True)
    yield
    driver.app_stop(Browser.pkg_name)
"""

conftest_ios_content = """
import pytest
from qrunner import conf, Browser
from qrunner.core.ios.wda_server import WDAServer
from qrunner.core.ios.element import Element
from qrunner.core.ios.driver Driver


# wda初始化
@pytest.fixture(scope='class', autouse=True)
def wda():
    ws = WDAServer(conf.get_name('device', 'serial_no'))
    ws.launch_wda()
    yield
    ws.stop_wda()


# 用例前后置
@pytest.fixture(autouse=True)
def case(app):
    _serial_no = conf.get_name('device', 'serial_no')
    _pkg_name = conf.get_name('app', 'pkg_name')
    
    driver = Driver.get_instance(_serial_no)
    Browser.driver = driver

    driver.app_terminate(_pkg_name)
    driver.app_start(_pkg_name)
    # Element(label='close white big').click_exists(timeout=5)
    yield 
    driver.app_stop(_pkg_name)
"""

conftest_web_content = """
import pytest
from qrunner import conf, Browser
from qrunner.core.web.driver import Driver

# driver初始化
@pytest.fixture(autouse=True)
def driver():
    browser_name = conf.get_name("browser", "browser_name")
    d = Driver.get_instance(browser_name)
    Browser.driver = d
    yield
    d.quit()
"""

page_adr_content = """
from qrunner.core.android.element import Page, Element


class HomePage(Page):
    my_entry = Element(resourceId='id/bottom_view', index=3)
"""

page_ios_content = """
from qrunner.core.ios.element import Page, Element


class HomePage(Page):
    my_entry = Element(name='我的')
"""

page_h5_content = """
from qrunner.core.h5.element import Page, Element


class PatentPage(Page):
    search_input = Element(class_name='h-b-content')
"""

page_web_content = """
from qrunner.core.web.element import Page, Element


class DemoPage(Page):
    search_input = Element(id="kw")
"""

case_android_content = """
import allure
from pages.demo_page import HomePage


@allure.feature('首页')
class TestDemo:
    @allure.title('进入我的')
    def test_01(self):
        page = HomePage()
        page.my_entry.click()
"""

case_ios_content = """
import allure
import time
from pages.demo_page import HomePage


@allure.feature('首页')
class TestDemo:
    @allure.title('从首页进入我的tab')
    def test_01(self):
        page = HomePage()
        page.my_entry.click()
        time.sleep(5)
"""

case_h5_content = """
import allure
from qrunner.core.h5.driver import Driver
from pages.demo_page import HomePage, PatentPage


@allure.feature('查专利')
class TestPeerSearch:
    def setup_method(self):
        self.d = Driver()
        self.home_page = HomePage()
        self.patent_page = PatentPage(self.d)

    @allure.title('点击顶部搜索框')
    def test(self):
        self.home_page.go_patent()
        self.patent_page.go_search()
"""

case_web_content = """
import allure
import time
from pages.demo_page import DemoPage


@allure.feature('百度首页')
class TestDemo:
    @allure.title('输入关键词')
    def test_01(self):
        page = DemoPage('https://www.baidu.com')
        page.search_input.input('企知道')
        time.sleep(5)
"""

require_content = """
qrunner
"""

ignore_content = "\n".join(
    ["allure-results/*", "__pycache__/*", "*.pyc", "report.html", ".idea/*"]
)


def init_scaffold_project(subparsers):
    parser = subparsers.add_parser(
        "startpro", help="Create a new project with template structure."
    )
    parser.add_argument(
        "platform_type", type=str, nargs="?", help="Specify new platform type."
    )
    parser.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return parser


def create_scaffold(project_name, platform):
    """ create scaffold with specified project name.
    """

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 创建公共内容
    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "pages"))
    if platform == 'web':
        create_file(
            os.path.join(project_name, "run.py"),
            run_web_content,
        )
    else:
        create_file(
            os.path.join(project_name, "run.py"),
            run_content,
        )
    create_file(
        os.path.join(project_name, ".gitignore"),
        ignore_content,
    )
    create_file(
        os.path.join(project_name, "requirements.txt"),
        require_content,
    )

    # 创建平台相关的内容
    def create_platform(conftest_content, page_content, case_content):
        create_file(
            os.path.join(project_name, "conftest.py"),
            conftest_content,
        )
        create_file(
            os.path.join(project_name, "pages", "demo_page.py"),
            page_content,
        )
        create_file(
            os.path.join(project_name, "tests", "test_demo.py"),
            case_content,
        )

    if platform == 'android':
        create_platform(conftest_adr_content, page_adr_content, case_android_content)
    elif platform == 'ios':
        create_platform(conftest_ios_content, page_ios_content, case_ios_content)
    elif platform == 'h5':
        create_platform(conftest_adr_content, page_h5_content, case_h5_content)
    elif platform == 'web':
        create_platform(conftest_web_content, page_web_content, case_web_content)
    # show_tree(project_name)
    return 0


def main_scaffold_project(args):
    sys.exit(create_scaffold(args.project_name, args.platform_type))

