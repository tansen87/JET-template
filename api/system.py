#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Description: 系统类
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''
import os
import time
import json
from datetime import datetime
# import traceback

import webview
import numpy as np
import pandas as pd
from pypinyin import lazy_pinyin, pinyin, Style

from src_py.config.config import Config
from src_py.config.log import Log

class System():
    window = None

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
    
    def system_cn2pinyin(self, columns):
        ''' 将中文列替换为拼音 '''
        try:
            start_time = time.time()
            file_type = os.path.splitext(self.result[0])[1].lower()
            list_columns = [cols for cols in columns.split('|')]
            file_path = os.path.splitext(self.result[0])[0]
            current_time_str = datetime.now().strftime('%Y-%m-%d %H%M%S')
            py_type = 'upper'
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                repl_cols = pd.read_excel(self.result[0], dtype=str, engine='calamine', usecols=list_columns)
                for x in list_columns:
                    repl_cols[x] = repl_cols[x].astype(str)
                    repl_cols[x] = repl_cols[x].apply(
                        lambda value: pinyin(value, style=Style.NORMAL)[0] if py_type == "abbre" else ''.join(
                            [i[0].upper() for i in pinyin(value, style=Style.NORMAL)]
                        )
                    )
                repl_cols.to_excel(f'{file_path}-EN {current_time_str}.xlsx', index=False, engine='xlsxwriter')
            if file_type in ['.csv', 'tsv', '.dat', '.spext', '.txt']:
                repl_cols = pd.read_csv(self.result[0], dtype=str, encoding=self.encoding, sep=self.sep)
                for x in list_columns:
                    repl_cols[x] = repl_cols[x].astype(str)
                    repl_cols[x] = repl_cols[x].apply(
                        lambda value: pinyin(value, style=Style.NORMAL)[0] if py_type == "abbre" else ''.join(
                            [i[0].upper() for i in pinyin(value, style=Style.NORMAL)]
                        )
                    )
                repl_cols.to_csv(f'{file_path}-EN {current_time_str}.csv', index=False, sep=self.sep, encoding=self.encoding)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except AttributeError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
    
    def system_repl_char(self, columns):
        ''' 替换掉特殊符号 '''
        try:
            start_time = time.time()
            file_type = os.path.splitext(self.result[0])[1].lower()
            list_columns = [cols for cols in columns.split('|')]
            file_path = os.path.splitext(self.result[0])[0]
            current_time_str = datetime.now().strftime('%Y-%m-%d %H%M%S')
            repl = {
                '，': '-', '。': '-', '？': '-', '：':'-', '；':'-', '、':'-', '.':'-',
                ',':'-', '"':'-', "'":'-', '”':'-', '’':'-', '|':'-', ':':'-', ';':'-',
                '\r':'-', '\n':'-', '\\':'-', '/':'-'
            }
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                repl_cols = pd.read_excel(self.result[0], dtype=str, engine='calamine', usecols=list_columns)
                for x in list_columns:
                    for old_text, new_text in repl.items():
                        repl_cols[x] = repl_cols[x].str.replace(old_text, new_text)
                repl_cols.to_excel(f'{file_path}-replChar {current_time_str}.xlsx', index=False, engine='xlsxwriter')
            if file_type in ['.csv', 'tsv', '.dat', '.spext', '.txt']:
                repl_cols = pd.read_csv(self.result[0], dtype=str, encoding=self.encoding, sep=self.sep)
                for x in list_columns:
                    for old_text, new_text in repl.items():
                        repl_cols[x] = repl_cols[x].str.replace(old_text, new_text)
                repl_cols.to_csv(f'{file_path}-replChar {current_time_str}.csv', index=False, sep=self.sep, encoding=self.encoding)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except AttributeError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
    
    def system_repl_sf_char(self, columns, old_char, new_char):
        ''' 替换掉指定符号 '''
        try:
            start_time = time.time()
            file_type = os.path.splitext(self.result[0])[1].lower()
            list_columns = [cols for cols in columns.split('|')]
            file_path = os.path.splitext(self.result[0])[0]
            current_time_str = datetime.now().strftime('%Y-%m-%d %H%M%S')
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                repl_cols = pd.read_excel(self.result[0], dtype=str, engine='calamine', usecols=list_columns)
                for x in list_columns:
                    repl_cols[x] = repl_cols[x].str.replace(old_char, new_char)
                repl_cols.to_excel(f'{file_path}-replSfChar {current_time_str}.xlsx', index=False, engine='xlsxwriter')
            if file_type in ['.csv', '.tsv', '.dat', '.spext', '.txt']:
                repl_cols = pd.read_csv(self.result[0], dtype=str, encoding=self.encoding, sep=self.sep)
                for x in list_columns:
                    repl_cols[x] = repl_cols[x].str.replace(old_char, new_char)
                repl_cols.to_csv(f'{file_path}-replSfChar {current_time_str}.csv', index=False, sep=self.sep, encoding=self.encoding)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except AttributeError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error

    def system_open_file(self, encoding, sep):
        '''打开文件'''
        file_types = [
            'All files (*.*)',
            'CSV (*.csv;*.txt;*.dat;*.spec;*.tsv)',
            'Excel (*.xlsx;*.xlsb;*.xlsm)'
        ]
        directory = ''
        try:
            file_types = tuple(file_types)
            self.result = System.window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=True, file_types=file_types)
            file_type = os.path.splitext(self.result[0])[1].lower()
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                check_df = pd.read_excel(self.result[0], dtype=str, engine='calamine', nrows=5)
            if file_type in ['.csv', '.tsv', '.dat', '.spext', '.txt']:
                self.encoding = encoding
                self.sep = sep
                check_df = pd.read_csv(self.result[0], dtype=str, encoding=self.encoding, sep=self.sep, nrows=5)
            df_json = check_df.to_json(orient='records', force_ascii=False)

            return df_json
        except Exception as e:
            Log.error(repr(e))

    def system_process(
        self,
        entity,
        entity_select,
        entity_language,
        company,
        company_select,
        journal_number,
        journal_type,
        number_m_date,
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
        account_description,
        switch_value
    ):
        try:
            start_time = time.time()
            file_type = os.path.splitext(self.result[0])[1].lower()

            # 读取excel
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                df = pd.read_excel(self.result[0], dtype=str, engine='calamine')

            # 读取csv
            if file_type in ['.csv', '.tsv', '.dat', '.spext', '.txt']:
                chunk_size = 10_0000
                dfs = []
                rdr = pd.read_csv(
                    self.result[0], chunksize=chunk_size, dtype=str, encoding=self.encoding, sep=self.sep)
                for chunk in rdr:
                    dfs.append(chunk)
                df = pd.concat(dfs)
            Log.info("数据已加载")

            if entity_select == 'column':
                if entity_language == 'EN':
                    df.rename(columns={entity: 'Entity'}, inplace=True)
                if entity_language == 'CN':
                    df.rename(columns={entity: 'Entity'}, inplace=True)
                    df['Entity'] = df['Entity'].astype(str)
                    df['Entity'] = df['Entity'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.INITIALS)) if isinstance(value, str) else value)
                    df['Entity'] = df['Entity'].apply(lambda value: value.upper() if isinstance(value, str) else value)
            if entity_select == 'input':
                df['Entity'] = entity

            if company_select == '' or company == '':
                df['Company Name'] = df['Entity']
            if company_select == 'column':
                df.rename(columns={company: 'Company Name'}, inplace=True)
            if company_select == 'input':
                df['Company Name'] = company

            if date_select == 'equal':
                df.rename(columns={date_effective: 'Date Effective'}, inplace=True)
                df['Date Effective'] = pd.to_datetime(df['Date Effective'])
                # 添加 Financial Period
                df['Financial Period'] = df['Date Effective'].dt.month
                df['Financial Period'] = df['Financial Period'].astype("uint8")
                df['Date Effective'] = df['Date Effective'].dt.strftime("%d/%m/%Y")
                df['Date Entered'] = df['Date Effective']
            if date_select == 'nequal':
                df.rename(columns={
                    date_effective: 'Date Effective',
                    date_entered: 'Date Entered'
                }, inplace=True)
                df['Date Effective'] = pd.to_datetime(df['Date Effective'])
                # 添加 Financial Period
                df['Financial Period'] = df['Date Effective'].dt.month
                df['Financial Period'] = df['Financial Period'].astype("uint8")
                df['Date Effective'] = df['Date Effective'].dt.strftime("%d/%m/%Y")
                df['Date Entered'] = pd.to_datetime(df['Date Entered']).dt.strftime("%d/%m/%Y")
            Log.info("成功转换日期为 dd/mm/yyyy")

            if number_m_date == 'multi':
                df['Journal Number'] = df[journal_number] + '_' + df['Date Effective']
            if number_m_date == 'single':
                df.rename(columns={journal_number: 'Journal Number'}, inplace=True)

            if journal_type != '':
                df.rename(columns={journal_type: 'Journal Type'}, inplace=True)
            if journal_type == '':
                df['Journal Type'] = None

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

            if user_select == 'CN':
                if user_enterd == '':
                    df['UserID Entered'] = None
                if user_enterd != '':
                    df.rename(columns={user_enterd: 'UserID Entered'}, inplace=True)
                    # df['UserID Entered'] = df['UserID Entered'].astype(str)
                    df['UserID Entered'] = df['UserID Entered'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.NORMAL)) if isinstance(value, str) else value)
                    df['UserID Entered'] = df['UserID Entered'].apply(lambda value: value.upper() if isinstance(value, str) else value)
                    df['Name of User Entered'] = df['UserID Entered']
                if user_updated == '':
                    df['UserID Updated'] = None
                if user_updated != '':
                    df.rename(columns={user_updated: 'UserID Updated'}, inplace=True)
                    # df['UserID Updated'] = df['UserID Updated'].astype(str)
                    df['UserID Updated'] = df['UserID Updated'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.NORMAL)) if isinstance(value, str) else value)
                    df['UserID Updated'] = df['UserID Updated'].apply(lambda value: value.upper() if isinstance(value, str) else value)
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

            # 替换掉Line Description中的特殊符号,保留200位
            repl = {
                '，': '-', '。': '-', '？': '-', '：':'-', '；':'-', '、':'-', '.':'-',
                ',':'-', '"':'-', "'":'-', '”':'-', '’':'-', '|':'-', ':':'-', ';':'-',
                '\r':'-', '\n':'-', '\\':'-', '/':'-'
            }
            for old_text, new_text in repl.items():
                df['Line Description'] = df['Line Description'].str.replace(old_text, new_text)
            df['Line Description'] = df['Line Description'].apply(lambda x: x[: 200])
            Log.info("成功清除特殊符号,且保留200位")

            # 排序
            if not switch_value:
                df = df.sort_values(by='Journal Number', ascending=True)
            if switch_value:
                df = df.sort_values(by=['Entity','Journal Number'], ascending=[True, True])
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
            df = pd.DataFrame(df2arr)
            df.columns = df_cols
            Log.info("成功添加Line Number")

            # 金额列保留两位小数
            df = df.round(
                {'Unsigned Debit Amount': 2, 'Unsigned Credit Amount': 2, "Signed Journal Amount": 2,
                "Unsigned Debit Amount EC": 2, "Unsigned Credit Amount EC": 2, "Signed Amount EC": 2})
            Log.info("金额列成功保留两位小数")

            # pivot, net 2 zero
            file_path = os.path.splitext(self.result[0])[0]
            current_time_str = datetime.now().strftime('%Y-%m-%d %H%M%S')
            pt = pd.pivot_table(df, index=['Entity', 'Account Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            if len(pt) < 104_0000:
                pt.to_excel(f"{file_path}_pivot {current_time_str}.xlsx", index=False)
            else:
                pt.to_csv(f'{file_path}_pivot {current_time_str}.csv', index=False, sep='|')

            pt = pd.pivot_table(df, index=['Entity', 'Journal Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            if len(pt) < 104_0000:
                pt.to_excel(f"{file_path}_Net2Zero {current_time_str}.xlsx", index=False)
            else:
                pt.to_csv(f'{file_path}_Net2Zero {current_time_str}.csv', index=False, sep='|')

            # 写入txt
            df.to_csv(f'{file_path}_GL_uploadTemplate {current_time_str}.txt', index=False, sep='|')
            Log.info('成功写入txt')

            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except FileNotFoundError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except AttributeError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except ValueError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "cannot convert float NaN to integer":
                error_info['message'] = '未找到Signed Amount EC'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
                # 'traceback': traceback.format_exc()
            }
            # 将错误信息转换为JSON字符串
            json_error = json.dumps(error_info, ensure_ascii=False, indent=2)
            return json_error
        
    def system_process_specific(
        self,
        entity,
        entity_select,
        entity_language,
        company,
        company_select,
        journal_number,
        journal_type,
        number_m_date,
        date_entered,
        date_effective,
        date_select,
        user_enterd,
        user_updated,
        user_select,
        line_desciption,
        currency,
        currency_select,
        amount,
        amount_select,
        account_number,
        account_description,
        switch_value
    ):
        try:
            start_time = time.time()
            file_type = os.path.splitext(self.result[0])[1].lower()

            # 读取excel
            if file_type in ['.xlsx', '.xlsb', '.xlsm']:
                df = pd.read_excel(self.result[0], dtype=str, engine='calamine')

            # 读取csv
            if file_type in ['.csv', '.tsv', '.dat', '.spext', '.txt']:
                chunk_size = 10_0000
                dfs = []
                rdr = pd.read_csv(
                    self.result[0], chunksize=chunk_size, dtype=str, encoding=self.encoding, sep=self.sep)
                for chunk in rdr:
                    dfs.append(chunk)
                df = pd.concat(dfs)
            Log.info("数据已加载")

            if entity_select == 'column':
                if entity_language == 'EN':
                    df.rename(columns={entity: 'Entity'}, inplace=True)
                if entity_language == 'CN':
                    df.rename(columns={entity: 'Entity'}, inplace=True)
                    df['Entity'] = df['Entity'].astype(str)
                    df['Entity'] = df['Entity'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.INITIALS)) if isinstance(value, str) else value)
                    df['Entity'] = df['Entity'].apply(lambda value: value.upper() if isinstance(value, str) else value)
            if entity_select == 'input':
                df['Entity'] = entity

            if company_select == '' or company == '':
                df['Company Name'] = df['Entity']
            if company_select == 'column':
                df.rename(columns={company: 'Company Name'}, inplace=True)
            if company_select == 'input':
                df['Company Name'] = company

            if date_select == 'equal':
                df.rename(columns={date_effective: 'Date Effective'}, inplace=True)
                df['Date Effective'] = pd.to_datetime(df['Date Effective'])
                # 添加 Financial Period
                df['Financial Period'] = df['Date Effective'].dt.month
                df['Financial Period'] = df['Financial Period'].astype("uint8")
                df['Date Effective'] = df['Date Effective'].dt.strftime("%d/%m/%Y")
                df['Date Entered'] = df['Date Effective']
            if date_select == 'nequal':
                df.rename(columns={
                    date_effective: 'Date Effective',
                    date_entered: 'Date Entered'
                }, inplace=True)
                df['Date Effective'] = pd.to_datetime(df['Date Effective'])
                # 添加 Financial Period
                df['Financial Period'] = df['Date Effective'].dt.month
                df['Financial Period'] = df['Financial Period'].astype("uint8")
                df['Date Effective'] = df['Date Effective'].dt.strftime("%d/%m/%Y")
                df['Date Entered'] = pd.to_datetime(df['Date Entered']).dt.strftime("%d/%m/%Y")
            Log.info("成功转换日期为 dd/mm/yyyy")

            if number_m_date == 'multi':
                df['Journal Number'] = df[journal_number] + '_' + df['Date Effective']
            if number_m_date == 'single':
                df.rename(columns={journal_number: 'Journal Number'}, inplace=True)

            if journal_type != '':
                df.rename(columns={journal_type: 'Journal Type'}, inplace=True)

            if user_select == 'EN':
                if user_enterd != '':
                    df.rename(columns={user_enterd: 'UserID Entered'}, inplace=True)
                    df['Name of User Entered'] = df['UserID Entered']
                if user_updated != '':
                    df.rename(columns={user_updated: 'UserID Updated'}, inplace=True)
                    df['Name of User Updated'] = df['UserID Updated']

            if user_select == 'CN':
                if user_enterd != '':
                    df.rename(columns={user_enterd: 'UserID Entered'}, inplace=True)
                    # df['UserID Entered'] = df['UserID Entered'].astype(str)
                    df['UserID Entered'] = df['UserID Entered'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.NORMAL)) if isinstance(value, str) else value)
                    df['UserID Entered'] = df['UserID Entered'].apply(lambda value: value.upper() if isinstance(value, str) else value)
                    df['Name of User Entered'] = df['UserID Entered']
                if user_updated != '':
                    df.rename(columns={user_updated: 'UserID Updated'}, inplace=True)
                    # df['UserID Updated'] = df['UserID Updated'].astype(str)
                    df['UserID Updated'] = df['UserID Updated'].apply(
                        lambda value: ''.join(lazy_pinyin(value, style=Style.NORMAL)) if isinstance(value, str) else value)
                    df['UserID Updated'] = df['UserID Updated'].apply(lambda value: value.upper() if isinstance(value, str) else value)
                    df['Name of User Updated'] = df['UserID Updated']

            df.rename(columns={
                line_desciption: 'Line Description',
                account_number: 'Account Number',
                account_description: 'Account Description'
            }, inplace=True)

            if currency_select == 'column':
                df.rename(columns={currency: 'Currency'}, inplace=True)
                df['Entity Currency (EC)'] = df['Currency']

            if amount_select == 'amount':
                df.rename(columns={amount: 'Signed Amount EC'}, inplace=True)
            if amount_select == 'dc':
                debit = amount.split('|')[0]
                credit = amount.split('|')[1]
                df[debit] = df[debit].astype(float)
                df[credit] = df[credit].astype(float)
                df['Signed Amount EC'] = df[debit] - df[credit]

            # 获取输入列
            if journal_type == '' and user_enterd != '' and user_updated != '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'UserID Entered', 'Name of User Entered',
                    'UserID Updated', 'Name of User Updated', 'Date Effective', 'Date Entered', 'Line Description',
                    'Signed Amount EC', 'Account Number', 'Account Description']]
            if journal_type == '' and user_enterd == '' and user_updated != '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'UserID Updated', 'Name of User Updated', 
                    'Date Effective', 'Date Entered', 'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description']]
            if journal_type == '' and user_enterd != '' and user_updated == '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'UserID Entered', 'Name of User Entered',
                    'Date Effective', 'Date Entered', 'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description']]
            if journal_type == '' and user_enterd == '' and user_updated == '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'Date Effective', 'Date Entered', 
                    'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description']]
            if journal_type != '' and user_enterd == '' and user_updated == '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'Date Effective', 'Date Entered', 'Journal Type',
                    'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description']]
            if journal_type != '' and user_enterd != '' and user_updated == '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'Date Effective', 'Date Entered', 'Journal Type',
                    'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description',
                    'UserID Entered', 'Name of User Entered']]
            if journal_type != '' and user_enterd == '' and user_updated != '':
                df = df.loc[:, [
                    'Entity', 'Company Name', 'Journal Number', 'Date Effective', 'Date Entered', 'Journal Type',
                    'Line Description', 'Signed Amount EC', 'Account Number', 'Account Description',
                    'UserID Updated', 'Name of User Updated']]

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

            # 替换掉Line Description中的特殊符号,保留200位
            repl = {
                '，': '-', '。': '-', '？': '-', '：':'-', '；':'-', '、':'-', '.':'-',
                ',':'-', '"':'-', "'":'-', '”':'-', '’':'-', '|':'-', ':':'-', ';':'-',
                '\r':'-', '\n':'-', '\\':'-', '/':'-'
            }
            for old_text, new_text in repl.items():
                df['Line Description'] = df['Line Description'].str.replace(old_text, new_text)
            df['Line Description'] = df['Line Description'].apply(lambda x: x[: 200])
            Log.info("成功清除特殊符号,且保留200位")

            # 排序
            if not switch_value:
                df = df.sort_values(by='Journal Number', ascending=True)
            if switch_value:
                df = df.sort_values(by=['Entity','Journal Number'], ascending=[True, True])
            Log.info("排序成功")

            # 添加Line Number
            df["Line Number"] = int(1)
            df_cols = [col for col in df.columns]
            jn = df.columns.get_loc('Journal Number')
            ln = df.columns.get_loc("Line Number")
            df_len = len(df)
            df2arr = np.array(df)
            for value in range(1, df_len):
                if df2arr[value][jn] == df2arr[value-1][jn]:
                    df2arr[value][ln] = df2arr[value-1][ln] + 1
                else:
                    df2arr[value][ln] = int(1)
            df = pd.DataFrame(df2arr)
            df.columns = df_cols
            Log.info("成功添加Line Number")

            # 金额列保留两位小数
            df = df.round(
                {'Unsigned Debit Amount': 2, 'Unsigned Credit Amount': 2, "Signed Journal Amount": 2,
                "Unsigned Debit Amount EC": 2, "Unsigned Credit Amount EC": 2, "Signed Amount EC": 2})
            Log.info("金额列成功保留两位小数")

            # pivot, net 2 zero
            file_path = os.path.splitext(self.result[0])[0]
            current_time_str = datetime.now().strftime('%Y-%m-%d %H%M%S')
            dirname = os.path.dirname(self.result[0])
            pt = pd.pivot_table(df, index=['Entity', 'Account Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            if len(pt) < 104_0000:
                pt.to_excel(f"{file_path}_pivot {current_time_str}.xlsx", index=False)
            else:
                pt.to_csv(f'{file_path}_pivot {current_time_str}.csv', index=False, sep='|')

            pt = pd.pivot_table(df, index=['Entity', 'Journal Number'], values='Signed Amount EC', aggfunc='sum')
            pt.reset_index(inplace=True)
            if len(pt) < 104_0000:
                pt.to_excel(f"{file_path}_Net2Zero {current_time_str}.xlsx", index=False)
            else:
                pt.to_csv(f'{file_path}_Net2Zero {current_time_str}.csv', index=False, sep='|')

            # 写入txt
            df.to_csv(f'{file_path}_GL_uploadTemplate_sf {current_time_str}.txt', index=False, sep='|')
            Log.info('成功写入txt')

            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_rounded = round(elapsed_time, 2)
            return elapsed_time_rounded
        except FileNotFoundError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except AttributeError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "'API' object has no attribute 'result'":
                error_info['message'] = '未选择文件'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except ValueError as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
            }
            if error_info['message'] == "cannot convert float NaN to integer":
                error_info['message'] = '未找到Signed Amount EC'
            json_error = json.dumps(error_info['message'], ensure_ascii=False, indent=2)
            return json_error
        except Exception as e:
            Log.error(repr(e))
            error_info = {
                'type': type(e).__name__,
                'message': str(e),
                # 'traceback': traceback.format_exc()
            }
            # 将错误信息转换为JSON字符串
            json_error = json.dumps(error_info, ensure_ascii=False, indent=2)
            return json_error