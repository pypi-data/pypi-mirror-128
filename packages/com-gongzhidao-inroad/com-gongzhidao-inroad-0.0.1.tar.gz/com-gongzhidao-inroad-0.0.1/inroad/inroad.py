"""
公共方法封装页面
作者：刘叶峰
"""

import logging.config
import logging.handlers
import os
import time

import win32con
import win32gui
from configobj import ConfigObj
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from element import BaseWebElement
from selenium.webdriver.common.keys import Keys


class Base:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 工程根目录

    def __init__(self, driver):
        self.driver = driver
        self.file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.basf_job_file_path = os.path.join(os.path.join(self.file_path, 'Config'), 'config.ini')

    def get_element(self, loc, timeout=20, poll_frequency=1.0):
        """
        定位单个元素
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:元素定位对象
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_element(*loc))

    def get_elements(self, loc, timeout=20, poll_frequency=1.0):
        """
        定位一组元素
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:元素定位对象列表
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_elements(*loc))

    def click_element(self, loc, timeout=20, poll_frequency=1.0):
        """
        点击元素
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:
        """
        try:
            self.get_element(loc, timeout, poll_frequency).click()
        except:
            ele = self.get_element(loc, timeout, poll_frequency)
            self.driver.execute_script("arguments[0].click();", ele)

    def click_elements(self, loc, element_num, timeout=20, poll_frequency=1.0):
        """
        点击元素
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param element_num: 选择一组元素的其中一个定位
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:
        """
        try:
            self.get_elements(loc, timeout, poll_frequency)[element_num].click()
        except:
            ele = self.get_elements(loc, timeout, poll_frequency)[element_num]
            self.driver.execute_script("arguments[0].click();", ele)

    def send_element(self, loc, text, timeout=20, poll_frequency=1.0):
        """
        输入文本内容
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param text: 输入文本内容
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:
        """
        # 定位元素
        input_text = self.get_element(loc, timeout, poll_frequency)
        # 清空输入框
        input_text.clear()
        # 输入元素
        input_text.send_keys(text)

    def send_elements(self, loc, text, element_num, timeout=20, poll_frequency=1.0):
        """
        输入文本内容
        :param loc: (By.ID,id属性值) (By.CLASS_NAME,class属性值) (By.XPATH,xpath属性值)
        :param text: 输入文本内容
        :param element_num: 选择一组元素的其中一个定位
        :param timeout: 搜索元素超时时间
        :param poll_frequency: 元素每次搜索间隔
        :return:
        """
        self.get_elements(loc, timeout, poll_frequency)[element_num].send_keys(text)

    def uplaod(self, file_path):
        """上传文件"""
        # win32gui
        dialog = win32gui.FindWindow("#32770", "打开")  # 一级窗口
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级窗口
        combox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级窗口
        edit = win32gui.FindWindowEx(combox, 0, 'Edit', None)  # edit元素
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 打开按钮
        time.sleep(2)
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)  # 往输入框输入绝对地址
        time.sleep(2)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

    def get_text(self, element):
        """
        获取弹窗内的值
        :param element:
        :return:
        """
        try:
            value = self.get_element(element).text
        except AttributeError:
            # 获取元素内容的方式有两种：一种是.text，另一种是通过.get_attribute('value')的方式
            try:
                value = self.get_element(element).get_attribute('value')
            except:
                print("未获取到提示框内容")
            else:
                return value
        else:
            return value

    def switch_to_new_window(self):
        """切换新窗口方法一"""
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def open_new_window(self):
        """切换新窗口方法二"""
        window_1 = self.driver.current_window_handle
        windows = self.driver.window_handles
        for current_window in windows:
            if current_window != window_1:
                self.driver.switch_to.window(current_window)

    def open_window(self, num):
        window_1 = self.driver.window_handles
        self.driver.switch_to.window(window_1[num])

    # 写入 需要获取的信息
    def write_info_in_config(self, section, setion_name, text_info):
        config = ConfigObj(self.basf_job_file_path, encoding='UTF8')
        config[section][setion_name] = text_info
        config.write()

    # 读取 需要获取的信息
    def read_info_in_config(self, section, setion_name):
        config = ConfigObj(self.basf_job_file_path, encoding='UTF8')
        return config[section][setion_name]

    def screen_page(self, name):
        """
        报告添加截图
        :param name: 截图名字
        :return:
        """
        # 定义图片名字
        # png_name = self.BASE_DIR + '/reports/'+ "{}.png".format(int(time.time()))
        rq = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        png_name = self.BASE_DIR + '/reports/' + "{}_{}.png".format(rq, name)
        # timeArray = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        # png_name = self.BASE_DIR + '/reports/' + "{}.png".format(int(time.mktime(timeArray)))
        # 截图
        self.driver.get_screenshot_as_file(png_name)

    def init_log_config(self):
        # 创建日志器
        logger = logging.getLogger()
        # 设置日志级别
        logger.setLevel(level=logging.INFO)
        # 创建处理器
        # 输出到控制台的处理器
        sh = logging.StreamHandler()
        log_path = self.BASE_DIR + '/log/' + 'Case.log'
        # 输出到文件的处理器
        th = logging.handlers.TimedRotatingFileHandler(log_path,
                                                       when='midnight',
                                                       interval=1,
                                                       backupCount=5,
                                                       encoding='utf-8')
        # 创建格式器
        fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
        formatter = logging.Formatter(fmt)
        # 将格式器添加给处理器
        sh.setFormatter(formatter)
        th.setFormatter(formatter)
        # 将处理器添加给日志器
        logger.addHandler(sh)
        logger.addHandler(th)

    #############################################################工智道公共方法############################################################

    # 点击新增按钮（按钮个数唯一）
    def gzd_click_add_button(self):
        self.click_element(BaseWebElement.web_add_button)

    # 点击新增按钮（按钮个数不唯一）
    def gzd_click_add_buttons(self, num):
        """
        :param num: 下标数
        :return:
        """
        self.click_elements(BaseWebElement.web_add_button,num)


    # 点击提交按钮（按钮个数唯一）
    def gzd_click_submit_button(self):
        self.click_element(BaseWebElement.web_submit_job)

    # 点击提交按钮（按钮个数不唯一）
    def gzd_click_submit_buttons(self, num):
        """
        :param num: 下标数
        :return:
        """
        self.click_elements(BaseWebElement.web_submit_job, num)

    # 点击选人按钮(按钮个数唯一)
    def gzd_click_choose_person_button(self):
        self.click_element(BaseWebElement.web_choose_person_button)

    # 点击选人按钮(按钮个数不唯一)
    def gzd_click_choose_person_buttons(self, num):
        """
        :param num: 下标数
        :return:
        """
        self.click_elements(BaseWebElement.web_choose_person_button, num)


    # 选择是、否（唯一）
    def gzd_click_t_f_box(self, result):
        if result == "是":
            self.click_element(BaseWebElement.web_check_button_t)
        else:
           self.click_element(BaseWebElement.web_check_button_f)

    # 选择是、否（不唯一）
    def gzd_click_t_f_boxs(self, result, num):
        if result == "是":
           self.click_elements(BaseWebElement.web_check_button_t, num)
        else:
            self.click_elements(BaseWebElement.web_check_button_f, num)

    # 下拉框(下拉框个数唯一)
    def gzd_drop_down_box(self, text):
        """
        :param text: 下拉框检索内容
        :return:
        """
        if text == "":
            pass
        else:
            # 点击部门下拉框
            self.click_element(BaseWebElement.drop_down_box)
            time.sleep(1)
            # 输入部门名称
            self.send_element(BaseWebElement.drop_down_box, text)
            time.sleep(1)
            # 模拟键盘向下箭头
            self.send_element(BaseWebElement.drop_down_box, Keys.DOWN)
            time.sleep(1)
            # 模拟键盘回车
            self.send_element(BaseWebElement.drop_down_box, Keys.ENTER)
            time.sleep(1)

    # 下拉框(下拉框个数不唯一)
    def gzd_drop_down_boxs(self, text, num):
        """
        :param text: 下拉框检索内容
        :param num: 下拉框下标
        :return:
        """
        if text == "":
            pass
        else:
            # 点击部门下拉框
            self.click_elements(BaseWebElement.drop_down_box, num)
            time.sleep(1)
            # 输入部门名称
            self.send_elements(BaseWebElement.drop_down_box, text, num)
            time.sleep(1)
            # 模拟键盘向下箭头
            self.send_elements(BaseWebElement.drop_down_box, Keys.DOWN, num)
            time.sleep(1)
            # 模拟键盘回车
            self.send_elements(BaseWebElement.drop_down_box, Keys.ENTER, num)
            time.sleep(1)

    # 选人方法-通过输入框选择（选人输入框不唯一）
    def gzd_choose_person_for_input(self, person_name):
        """
        :param person_name: 人员名称
        :return:
        """
        if person_name == "":
            pass
        else:
            self.send_element(BaseWebElement.web_choose_person_input, person_name)
            time.sleep(1)
            self.send_element(BaseWebElement.web_choose_person_input, Keys.DOWN)
            time.sleep(1)
            self.send_element(BaseWebElement.web_choose_person_input, Keys.ENTER)

    # 选人方法-通过输入框选择（选人输入框不唯一）
    def gzd_choose_person_for_inputs(self, person_name, num):
        """
        :param person_name: 人员名称
        :param num: 下标数
        :return:
        """
        if person_name == "":
            pass
        else:
            self.send_elements(BaseWebElement.web_choose_person_input, person_name, num)
            time.sleep(1)
            self.send_elements(BaseWebElement.web_choose_person_input, Keys.DOWN, num)
            time.sleep(1)
            self.send_elements(BaseWebElement.web_choose_person_input, Keys.ENTER, num)
            time.sleep(1)
            self.click_elements(BaseWebElement.web_choose_person_input, num)

    # 输入框填写信息（唯一）
    def gzd_input_info(self, ele, text):
        if text == "":
            pass
        else:
            self.send_element(ele, text)

    # 输入框填写信息（不唯一）
    def gzd_input_infos(self, ele, text, num):
        if text == "":
            pass
        else:
            self.send_elements(ele, text, num)

    # 最后一个输入框填写信息（不唯一）
    def gzd_last_input_infos(self,ele,text):
        if text == "":
            pass
        else:
            lens = len(self.get_elements(ele))
            self.send_elements(ele, text, lens-1)

    # 填写 计划时间（唯一）
    def gzd_input_plan_time(self, start_time, end_time):
        if start_time == "":
            pass
        else:
            self.send_element(BaseWebElement.web_search_start_date, start_time)
        if end_time == "":
            pass
        else:
            self.send_element(BaseWebElement.web_search_end_date, end_time)

    # 填写时间
    def gzd_input_time(self,now_time):
        if now_time == "":
            pass
        elif now_time == "此刻":
            self.click_element(BaseWebElement.web_time)
            time.sleep(1)
            self.click_element(BaseWebElement.web_now_time_button)
        else:
            self.send_element(BaseWebElement.web_time,now_time)
        time.sleep(1)

    # 获取标题并记录(唯一)
    def gzd_get_title_write_in_config(self, common, name):
        text = self.get_element(BaseWebElement.web_title).text
        self.write_info_in_config(common, name, text)

    # 按条件查询(目前支持，关键字+时间筛选)
    def gzd_query_by_condition(self, text, start_time, end_time):
        self.click_element(BaseWebElement.web_search_info_button)
        self.send_element(BaseWebElement.web_search_input, text)
        self.send_element(BaseWebElement.web_search_start_time, start_time)
        self.send_element(BaseWebElement.web_search_start_time, Keys.ENTER)
        self.send_element(BaseWebElement.web_search_end_time, end_time)
        self.send_element(BaseWebElement.web_search_end_time, Keys.ENTER)
        self.click_element(BaseWebElement.web_search_button)
        time.sleep(2)

    # 点击链接进行跳转（不唯一）
    def gzd_click_links(self,num):
        self.click_elements(BaseWebElement.web_link,num)
        self.open_new_window()
        time.sleep(3)

    # 获取弹窗返回值
    def gzd_get_alert_text(self):
        return self.get_text(BaseWebElement.web_alert_text)

    # 签名按钮进行签名操作(唯一)
    def gzd_signature(self, pwd):
        self.click_element(BaseWebElement.web_signature_button)
        self.send_element(BaseWebElement.web_signature_pwd_input, pwd)
        try:
            lens = len(self.get_elements(BaseWebElement.web_signature_sure_button))
            a = lens - 1
        except:
            a = 0
        self.click_elements(BaseWebElement.web_signature_sure_button, a)
        time.sleep(1)
        try:
            lens_t = len(self.get_elements(BaseWebElement.web_signature_t_button))
            b = lens_t - 1
        except:
            b = 0
        self.click_elements(BaseWebElement.web_signature_t_button, b)
        time.sleep(1)

        # 签名按钮进行签名操作(不唯一)
    def gzd_signatures(self, pwd, num):
        self.click_elements(BaseWebElement.web_signature_button,num)
        try:
            self.send_element(BaseWebElement.web_signature_pwd_input, pwd)
        except:
            a = len(self.get_elements(BaseWebElement.web_signature_pwd_input)) - 1
            self.send_elements(BaseWebElement.web_signature_pwd_input, pwd, a)
        try:
            self.click_element(BaseWebElement.web_signature_sure_button)
        except:
            a = len(self.get_elements(BaseWebElement.web_signature_sure_button)) - 1
            self.click_elements(BaseWebElement.web_signature_sure_button, a)
        time.sleep(1)
        try:
            self.click_element(BaseWebElement.web_signature_t_button)
        except:
            b = len(self.get_elements(BaseWebElement.web_signature_t_button)) - 1
            try:
                self.click_elements(BaseWebElement.web_signature_t_button, b)
            except:
                pass
        time.sleep(1)

    ###############################################################APP公共方法############################################################

    # 根据坐标 进行点击操作
    def click_coordinate(self, coordinate, coordinate_time=100):
        self.driver.tap(coordinate, coordinate_time)

    def swipe(self):
        # 设置页面滑动  高80% -> 高30%  {'width': , 'height': } 宽50%
        screen_size = self.driver.get_window_size()
        # 手机宽
        width = screen_size.get("width")
        # 手机高
        height = screen_size.get("height")
        # 滑动 width*50% height*80% -> width*50% height*30%
        self.driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.3, duration=2000)

    def get_toast(self, toast):
        """
        获取toast消息
        :param toast: 拼接xpath的toast内容
        :return: 返回获取到的toast
        """
        # 找toast
        toast_xpath = (By.XPATH, "//*[contains(@text,'{}')]".format(toast))
        # 找元素
        data = self.get_element(toast_xpath).text
        # 返回toast消息
        return data

    def mouse_wheel_scroll(self, num):
        """鼠标滑轮滚动，0是最上面，100000是最底部"""
        if num == "up":
            js = "document.documentElement.scrollTop=0"
            self.driver.execute_script(js)
        if num == "down":
            js = "document.documentElement.scrollTop=100000"
            self.driver.execute_script(js)