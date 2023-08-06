import sys


def init_scaffold_page(subparsers):
    parser = subparsers.add_parser(
        "startpage", help="Create a new page with template structure."
    )
    parser.add_argument(
        "platform_type", type=str, nargs="?", help="Specify new platform type."
    )
    parser.add_argument(
        "page_name", type=str, nargs="?", help="Specify new page name."
    )
    return parser


def create_scaffold(page_name: str, platform):
    """ create scaffold with specified page name.
    """

    # 构造用例名和类名
    file_name = page_name + '_page'
    class_name = ''
    if '_' in page_name:
        lst = page_name.split('_')
        for item in lst:
            class_name = class_name + item.capitalize()
        class_name = class_name + 'Page'
    else:
        class_name = page_name.capitalize() + 'Page'

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 创建平台相关的内容
    def create_platform(page_content):
        create_file(
            f"{file_name}.py",
            page_content,
        )

    if platform == 'android':
        page_adr_content = f"""
from qrunner.core.android.element import Page, Element


class {class_name}(Page):
    # 元素定位
    pass

    def method_01(self):
        # 元素操作
        pass
"""
        create_platform(page_adr_content)
    elif platform == 'ios':
        page_ios_content = f"""
from qrunner.core.ios.element import Page, Element


class {class_name}(Page):
    # 元素定位
    pass

    def method_01(self):
        # 元素操作
        pass
"""
        create_platform(page_ios_content)
    elif platform == 'h5':
        page_h5_content = f"""
from qrunner.core.h5.element import Element
from selenium.webdriver.common.by import By
from qrunner.core.android.element import Element


class {class_name}:
    def __init__(self, d):
        # 元素定位
        pass

    def method_01(self):
        # 元素操作
        pass
"""
        create_platform(page_h5_content)
    elif platform == 'web':
        page_web_content = f"""
from qrunner.core.web.element import Element
from selenium.webdriver.common.by import By


class {class_name}:
    def __init__(self, d, url):
        self.d = d
        self.url = url
        # 元素定位
        pass

    def open(self):
        self.d.get(self.url)

    def method_01(self):
        # 操作步骤
        pass
"""
        create_platform(page_web_content)
    # show_tree(project_name)
    return 0


def main_scaffold_page(args):
    sys.exit(create_scaffold(args.page_name, args.platform_type))

