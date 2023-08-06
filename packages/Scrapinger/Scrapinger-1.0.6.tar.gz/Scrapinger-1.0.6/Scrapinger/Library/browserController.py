from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from LibHanger.Library.uwGlobals import *
from Scrapinger.Library.baseWebDriverController import baseWebBrowserController
from Scrapinger.Library.scrapingConfig import scrapingConfig

class browserContainer:
    
    """
    ブラウザコンテナクラス
    """

    class chrome(baseWebBrowserController):
        
        """
        GoogleCheromブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = chromeOptions()
            # ヘッドレスモード設定
            options.add_argument('--headless')
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.chrome)
            # WebDriverを返す
            if self.config.chrome.WebDriverLogPath == '':
                self.wDriver = webdriver.Chrome(executable_path=webDriverPath, options=options)
            else:
                self.wDriver = webdriver.Chrome(executable_path=webDriverPath, log_path=self.config.chrome.WebDriverLogPath, options=options)
            return self.wDriver 
        
    class firefox(baseWebBrowserController):
        
        """
        FireFoxブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = firefoxOptions()
            # ヘッドレスモード設定
            options.add_argument('--headless')
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.firefox)
            # WebDriverを返す
            if self.config.firefox.WebDriverLogPath == '':
                self.wDriver = webdriver.Firefox(executable_path=webDriverPath, options=options)
            else:
                self.wDriver = webdriver.Firefox(executable_path=webDriverPath, log_path=self.config.firefox.WebDriverLogPath, options=options)
            return self.wDriver 
