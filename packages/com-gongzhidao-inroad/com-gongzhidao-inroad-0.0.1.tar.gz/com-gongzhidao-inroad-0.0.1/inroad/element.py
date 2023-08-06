"""web端，公共元素"""
from selenium.webdriver.common.by import By


class BaseWebElement:

    # 查询--按条件
    web_search_info_button = (By.XPATH, "//div[text()='按条件']")
    # 查询--关键字输入框
    web_search_input = (By.XPATH, "//input[@placeholder='请输入关键字']")
    # 查询--查询按钮
    web_search_button = (By.XPATH, "//span[text() = '查询']")
    # 查询--开始时间和结束时间
    web_search_start_time = (By.XPATH, "//input[@placeholder = '请选择开始日期']")
    web_search_end_time = (By.XPATH, "//input[@placeholder = '请选择结束日期']")
    web_time = (By.XPATH, "//input[@placeholder = '选择日期时间']")
    web_now_time_button = (By.XPATH, "//span[contains(text(),'此刻')]")
    # 查询--状态下拉框
    web_search_state = (By.XPATH, "//input[@placeholder = '选择许可证状态']")


    # 链接
    web_link = (By.XPATH, "//div[@class = 'cell']/a")

    # 通用标题
    web_title = (By.XPATH, "//div[@class = 'title']")


    # 签名--按钮
    web_signature_button = (By.XPATH, "//img[@alt = '签名']")
    # 签名--密码输入框
    web_signature_pwd_input = (By.XPATH, "//input[@type = 'password']")
    # 签名--检验按钮
    web_signature_sure_button = (By.XPATH, "//span[text()='校验']")
    # 签名--确定按钮
    web_signature_t_button = (By.XPATH, "//span[contains(text(),'确认')]")

    # 通用选择是否
    web_check_button_t = (By.XPATH, "//span[text()='是']")
    web_check_button_f = (By.XPATH, "//span[text()='否']")
    web_check_button_no = (By.XPATH, "//span[text()='没有']")

    # 通用弹窗信息获取
    web_alert_text = (By.XPATH, "//p[@class = 'el-message__content']")

    # 通用添加按钮
    web_add_button = (By.XPATH, "//button[@type = 'button']//span[contains(text(),'添加')]")

    # 通用提交按钮
    web_submit_job = (By.XPATH, "//span[contains(text(),'提交')]")
    web_submit_button = (By.XPATH, "//span[text()='全部提交']")

    # 通用下拉框
    drop_down_box = (By.XPATH, "//input[@class = 'vue-treeselect__input']")

    # 选人输入框
    web_choose_person_input = (By.XPATH, "//input[@class = 'el-select__input is-medium']")
    # 选人按钮
    web_choose_person_button = (By.XPATH, "//span[text()='选人']")

    # 通用输入框
    web_input = (By.XPATH, "//input[@class = 'el-input__inner']")
    web_input_other_one = (By.XPATH, "//input[@placeholder = '请输入内容']")

    # 开始日期
    web_search_start_date = (By.XPATH, "//input[@placeholder = '开始日期']")
    # 结束日期
    web_search_end_date = (By.XPATH, "//input[@placeholder = '结束日期']")

    # 移除按钮
    web_remove_button = (By.XPATH, "//span[text()='移除']")

    # 下一步按钮
    web_next_tep_button = (By.XPATH, "//span[text()='下一步']")

    # 去分析按钮
    web_to_analyze_button = (By.XPATH, "//span[text()='去分析']")

    # 通用确定按钮
    web_sure_button = (By.XPATH, "//span[text()='确 定']")

    # 上传附件按钮
    web_upload_button = (By.XPATH, "//i[@class = 'el-icon-plus']")

