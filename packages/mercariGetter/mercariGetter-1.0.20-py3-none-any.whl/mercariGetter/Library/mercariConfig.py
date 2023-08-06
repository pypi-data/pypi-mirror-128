from Scrapinger.Library.scrapingConfig import scrapingConfig

class mercariConfig(scrapingConfig):
    
    """
    mercariGetter共通設定クラス(mercariConfig)
    """ 

    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        self.MercariUrl = 'https://jp.mercari.com/'
        """ メルカリURL """
        
        self.MercariUrlSearch = 'search?'
        """ メルカリURL Search Keyword"""

    def getConfigFileName(self):
        
        """ 
        設定ファイル名 
        """

        return 'mercariGetter.ini'
    
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # 基底側実行
        super().setInstanceMemberValues()
        
        # メルカリURL
        super().setConfigValue('MercariUrl',self.config_ini,'SITE','MERCARI_URL',str)

        # メルカリURL Search Keyword
        super().setConfigValue('MercariUrlSearch',self.config_ini,'SITE','MERCARI_URL_SEARCH',str)
