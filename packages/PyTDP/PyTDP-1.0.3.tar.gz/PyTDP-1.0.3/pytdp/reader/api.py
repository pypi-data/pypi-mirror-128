# -*- coding: utf-8 -*-
from googletrans import Translator
import pandas as pd
import time
import os
from IPython.display import clear_output
import re
from copy import deepcopy
import glob
from chardet import detect 
from pytdp.bases.api import Base

"""
[Function for translating Japanese to English]
"""
def translate_ja_to_en(text):
    # wait a second for using web api
    time.sleep(1)
    translator = Translator()

    translation = translator.translate(text, src='ja', dest="en")
    translation = translation.text.replace(' ', '_')
    translation = translation.replace('-', '_')
    translation = translation.replace('+', 'plus')
    translation = translation.replace('*', 'mul').lower()
    return translation

def num2words(num):
    nums_20_90 = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
    nums_0_19 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight',"Nine",
                'Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen',
                'Seventeen','Eighteen','Nineteen']
    nums_dict = {100: 'hundred',1000:'thousand', 1000000:'million', 1000000000:'billion'}
    if num < 20: return nums_0_19[num]
    if num < 100: return nums_20_90[num//10-2] + ('' if num%10 == 0 else '_' + nums_0_19[num%10])
    # find the largest key smaller than num
    maxkey = max([key for key in nums_dict.keys() if key <= num])
    return num2words(num//maxkey) + '_' + nums_dict[maxkey] + ('' if num%maxkey == 0 else '_' + num2words(num%maxkey))

def read_files(data_path_list:list) -> dict:
    extension_lst = list(map(lambda x: x.split('.')[-1], data_path_list))
    arg_fomula = f'result = {{'
    for i in range(len(data_path_list)):
        clear_output()
        print(f'{i + 1}/{len(data_path_list)}')
        s = data_path_list[i].split('/')[-1].split('.')[0]

        # if number in strings, change english words
        # int_to_str = []
        for j in sorted(list(set(re.compile(r"\d+").findall(s))), reverse = True):
            s = s.replace(j, num2words(int(j)))

        local_arg_name = translate_ja_to_en(s)
        local_arg_fomula = ''
        # blanch extension
        if extension_lst[i] == 'csv': local_arg_fomula += f'{local_arg_name} = pd.DataFrame(pd.read_csv("{data_path_list[i]}"))' 
        elif extension_lst[i] == 'xlsx': local_arg_fomula += f'{local_arg_name} = pd.read_excel("{data_path_list[i]}", sheet_name = None)' 
        exec(local_arg_fomula)
        arg_fomula += f'"{local_arg_name}" : {local_arg_name},'
    arg_fomula += '}'
    exec(arg_fomula)
    return eval('result')

class Tdp_reader(Base):
    def __init__(self, data_list_or_directory, working_directory):
        super().__init__()
        self.working_directory = working_directory 
        self.data = {}
        if type(data_list_or_directory) == list: self.data = read_files(data_list_or_directory)
        elif type(data_list_or_directory) == str: self._load_file(data_directory = data_list_or_directory, recursive = True)
        else : print('引数が適切ではありません。')

        self.key = list(self.data.keys())
        self.FIXED_DATA = deepcopy(self.data)

    def _get_list_file_path(self, data_directory = os.getcwd(), recursive = True):
        # データの取得
        extension = ['txt', 'csv', 'xlsx']
        file_path_list = [f for e in extension for f in glob.glob(f'{data_directory}/**.{e}', recursive = True)]
        return file_path_list

    def _load_file(self, data_directory, recursive):
        # テキストデータの場合の処理 => csv変換して保存するまで(db保存を一応しとく)
        self.data = {}
        i = 0
        file_path_list = self._get_list_file_path(data_directory = data_directory, recursive = recursive)
        for p in file_path_list:
            clear_output()
            print(f'{i + 1}/{len(file_path_list)}')
            i += 1
            ############################
            # s = p.split('/')[-1].split('.')[0]

            # if number in strings, change english words
            # int_to_str = []
            # for j in sorted(list(set(re.compile(r"\d+").findall(s))), reverse = True): s = s.replace(j, num2words(int(j)))

            # local_arg_name = translate_ja_to_en(s)
            local_arg_name = p.split('/')[-1].split('.')[0]
            #############################
            # テキストデータの場合の処理 => csv変換して保存するまで(db保存を一応しとく)
            if p.split('.')[-1] == 'txt':
                with open(p, 'rb') as f:  # バイナリファイルとして読み込みオープン
                    b = f.read()  # ファイルから全データを読み込み
                    enc = detect(b)  # 読み込んだデータdetect関数に渡して判定する
                #print(enc) #文字コードの確認ができる
                if enc['encoding'] == 'CP932': encode = 'CP932'
                elif enc['encoding'] == 'utf-8': encode = 'utf-8'
                else: encode = 'SHIFT_JIS'
                with open(p, mode = 'r', encoding = encode) as f:
                    #print(p.split('/')[-1].split('.')[0]) # どのファイルを現在操作しているかを確認できる
                    dt = f.readlines()
                    dt_columns = dt[0].split('\n')[0].split('\t')
                    dt_lis = []
                    for d in dt[1:]: dt_lis.append(d.split('\n')[0].split('\t'))
                    self.data[local_arg_name] = pd.DataFrame(dt_lis, columns = dt_columns)
            elif p.split('.')[-1] == 'xlsx':
                tmp_data_dict = pd.read_excel(p, sheet_name = None)
                for key in tmp_data_dict.keys():
                    self.data[key] = tmp_data_dict[key]
            elif p.split('.')[-1] == 'csv': self.data[local_arg_name] = pd.read_csv(p, encoding='SHIFT_JIS')    
