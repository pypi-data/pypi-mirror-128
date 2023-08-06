import os
import time
import LibHanger.Library.uwLogger as Logger
from os import path
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.android.webdriver import WebDriver
from pandas.core.frame import DataFrame
from LibHanger.Library.uwGetter import getPlatform
from LibHanger.Library.uwGlobals import *
from Scrapinger.Library.scrapingConfig import scrapingConfig

class baseWebBrowserController:

    """
    ブラウザーコントローラー基底クラス
    """ 
    
    def __init__(self, _config:scrapingConfig):

        """ 
        コンストラクタ
        """

        # 共通設定のセット
        self.config = _config

        # Webドライバーインスタンス格納用変数初期化
        self.wDriver:WebDriver = None

        # コールバック関数
        self.cbCreateSearchResultDictionaryByWebDriver = baseWebBrowserController.createSearchResultDictionaryByWebDriver
        self.cbCreateSearchResultDictionaryByBeutifulSoup = baseWebBrowserController.createSearchResultDictionaryByBeutifulSoup
        
        pass
    
    @Logger.loggerDecorator('Get WebDriverPath')
    def getWebDriverPath(self, _webDriverPath:scrapingConfig.settingValueStruct.WebDriverPath):
        
        """ 
        Webドライバーパスを取得する
        
        Parameters
        ----------
        _webDriverPath : scrapingConfig.settingValueStruct.WebDriverPath
            WebDriverパス列挙体
        """
        
        webDriverPath = ''
        if getPlatform() == gv.platForm.win:
            webDriverPath = os.path.join(path.dirname(self.config.scriptFilePath), _webDriverPath.WebDriverPathWin)
        elif getPlatform() == gv.platForm.linux:
            webDriverPath = os.path.join(path.dirname(self.config.scriptFilePath), _webDriverPath.WebDriverPathLinux)
        elif getPlatform() == gv.platForm.mac:
            webDriverPath = os.path.join(path.dirname(self.config.scriptFilePath), _webDriverPath.WebDriverPathMac)

        # WebDriverPathログ出力
        Logger.logging.info(webDriverPath)

        # WebDriverPathを返す
        return webDriverPath

    @Logger.loggerDecorator('Get WebDriver')
    def getWebDriver(self):

        """
        ブラウザ操作用のWebドライバーを取得する

        Parameters
        ----------
        config : scrapingConfig
            共通設定クラス
        """

        pass
    
    @Logger.loggerDecorator('Setting BrowserSize')
    def changeBrowserSize(self, width:str, height:str):

        """
        ブラウザのウィンドウサイズを変更する

        Parameters
        ----------
        width : str
            ウィンドウ横幅(px)
        height : str
            ウィンドウ縦幅(px)
        """

        # Browserサイズログ出力
        Logger.logging.info('BrowserSize:{} x {}'.format(width, height))
        
        # ウィンドウサイズ変更
        self.wDriver.set_window_size(width, height)
        
    @Logger.loggerDecorator('Load WebPage')
    def loadPage(self, url:str):

        """
        指定URLのページ内容を取得する

        Parameters
        ----------
        url : str
            ページURL
        """
        
        # URLログ出力
        Logger.logging.info('TargetUrl]' + url)
        
        # ページ内容取得
        self.wDriver.get(url)

    @Logger.loggerDecorator('Normal-Delay')
    def Delay(self):

        """
        指定秒数待機する

        Parameters
        ----------
        None

        """

        # DelayTime-ログ出力
        Logger.logging.info('DelayTime {} Seconds'.format(self.config.DelayTime))

        # 待機
        time.sleep(self.config.DelayTime)
    
    @Logger.loggerDecorator('WebDriver-Delay')
    def WebDriverWait(self, locater:str):

        """
        WebDriverWaitを使った待機及び対象エレメントの取得

        Parameters
        ----------
        locater : str
            By.ID,By.CSS_SELECTOR,By.CLASS_NAME,By.TAG_NAME
        """

        # DelayTime-ログ出力
        Logger.logging.info('WebDriverDelayTime {} Seconds'.format(self.config.WebDriverTimeout))

        # タイムアウト設定
        self.wDriver.implicitly_wait(self.config.WebDriverTimeout)
        # 検索結果エレメント取得
        if locater == By.CSS_SELECTOR:
            element = self.wDriver.find_element_by_css_selector(self.config.DelayWaitElement)
        elif locater == By.CLASS_NAME:
            element = self.wDriver.find_element_by_class_name(self.config.DelayWaitElement)
        elif locater == By.TAG_NAME:
            element = self.wDriver.find_element_by_tag_name(self.config.DelayWaitElement)

        return element
    
    @Logger.loggerDecorator('Create SearchResultDictionary')
    def createSearchResultDictionary(self, dfItemInfo:DataFrame, dictItemInfoRowCount:int, locater:str = By.CSS_SELECTOR) -> dict:
            
            """
            スクレイピング結果をディクショナリで返す

            Parameters
            ----------
            dfItemInfo : DataFrame
                列情報DataFrame
            dictItemInfoRowCount : int
                生成中のディクショナリ行数
            locater : str
                By.ID,By.CSS_SELECTOR,By.CLASS_NAME,By.TAG_NAME
            """
            
            if self.config.ScrapingType == self.config.settingValueStruct.ScrapingType.selenium.value:
                # 待機
                element = self.WebDriverWait(locater)
                # スクレイピング
                return self.cbCreateSearchResultDictionaryByWebDriver(self, element, dfItemInfo, dictItemInfoRowCount)
            elif self.config.ScrapingType == self.config.settingValueStruct.ScrapingType.beutifulSoup.value:
                # 待機
                self.Delay(self.config)
                # スクレイピング
                soup:BeautifulSoup = self.scrapingWithBeautifulSoup()
                return self.cbCreateSearchResultDictionaryByBeutifulSoup(self, soup, dfItemInfo, dictItemInfoRowCount)
    
    @Logger.loggerDecorator('Create SearchResultDictionary By WebDriver')
    def createSearchResultDictionaryByWebDriver(self, element, dfItemInfo:DataFrame, dictItemInfoRowCount:int) -> dict:

        """
        WebDriverを使用してスレイピング結果からDictionaryを生成する(デリゲート用関数)

        Parameters
        ----------
        element : any
            スクレイピング結果
        dfItemInfo : DataFrame
            取得対象DataFrame(列情報)
        config : scrapingerConfig
            共通設定クラス
        dictItemInfoRowCount : int
            取得対象Dictionary現在行数
        
        Notes
        -----
            selenium用データ取得メソッド
            派生クラスで個別処理を実装する
        """
        
        pass

    @Logger.loggerDecorator('Create SearchResultDictionary By BeutifulSoup') 
    def createSearchResultDictionaryByBeutifulSoup(self, soup, dfItemInfo:DataFrame, dictItemInfoRowCount:int) -> dict:
        
        """
        ByBeutifulSoupを使用してスレイピング結果からDictionaryを生成する(デリゲート用関数)

        Parameters
        ----------
        soup : BeautifulSoup
            スクレイピング結果
        dfItemInfo : DataFrame
            取得対象DataFrame(列情報)
        config : scrapingerConfig
            共通設定クラス
        dictItemInfoRowCount : int
            取得対象Dictionary現在行数

        Notes
        -----
            BeautifulSoup用データ取得メソッド
            派生クラスで個別処理を実装する
        """
        
        pass
    
    @Logger.loggerDecorator('Create PandasData') 
    def createPandasData(self, dfItemInfo:DataFrame, dictItemInfo:dict, keys:list) -> DataFrame:

        """
        ディクショナリからPandasDataFrameを生成する

        Parameters
        ----------
        dfItemInfo : DataFrame
            取得データDataFrame
        dictItemInfo : dict
            取得データDictionary
        keys : list
            主キー情報
        """

        # ディクショナリの件数が0件の場合は列情報(DataFrame)のみ返す
        if len(dictItemInfo) == 0: return dfItemInfo
        
        # DictionaryをDataFrameに変換
        dfItemInfo = dfItemInfo.from_dict(dictItemInfo, orient='index')

        # 主キー指定して返す
        return dfItemInfo.set_index(keys, drop=False)
    
class baseWebDriverController:

    
    """
    WebDriverコントローラー基底クラス
    """ 
    
    def __init__(self, _config:scrapingConfig):

        """
        コンストラクタ
        
        Parameters
        ----------
        _config : scrapingConfig
            共通設定クラス

        """
        
        pass
