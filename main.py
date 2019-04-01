#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import os
import zipfile
import datetime
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""
        get SystemAnswer graph download as csv and png
        """)
    parser.add_argument('--start_date', type=str, required=True, default=datetime.datetime.today().strftime("%Y/%m/%d"), nargs='?', 
        help="""
        specify a start date of data.
        Style: YYYY/MM/DD
    """)
    parser.add_argument('--end_date', type=str, required=True, default=datetime.datetime.today().strftime("%Y/%m/%d"), nargs='?', 
        help="""
        specify a end date of data.
        Style: YYYY/MM/DD
    """)
    return vars(parser.parse_args())


def set_inputfield(inputfield, options):
    inputfield.clear()
    inputfield.send_keys(options)
    time.sleep(0.3)

def set_selectfield(inputfield, options):
    selectfield = Select(inputfield)
    selectfield.select_by_value(options)
    time.sleep(0.3)

def click_btn(inputbtn):
    inputbtn.click()
    time.sleep(1)

def get_graphoption(startdate, enddate, bandwidth):
    graphoptions = {}

    graphoptions['start_date'] = startdate + " 00:00"
    graphoptions['end_date']   = enddate + " 23:59" 
        
    graphoptions['graph_draw_cf'] = "max"
    # graphoptions['graph_draw_cf'] = "min"
    # graphoptions['graph_draw_cf'] = "avg"
                
    if bandwidth == "1000M" and bandwidth == "1G":
        graphoptions['llimit'] = "auto"
        graphoptions['lunit'] = "M"
        graphoptions['ulimit'] = "1000"
        graphoptions['uunit'] = "M"
    elif bandwidth == "100M":
        graphoptions['llimit'] = "auto"
        graphoptions['lunit'] = "M"
        graphoptions['ulimit'] = "100"
        graphoptions['uunit'] = "M"
    elif bandwidth == "10M":
        graphoptions['llimit'] = "auto"
        graphoptions['lunit'] = "M"
        graphoptions['ulimit'] = "10"
        graphoptions['uunit'] = "M"
    elif bandwidth == "1M":
        graphoptions['llimit'] = "auto"
        graphoptions['lunit'] = "M"
        graphoptions['ulimit'] = "1"
        graphoptions['uunit'] = "M"
    else:
        graphoptions['llimit'] = "auto"
        graphoptions['lunit'] = "M"
        graphoptions['ulimit'] = "auto"
        graphoptions['uunit'] = "M"

    return graphoptions


class ChromeBrowswer:
    def __init__(self):
        # Chromeオプション
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1024,768')

        self.driver = webdriver.Chrome(options=options)

    def login(self, logininfo):
        self.baseurl = logininfo['baseurl']
        self.username = logininfo['username']
        self.userpass = logininfo['userpass']

        self.driver.get(self.baseurl)
        self.parentwindow = self.driver.current_window_handle

        set_inputfield( self.driver.find_element_by_id('UserName'), self.username )
        set_inputfield( self.driver.find_element_by_id('Password'), self.userpass )
        click_btn( self.driver.find_element_by_xpath( "//*[@id='ContentsLoginPrompt']/table/tbody/tr[3]/td[2]/input") )

    def drow_graph(self, hostid, graphid):
        self.driver.switch_to.window( self.parentwindow )
        self.driver.execute_script( "NodeSelectGraph(%s,%s)" % (hostid, graphid) )
        time.sleep(1)

    def change_graph_options(self, graphoptions):
        # グラフのiframeにDOMを移動
        self.driver.switch_to.frame( self.driver.find_element_by_id('MainIframe'))
        # 開始日時
        set_inputfield( self.driver.find_element_by_id('graph_start'), graphoptions['start_date'] )
        # 終了日時
        set_inputfield( self.driver.find_element_by_id('graph_end'), graphoptions['end_date'] )
        # 描画方法
        set_selectfield( self.driver.find_element_by_id('graph_draw_cf'), graphoptions['graph_draw_cf'] )
        # 縦軸最小値
        set_inputfield( self.driver.find_element_by_id('llimit'), graphoptions['llimit'] )
        # 縦軸最小値単位
        set_selectfield( self.driver.find_element_by_id('lunit'), graphoptions['lunit'])
        # 縦軸最大値
        set_inputfield( self.driver.find_element_by_id('ulimit'), graphoptions['ulimit'])
        # 縦軸最大値単位
        set_selectfield( self.driver.find_element_by_id('uunit'), graphoptions['uunit'])
        # 更新
        click_btn( self.driver.find_element_by_xpath( "//*[@id='frmMain']/table/tbody/tr[3]/td[7]/input" ) )

        self.driver.switch_to.window( self.parentwindow )
    
    def download_graph(self, filename):
        # グラフのiframeにDOMを移動
        self.driver.switch_to.frame( self.driver.find_element_by_id('MainIframe'))

        url = self.driver.find_element_by_xpath( "//*[@id='Contents']/div[3]/div/img" ).get_attribute("src")
        
        js = """
        var getBinaryResourceText = function(url) {
            var req = new XMLHttpRequest();
            req.open('GET', url, false);
            req.overrideMimeType('text/plain; charset=x-user-defined');
            req.send(null);
            if (req.status != 200) return '';

            var filestream = req.responseText;
            var bytes = [];
            for (var i = 0; i < filestream.length; i++){
                bytes[i] = filestream.charCodeAt(i) & 0xff;
            }

            return bytes;
        }
        """
        js += "return getBinaryResourceText(\"{url}\");".format(url=url)
        data_bytes = self.driver.execute_script( js )

        file_path = os.path.dirname(filename)
        if not os.path.exists(file_path):
          os.makedirs(file_path)

        # PNGダウンロード
        with open(filename, 'wb') as f:
           f.write(bytes(data_bytes))
        
        self.driver.switch_to.window( self.parentwindow )

    def download_csv(self, filename):
        # グラフのiframeにDOMを移動
        self.driver.switch_to.frame( self.driver.find_element_by_id('MainIframe'))

        url = self.driver.find_element_by_xpath( "//*[@id='Contents']/div[2]/div/a[2]" ).get_attribute("href")
        
        js = """
        var getBinaryResourceText = function(url) {
            var req = new XMLHttpRequest();
            req.open('GET', url, false);
            req.overrideMimeType('text/plain; charset=x-user-defined');
            req.send(null);
            if (req.status != 200) return '';

            var filestream = req.responseText;
            var bytes = [];
            for (var i = 0; i < filestream.length; i++){
                bytes[i] = filestream.charCodeAt(i) & 0xff;
            }

            return bytes;
        }
        """
        js += "return getBinaryResourceText(\"{url}\");".format(url=url)
        data_bytes = self.driver.execute_script( js )

        file_path = os.path.dirname(filename)
        if not os.path.exists(file_path):
          os.makedirs(file_path)

        # PNGダウンロード
        with open(filename, 'wb') as f:
           f.write(bytes(data_bytes))
        
        compFile = zipfile.ZipFile( filename.replace(".csv", ".zip"), 'w', zipfile.ZIP_DEFLATED )
        compFile.write( filename )
        compFile.close()
        os.remove( filename )

        self.driver.switch_to.window( self.parentwindow )

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    # 変数定義
    parse_args = parse_command_line_args()
    start_date = parse_args['start_date']
    end_date = parse_args['end_date']

    # システム情報/ユーザ情報読み込み
    logininfo = json.load(open("settings/login.json", "r", encoding='utf-8'))
    nodeinfo  = json.load(open("settings/node.json", "r", encoding='utf-8'))

    # ブラウザ開始
    cb = ChromeBrowswer( )

    # サイトログイン
    cb.login( logininfo )

    for nodeinfo in nodeinfo["nodelist"]:
        if start_date == end_date:
            pngfile = start_date.replace("/", "") + "_" + nodeinfo["hostname"] + ".png"
            csvfile = start_date.replace("/", "") + "_" + nodeinfo["hostname"] + ".csv"
        else:
            pngfile = start_date.replace("/", "") + "-" + end_date.replace("/", "") + "_" + nodeinfo["hostname"] + ".png"
            csvfile = start_date.replace("/", "") + "-" + end_date.replace("/", "") + "_" + nodeinfo["hostname"] + ".csv"

        # グラフを表示
        cb.drow_graph( nodeinfo["hostid"], nodeinfo["graphid"] )
        # グラフ条件の変更
        cb.change_graph_options( get_graphoption(start_date, end_date, nodeinfo['bandwidth']) )
        # グラフ保存
        cb.download_graph( "./outputs/" + pngfile )
        # グラフ元データ保存
        cb.download_csv( "./outputs/CSV/" + csvfile ) 

    # ブラウザ終了
    cb.close()