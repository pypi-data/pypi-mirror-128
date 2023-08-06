from Scrapinger.Library.scrapingerGlobals import scrapingerGlobal

class mercariGetterGlobal(scrapingerGlobal):
    
    def __init__(self):
        
        # 基底側コンストラクタ呼び出し
        super().__init__()
        
        self.mercariGetterConfig = None
        """ mercariGetter共通設定 """

# インスタンス生成(import時に実行される)
gv = mercariGetterGlobal()