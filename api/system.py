'''
Author: tansen
Date: 2024-02-24 20:07:57
LastEditors: Please set LastEditors
LastEditTime: 2024-02-25 13:25:24
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Description: 系统类
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''
import os
import time
import json
# import traceback

import webview
import numpy as np
import pandas as pd
from pypinyin import pinyin, Style

from src_py.config.config import Config
from src_py.config.log import Log

class System():
    window = None
    def __init__(self):
        self.log_info = "" 

    def system_py2js(self, func, info):
        '''调用js中挂载到window的函数'''
        infoJson = json.dumps(info)
        System.window.evaluate_js(f"{func}('{infoJson}')")

    def system_getAppInfo(self):
        '''程序基础配置信息'''
        return {
            'appName': Config.appName,  # 应用名称
            'appVersion': Config.appVersion  # 应用版本号
        }
    
    def log_info_callback(self, message):
        self.log_info += message + "\n"
        return self.log_info

    def system_open_file(self, encoding, sep):
        '''打开文件'''
        file_types = ['csv(*.csv;*.txt;*.dat;*.spext;*.tsv)']
        directory = ''
        try:
            self.encoding = encoding
            self.sep = sep
            file_types = tuple(file_types)
            self.result = System.window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=True, file_types=file_types)

            check_df = pd.read_csv(self.result[0], dtype=str, nrows=5, encoding=self.encoding, sep=self.sep)

            df_json = check_df.to_json(orient='records', force_ascii=False)

            return df_json
        except Exception as e:
            print(f"system_open_file error: {e}")

    def system_process(
        self,
        entity,
        entity_select,
        journal_number,
        date_entered,
        date_effective,
        date_select,
        user_enterd,
        user_updated,
        user_select,
        ami,
        line_desciption,
        currency,
        currency_select,
        amount,
        amount_select,
        account_number,
        account_description
    ):
        try:
            start_time = time.time()
            # 读取csv
            # df = pd.read_csv(self.result[0], dtype=str, encoding=self.encoding, sep=self.sep)
            chunk_size = 10_0000
            dfs = []
            rdr = pd.read_csv(self.result[0], chunksize=chunk_size, dtype=str, encoding=self.encoding, sep=self.sep)
            for chunk in rdr:
                dfs.append(chunk)
            df = pd.concat(dfs)
            Log.info("数据已加载")

            if entity_select == 'column':
                df.rename(columns={entity: 'Entity'}, inplace=True)
            if entity_select == 'input':
                df['Entity'] = entity
            df['Company Name'] = df['Entity']

            if date_select == 'equal':
                df.rename(columns={date_effective: 'Date Effective'}, inplace=True)
                df['Date Entered'] = df['Date Effective']
            if date_select == 'nequal':
                df.rename(columns={
                    date_effective: 'Date Effective',
                    date_entered: 'Date Entered'
                }, inplace=True)
            
            df['Date Effective'] = pd.to_datetime(df['Date Effective']).dt.strftime("%d/%m/%Y")
            df['Journal Number'] = df[journal_number] + '_' + df['Date Effective']

            if user_select == 'EN':
                if user_enterd == '':
                    df['UserID Entered'] = None
                if user_enterd != '':
                    df.rename(columns={user_enterd: 'UserID Entered'}, inplace=True)
                    df['Name of User Entered'] = df['UserID Entered']
                if user_updated == '':
                    df['UserID Updated'] = None
                if user_updated != '':
                    df.rename(columns={user_updated: 'UserID Updated'}, inplace=True)
                    df['Name of User Updated'] = df['UserID Updated']

            py_type = 'upper'
            if user_select == 'CN':
                if user_enterd == '':
                    df['UserID Entered'] = None
                if user_enterd != '':
                    df.rename(columns={user_enterd: 'UserID Entered'}, inplace=True)
                    df['UserID Entered'] = df['UserID Entered'].apply(
                        lambda value: pinyin(value, style=Style.NORMAL)[0] if py_type == "abbre" else ''.join(
                            [i[0].upper() for i in pinyin(value, style=Style.NORMAL)]))
                    df['Name of User Entered'] = df['UserID Entered']
                if user_updated == '':
                    df['UserID Updated'] = None
                if user_updated != '':
                    df.rename(columns={user_updated: 'UserID Updated'}, inplace=True)
                    df['UserID Updated'] = df['UserID Updated'].apply(
                        lambda value: pinyin(value, style=Style.NORMAL)[0] if py_type == "abbre" else ''.join(
                            [i[0].upper() for i in pinyin(value, style=Style.NORMAL)]))
                    df['Name of User Updated'] = df['UserID Updated']

            df['Auto Manual or Interface'] = ami

            df.rename(columns={
                line_desciption: 'Line Description',
                account_number: 'Account Number',
                account_description: 'Account Description'
            }, inplace=True)

            if currency_select == 'column':
                df.rename(columns={currency: 'Currency'}, inplace=True)
                df['Entity Currency (EC)'] = df['Currency']
            if currency_select == 'input':
                df['Currency'] = currency
                df['Entity Currency (EC)'] = df['Currency']

            if amount_select == 'amount':
                df.rename(columns={amount: 'Signed Amount EC'}, inplace=True)
            if amount_select == 'dc':
                debit = amount.split('|')[0]
                credit = amount.split('|')[1]
                df[debit] = df[debit].astype(float)
                df[credit] = df[credit].astype(float)
                df['Signed Amount EC'] = df[debit] - df[credit]

            # 插入模板列
            with open("./columnName.txt", "r", encoding="utf-8") as fp:
                column_names = fp.readlines()
            list_cs = [column_name.strip("\n") for column_name in column_names]
            insert_cols = [x for x in list_cs if x not in df.columns]
            for value in range(len(insert_cols)):
                df.insert(loc=value, column=insert_cols[value], value=None)
            Log.info("成功插入模板列")

            # 只保留模板列
            df = df.loc[:, list_cs]

            # 根据Amount添加DC的方向
            df['Signed Amount EC'] = df['Signed Amount EC'].astype(float)
            df['DC Indicator'] = np.where(df['Signed Amount EC'] >= 0, "D", "C")
            Log.info("成功添加DC Indicator")

            # 添加debit credit, 默认原币=本位币
            df['Unsigned Debit Amount EC'] = np.where(df['Signed Amount EC'] > 0, df['Signed Amount EC'], 0)
            df['Unsigned Credit Amount EC'] = np.where(df['Signed Amount EC'] < 0, df['Signed Amount EC']*-1, 0)
            df['Signed Journal Amount'] = df['Signed Amount EC']
            df["Unsigned Debit Amount"] = df['Unsigned Debit Amount EC']
            df["Unsigned Credit Amount"] = df['Unsigned Credit Amount EC']
            Log.info("成功添加debit,credit")

            # 转换日期格式为 dd/mm/yyyy
            # df['Date Effective'] = pd.to_datetime(df['Date Effective'])
            df['Date Effective'] = pd.to_datetime(df['Date Effective']).dt.strftime("%d/%m/%Y")
            # df['Date Entered'] = pd.to_datetime(df['Date Entered'])
            df['Date Entered'] = pd.to_datetime(df['Date Entered']).dt.strftime("%d/%m/%Y")
            Log.info("成功转换日期为 dd/mm/yyyy")

            # 添加 Financial Period
            df['Financial Period'] = df["Date Effective"].str.split("/").str[1]
            df['Financial Period'] = df['Financial Period'].astype("uint8")
            Log.info("成功添加 Financial Period")

            # 替换掉Line Description中的特殊符号,保留200位
            repl = {
                '，': '-', '。': '-', '？': '-', '：':'-', '；':'-', '、':'-',
                ',':'-', '"':'-', "'":'-', '”':'-', '’':'-', '|':'-', ':':'-', ';':'-',
                '\r':'-', '\n':'-'
            }
            for old_text, new_text in repl.items():
                df['Line Description'] = df['Line Description'].str.replace(old_text, new_text)
            df['Line Description'] = df['Line Description'].apply(lambda x: x[: 200])
            Log.info("成功清除特殊符号,且保留200位")

            # 排序
            df = df.sort_values(by='Journal Number', ascending=True, ignore_index=True)
            Log.info("排序成功")

            # 添加Line Number
            df_cols = [col for col in df.columns]
            jn = df.columns.get_loc('Journal Number')
            ln = df.columns.get_loc("Line Number")
            df["Line Number"] = int(1)
            df_len = len(df)
            df2arr = np.array(df)
            for value in range(1, df_len):
                if df2arr[value][jn] == df2arr[value-1][jn]:
                    df2arr[value][ln] = df2arr[value-1][ln] + 1
                else:
                    df2arr[value][ln] = int(1)
            arr2df = pd.DataFrame(df2arr)
            arr2df.columns = df_cols
            Log.info("成功添加Line Number")

            # 金额列保留两位小数
            df = df.round(
                {'Unsigned Debit Amount': 2, 'Unsigned Credit Amount': 2, "Signed Journal Amount": 2,
                "Unsigned Debit Amount EC": 2, "Unsigned Credit Amount EC": 2, "Signed Amount EC": 2})
            Log.info("金额列成功保留两位小数")

            # pivot, net 2 zero
            dirname = os.path.dirname(self.result[0])
            pt = pd.pivot_table(df, index=['Entity', 'Account Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            pt.to_excel(f"{dirname}/Pivot.xlsx", index=False)

            pt = pd.pivot_table(df, index=['Entity', 'Journal Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            pt.to_excel(f"{dirname}/Net2Zero.xlsx", index=False)

            # 写入txt
            df.to_csv(f'{dirname}/upload.txt', encoding='utf-16le', index=False, sep='|')
            Log.info('成功写入txt')

            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except FileNotFoundError as e:
            Log.error(e)
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except AttributeError as e:
            Log.error(e)
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except ValueError as e:
            Log.error(e)
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "cannot convert float NaN to integer":
                error_info['message'] = '未找到Signed Amount EC'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(e)
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
                # 'traceback': traceback.format_exc()
            }
            # 将错误信息转换为JSON字符串
            json_error = json.dumps(error_info, ensure_ascii=False, indent=2)
            return json_error
        