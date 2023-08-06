# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : base.py
# Describe :
# ---------------------------------------
import functools
import sys

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from lazyTest.base.config import Config
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains





def _retrying(func):
    @functools.wraps(func)
    def inner(*args):
        # 如果是字符串，直接传入不进行重试
        if isinstance(args[1], str):
            result = func(*args)
            return result
        ele = iter(args[1])  # 非字符串，创建迭代器

        # 实现重试机制，报错就会重试，直到迭代所有
        def run(ele, *args):
            args = list(args)  # 兼容多个参数
            try:
                e = next(ele)
            except StopIteration:
                raise WebDriverException(msg=f"重试结束，无法定位：{args}")
            try:
                args[1] = e  # 处理时只处理第一个参数
                result = func(*args)
                return result
            except BaseException as e:  # 捕获所有异常
                result = run(ele, *args)
            return result

        result = run(ele, *args)
        return result

    return inner


class WebOption(Config):
    def Get(self, url: str) -> None:
        urls = self.baseUrl + url
        self.baseDriver.get(urls)

    @_retrying
    def Click(self, selector: str) -> None:
        """元素点击操作"""
        ele = self.locate_element(selector)
        ele.click()

    @_retrying
    def RightClick(self, selector: str) -> None:
        """鼠标右键"""
        ele = self.locate_element(selector)
        ActionChains(self.baseDriver).context_click(selector)

    @_retrying
    def DoubleClick(self, selector: str) -> None:
        """元素双击"""
        ele = self.locate_element(selector)
        ActionChains(self.baseDriver).double_click(ele).perform()

    def DragAndDrop(self, source, target):
        """从源元素按住左键不放拖动到指定元素"""
        start = self.locate_element(source)
        end = self.locate_element(target)
        ActionChains(self.baseDriver).drag_and_drop(start, end)

    @_retrying
    def ActionScroll(self, selector: str, x: int = 0, y: int = 10):
        """内嵌滚动条滚动"""
        ele = self.locate_element(selector)
        ActionChains(self.baseDriver).drag_and_drop_by_offset(ele, x, y).perform()

    @_retrying
    def Input(self, selector: str, *value: str) -> None:
        """元素输入操作"""
        ele = self.locate_element(selector)
        ele.send_keys(*value)

    @_retrying
    def Clear(self, selector: str) -> None:
        """元素输入框清空输入内容"""
        ele = self.locate_element(selector)
        ele.clear()

    @_retrying
    def KeysClear(self, selector: str):
        """通过键盘输入物理清楚文本框内容"""
        ele = self.locate_element(selector)
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)

    @_retrying
    def ClearAndInput(self, selector: str, value: str) -> None:
        """清空输入框并输入内容"""
        ele = self.locate_element(selector)
        ele.clear()
        ele.send_keys(value)

    @_retrying
    def GetText(self, selector: str) -> str:
        """获取元素文本内容"""
        ele = self.locate_element(selector)
        return ele.text

    @_retrying
    def GetTexts(self, selector: str, index: int = None) -> list:
        """获取一组元素的文本内容"""
        ele = self.locate_elements(selector)
        if index is not None:
            return ele[index].text
        else:
            text_list = [i.text for i in ele]
            return text_list

    @_retrying
    def GetElement(self, selector: str):
        """定位单个元素"""
        ele = self.locate_element(selector)
        return ele

    @_retrying
    def GetElements(self, selector: str, text: str = "", index: int = None, ):
        """获取一组元素"""
        eles = []
        ele = self.locate_elements(selector)
        if text != "":
            for i in ele:
                if i.text == text:
                    eles.append(i)
            if index is not None:
                return eles[index]
            return eles
        return ele

    @_retrying
    def ElementFilterByText(self, selector: str, text: str):
        """获取一组元素，根据指定的文本进行过滤"""
        ele = self.locate_elements(selector)
        if text is not None:
            for i in ele:
                if i.text == text:
                    return i

    @_retrying
    def ElementFilterByIndex(self, selector: str, index: int = None):
        """获取一组元素，根据指定的索引进行过滤"""
        ele = self.locate_elements(selector)
        return ele[index]

    @_retrying
    def GetAttribute(self, selector: str, value: str = 'value') -> str:
        """
        获取元素属性
        textContent: 可用于获取没有在当前窗口显示的文本内容
        value： 用于获取元素的value属性
        """
        ele = self.locate_element(selector)
        return ele.get_attribute(value)

    @_retrying
    def AddAttribute(self, selector: str, attributeName: str, value: str):
        '''
        封装向页面标签添加新属性的方法
        '''
        ele = self.locate_element(selector)
        self.baseDriver.execute_script("arguments[0].%s=arguments[1]" % attributeName, ele, value)

    @_retrying
    def SetAttribute(self, selector: str, attributeName: str, value: str):
        '''
        封装设置页面对象的属性值的方法
        '''
        ele = self.locate_element(selector)
        self.baseDriver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", ele, attributeName,
                                       value)

    @_retrying
    def SwitchFrame(self, selector: str) -> None:
        """根据框架定位元素值切换"""
        ele = self.locate_element(selector)
        self.baseDriver.switch_to.frame(ele)

    def SwitchParentFrame(self):
        """切换到父框架"""
        self.baseDriver.switch_to.parent_frame()

    def SwitchDefaultContent(self):
        """切换到默认框架"""
        self.baseDriver.switch_to.default_content()

    def SwitchWindow(self, window_Num=-1):
        """切换窗口默认切换到最后一个"""
        handles = self.baseDriver.window_handles()
        self.baseDriver.switch_to.window(handles[window_Num])

    def OperationAlert(self, operation: str = 'accept'):
        """处理弹窗"""
        alert = self.baseDriver.switch_to.alert
        if operation == 'accept':
            alert.accept()
        elif operation == 'dismiss':
            alert.dismiss()

    @_retrying
    def SelectOperation(self, selector: str, operation_type: str, value: str) -> None:
        """下拉框处理"""
        if operation_type == 'index':
            Select(self.locate_element(selector)).deselect_by_index(value)
        elif operation_type == 'value':
            Select(self.locate_element(selector)).deselect_by_value(value)
        elif operation_type == 'text':
            Select(self.locate_element(selector)).deselect_by_visible_text(value)

    def browser_close(self):
        """关闭浏览器"""
        self.baseDriver.close()

    def browser_quit(self):
        """退出浏览器"""
        self.baseDriver.quit()

    def Refresh(self):
        """刷新浏览器"""
        self.baseDriver.refresh()

    def ExcuteScript(self, script: str, *args) -> None:
        """执行js脚本"""
        self.baseDriver.execute_script(script, args)

    def JsClick(self, args):
        """通过js执行点击"""
        self.ExcuteScript("arguments[0].click();", args)

    def ExhibitionElement(self, selector: str) -> None:
        """将元素显示到可见窗口中 """
        ele = self.locate_element(selector)
        js = "arguments[0].scrollIntoView();"
        self.baseDriver.execute_script(js, ele)

    def ScrollBy(self, *args):
        """滚动操作"""
        for i in list(args):
            get_js = f"window.scrollBy(0,{i});"  # 执行多个js脚本则需要用到scrollBy；表示再次下拉到300位置
            self.baseDriver.execute_script(get_js)  # 执行js脚本

    @_retrying
    def getALlPageText(self, selector: str) -> list:
        """获取整个页面的一组元素文本，包括没有显示在当前窗口的"""
        js = "return arguments[0].textContent"
        ele = self.locate_elements(selector)
        return [self.baseDriver.execute_script(js, i) for i in ele]

    def AddCookie(self, cookie):
        """设置cookie"""
        if isinstance(cookie, dict):
            self.baseDriver.add_cookie(cookie)
        else:
            key = cookie.split("=")[0]
            value = cookie.split("=")[1]
            self.baseDriver.add_cookie({"name": key, "value": value})

    def GetCookie(self, name):
        """获取指定key的cookie"""
        return self.baseDriver.get_cookie(name)

    def GetCookies(self):
        """获取当前会话的所有cookie"""
        return self.baseDriver.get_cookies()
