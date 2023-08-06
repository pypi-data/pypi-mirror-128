import LibHanger.Library.uwLogger as Logger
from Scrapinger.Library.baseWebDriverController import baseWebDriverController
from Scrapinger.Library.browserController import browserContainer
from Scrapinger.Library.scrapingConfig import scrapingConfig

class webDriverController(baseWebDriverController):
    
    """
    WebDriverコントローラークラス
    
    Notes
    -----
        取り扱うWebDriverをブラウザータイプごとに取得する
    """ 

    def __init__(self, _config:scrapingConfig, _browserContainer:browserContainer):
        
        """
        コンストラクタ
        
        Parameters
        ----------
        _config : scrapingConfig
            共通設定クラス

        """ 
        
        # 共通設定取得
        self.config = _config
        
        # ブラウザーコンテナインスタンス設定
        self.browserContainerInstance = _browserContainer
        
        # ブラウザーコントロールインスタンス初期化
        self.browserCtl = None
    
    @Logger.loggerDecorator('Get WebDriverInstance')
    def getWebDriverInstance(self):
        
        """
        WebDriverインスタンスを取得する
        """ 

        # ブラウザータイプごとに生成するインスタンスを切り替える
        browserName = 'unknown'
        if self.config.BrowserType == scrapingConfig.settingValueStruct.BrowserType.chrome.value:
            self.browserCtl = self.browserContainerInstance.chrome(self.config)
            browserName = scrapingConfig.settingValueStruct.BrowserType.chrome.name
        elif self.config.BrowserType == scrapingConfig.settingValueStruct.BrowserType.firefox.value:
            self.browserCtl = self.browserContainerInstance.firefox(self.config)
            browserName = scrapingConfig.settingValueStruct.BrowserType.firefox.name
        
        # 取得したWebDriverをログ出力
        Logger.logging.info('BrowserType:' + str(self.config.BrowserType))
        Logger.logging.info('SelectedBrowser:' + browserName)

        # 取得したWebDriverインスタンスを返す
        return self.browserCtl.getWebDriver()

