import sys


def init_scaffold_case(subparsers):
    parser = subparsers.add_parser(
        "startcase", help="Create a new case with template structure."
    )
    parser.add_argument(
        "platform_type", type=str, nargs="?", help="Specify new platform type."
    )
    parser.add_argument(
        "case_name", type=str, nargs="?", help="Specify new case name."
    )
    return parser


def create_scaffold(case_name: str, platform):
    """ create scaffold with specified case name.
    """

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 创建平台相关的内容
    def create_platform(case_content):
        create_file(
            f"test_{case_name}.py",
            case_content,
        )

    # 构造用例类名
    if '_' in case_name:
        lst = case_name.split('_')
        class_name = ''
        for item in lst:
            class_name = case_name + item.capitalize()
    else:
        class_name = case_name.capitalize()

    if platform == 'android':
        case_android_content = f"""import allure
# 导入页面
pass


@allure.feature('所属模块')
class Test{class_name}:
    @allure.title('用例标题')
    def test_01(self, app):
        # 编写用例
        pass
"""
        create_platform(case_android_content)
    elif platform == 'ios':
        case_ios_content = f"""import allure
# 导入页面
pass


@allure.feature('所属模块')
class Test{class_name}:
    @allure.title('用例标题')
    def test_01(self, app):
        # 编写用例
        pass
"""
        create_platform(case_ios_content)
    elif platform == 'h5':
        case_h5_content = f"""import allure
from qrunner.core.h5.driver import Driver
# 导入页面
pass


@allure.feature('所属模块')
class Test{class_name}:
    def setup_method(self):
        # h5Driver初始化
        self.d = Driver()
        # 页面初始化
        pass

    @allure.title('用例标题')
    def test_01(self):
        # 编写用例
        pass
"""
        create_platform(case_h5_content)
    elif platform == 'web':
        case_web_content = f"""import allure
# 导入页面
pass


@allure.feature('所属模块')
class Test{class_name}:
    def setup_method(self):
        # 页面初始化
        pass

    @allure.title('用例标题')
    def test_01(self, driver):
        # 编写用例
        pass
"""
        create_platform(case_web_content)
    # show_tree(project_name)
    return 0


def main_scaffold_case(args):
    sys.exit(create_scaffold(args.case_name, args.platform_type))

