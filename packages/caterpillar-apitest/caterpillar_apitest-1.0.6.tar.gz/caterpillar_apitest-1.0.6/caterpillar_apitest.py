
import json
import logging
import requests
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
    def request(url="", headers=None, data=None, method="GET",**kwargs):
        method = method.strip().upper()
        response=None
        if method == "GET":
            if data:
                params=data
            else:
                params={}
            response = requests.get(url, params=params, headers=headers)
            log.info(f"接口请求url：{url}，请求方法method：{method}，请求返回状态码：status_code：{response.status_code}")
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers,**kwargs)
            log.info(f"接口请求url：{url}，请求方法method：{method}，请求返回状态码：status_code：{response.status_code}")
        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=headers)
            log.info(f"接口请求url：{url}，请求方法method：{method}，请求返回状态码：status_code：{response.status_code}")
        else:
            log.warning(f"目前请求方法支持post,get,put,delete，不区分大小写，当前请求方法不在上述之列，请求方法未：{method}")
        return response

    @staticmethod
    def save_response_to_case_data(case_id,response):
        if case_id not in ApiTest.case_data.keys():
            ApiTest.case_data[case_id]={}
        ApiTest.case_data[case_id]["headers"] = response.headers
        try:
            ApiTest.case_data[case_id]["data"] = json.loads(response.text)
        except Exception as e:
            log.warning(f"接口返回文本信息进行json格式化时出错，接口返回信息为：response.text:{response.text},格式化数据时报错信息为：{str(e)}")
            ApiTest.case_data[case_id]["data"] = {}
        ApiTest.case_data["status_code"]=response.status_code

    @staticmethod
    def deal_dependency(headers,data,dependencies):
        if not dependencies:
            log.info("当前接口对其他接口没有依赖")
            return headers,data
        dependencies=dependencies.strip()
        for dependency in dependencies.split(","):
            dependency=dependency.strip()
            if "=" not in dependency.strip():
                log.warning(f"接口对其他接口的依赖条件需要使用等号=赋值，当前依赖中未检测到=，所以这里将忽略此依赖，当前依赖信息为：{dependency}")
                continue
            src, dest = dependency.split("=")
            src = src.strip()
            dest = dest.strip()
            # 获取dest指定的值
            value = ApiTest.case_data
            for key in dest.split("."):
                key=key.strip()

                try:
                    value = value[key]
                except Exception as e:
                    log.warning(f"解析接口对其他接口的依赖时，在ApiTest.case_data中未找到对应的值，异常信息为：{str(e)}")
                    raise e

            # 将获取到的value赋值
            dependency_list = src.split(".")
            if dependency_list[0] == "headers":
                obj = headers
                for key in dependency_list[1:-1]:
                    if key not in obj:
                        obj[key] = {}
                    obj = obj[key]
                obj[dependency_list[-1]] = value

            if dependency_list[0] == "data":
                obj = data
                for key in dependency_list[1:-1]:
                    if key not in obj:
                        obj[key] = {}
                    obj = obj[key]
                obj[dependency_list[-1]] = value
        return headers, data

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

