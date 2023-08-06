import time

# from qrunner import Browser
# from qrunner.core.ios.driver import Driver
# from qrunner.core.ios.element import Element
from qrunner import Browser
from qrunner.core.android.driver import Driver
from qrunner.core.android.element import Element


start = time.time()
# serial_no = '00008020-00086434116A002E'
# pkg_name = 'com.qizhidao.company'
# driver = Driver.get_instance(serial_no)
# Browser.driver = driver
# driver.app_stop(pkg_name)
# driver.app_start(pkg_name)
# Element(xpath='//*[@label="navi scan"]//../Other[1]').click()
serial_no = 'UJK0220521066836'
pkg_name = 'com.qizhidao.clientapp'
driver = Driver.get_instance(serial_no)
Browser.driver = driver
Browser.pkg_name = pkg_name
driver.app_stop(pkg_name)
driver.app_start(pkg_name)
Element(resourceId='id/banner').click()
end = time.time()
print(f'耗时：{end - start}')
