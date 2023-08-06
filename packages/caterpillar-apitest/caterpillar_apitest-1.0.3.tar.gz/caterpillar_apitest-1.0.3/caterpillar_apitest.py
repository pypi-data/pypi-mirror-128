
import json
import logging
from pathlib import Path
from openpyxl import load_workbook
from caterpillar_log import logger
log=logging.getLogger("caterpillar_log")



class ApiTest(object):
    """
    基于pytest的数据驱动的接口自动化框架
    数据驱动：
        文件类型：         .xlsx
        xlsx文件头字段：    case_id       case_name       url                  method      headers     data        dependency     assert      setup                        teardown                   mark
        xlsx文件头含义      用例id         用例名称        接口url(不含ip:port)    方法        头部信息      body体      数据依赖         断言        接口执行之前函数自定义函数名      接口执行之后的自定义函数名      标记

    存储接口数据的结构体，case_id需要保持唯一性，实例如下：
        case_data={
            "case_id_1":{
                "headers":{},
                "data":{},
                "response":{},
                "status_code":200
            },
            "case_id_2":{
                "headers":{},
                "data":{},
                "response":{},
                "status_code":200
            }
        }
    """
    case_data={}

    @staticmethod
    def get_all_xlsx_files(current_file,current_test_datas_dir):
        xlsx_files=[]
        test_datas_dir=Path(current_file).resolve().parent / current_test_datas_dir
        for xlsx_file in test_datas_dir.iterdir():
            if str(xlsx_file).endswith(".xlsx"):
                xlsx_files.append(xlsx_file)
        return xlsx_files

    @staticmethod
    def get_all_test_datas(current_file,current_test_datas_dir):
        test_datas=[]
        for xlsx in ApiTest.get_all_xlsx_files(current_file,current_test_datas_dir):
            workbook = load_workbook(xlsx)
            all_sheets=workbook.get_sheet_names()
            for sheet_name in all_sheets:
                worksheet=workbook.get_sheet_by_name(sheet_name)
                for row in worksheet.rows:
                    if "case_id" in row[0].value:
                        continue
                    test_datas.append([elem.value for elem in row])
        return test_datas

    @staticmethod
    def loads(data):
        try:
            data_new=json.loads(data)
        except Exception as e:
            log.warning(f"在执行json.loads(data)时报错，返回空字典，data为：{data}，异常信息为{str(e)}")
            data_new={}
        return data_new


    @staticmethod
    def api_assert(assert_str):
        """
        xlsx 文件中的断言列，为字符串，直接转换为可以进行assert断言的语句
        :param assert_str: 字符串
        :return:
        """
        op=ApiTest.get_op(assert_str)
        if not op:
            raise ValueError("无法识别断言字符串，请联系hitredrose@163.com进行扩展开发支持......")

    @staticmethod
    def get_op(assert_str):
        if "==" in assert_str:
            return "=="
        elif ">=" in assert_str:
            return ">="
        elif "<=" in assert_str:
            return "<="
        elif "!=" in assert_str:
            return "!="
        elif " not in " in assert_str:
            return " not in "
        elif " in " in assert_str:
            return " in "
        elif " is not " in assert_str:
            return " is not "
        elif " is " in assert_str:
            return " is "
        else:
            return None

