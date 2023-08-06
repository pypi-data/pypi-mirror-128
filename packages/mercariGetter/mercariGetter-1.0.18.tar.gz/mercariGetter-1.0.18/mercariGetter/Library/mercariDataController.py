import json
import pandas as pd
import LibHanger.Library.uwLogger as Logger
from pandas.core.frame import DataFrame
from Scrapinger.Library.browserController import browserContainer
from Scrapinger.Library.webDriverController import webDriverController
from mercariGetter.Library.mercariConfig import mercariConfig
from mercariGetter.Library.mercariGetterGlobals import *
from mercariGetter.Library.mercariException import resultDataGenerateError

class mercariDataSearch(browserContainer):
    
    """
    mercariデータ検索クラス
    """
    
    def __init__(self) -> None:
        
        # 基底側コンストラクタ
        super().__init__()

        # WebDriverController
        self.wdc = webDriverController(gv.mercariGetterConfig, self)
        
    def searchData(self, searchConditionJsonString:str) -> str:
        
        """
        mercariデータ検索

        Parameters
        ----------
        searchConditionJsonString : str
            検索条件Json文字列

        """
        
        # 取得したメルカリデータをpandas dataframeで返却する
        dfMercariData = self.getMercariDataToPandas(searchConditionJsonString, gv.mercariGetterConfig)
        
        # pandasデータをjson形式に変換する
        stringJson = dfMercariData.to_json(orient='records')

        # jsonデータを返す
        return stringJson
    
    def getMercariDataToPandas(self, searchConditionJsonString:str, config:mercariConfig):
        
        """
        取得したmercariデータをpandas dataframeに変換

        Parameters
        ----------
        searchConditionJsonString : str
            検索条件JSON文字列
        config : mercariConfig
            共通設定クラス
        """

        # 検索キーワードと取得する最大ページ数を取得する
        searchWord, maxPageCount = self.getSearchConditionKeywords(searchConditionJsonString)
        
        # 格納用pandasカラム準備
        dfItemInfo:DataFrame = self.initSearchResultDataColumns()
        
        # 検索キーワードが未指定なら処理を抜ける
        if searchWord == '':
            return dfItemInfo

        # 検索url
        url = config.MercariUrl + config.MercariUrlSearch + searchWord
        
        # ヘッドレスでブラウザを起動
        #driver:WebDriver = self.wdc.getWebDriver(config)
        #driver = self.wdc.browserCtl.getWebDriver()
        self.wdc.getWebDriverInstance()

        # ウィンドウサイズを1200x1200にする(商品名が省略される為)
        #self.changeBrowzerSize(driver, '1200', '1000')
        self.wdc.browserCtl.changeBrowserSize('1200', '1000')
                
        # 最大ページ数の数だけループして各ページから取得した結果を結合
        dictItemInfo:dict = {}
        for pageNum in range(int(maxPageCount)):
            
            # urlの最後にページ番号を付加する
            pageNum += 1
            targetUrl = url + '&page={}'.format(str(pageNum))

            # url指定してページ読込
            #self.loadPage(driver, targetUrl)
            self.wdc.browserCtl.loadPage(targetUrl)
            
            # 検索結果ディクショナリ生成
            #dictItemInfoTmp:dict = self.createSearchResultDictionary(driver,dfItemInfo, config, len(dictItemInfo))
            dictItemInfoTmp:dict = self.wdc.browserCtl.createSearchResultDictionary(dfItemInfo, len(dictItemInfo))
            if len(dictItemInfoTmp) == 0:
                break
            else:
                dictItemInfo.update(dictItemInfoTmp)

            print(len(dictItemInfo))
            
        # ブラウザを閉じる
        self.wdc.browserCtl.wDriver.quit()
        
        # pandasデータを返却する
        #return dfItemInfo if len(dictItemInfo) == 0 else self.createPandasData(dfItemInfo, dictItemInfo)
        return self.wdc.browserCtl.createPandasData(dfItemInfo, dictItemInfo, ['itemId'])
    
    def getSearchConditionKeywords(self, searchConditionJsonString:str) -> str:

        """
        検索キーワードを取得する

        Parameters
        ----------
        searchConditionJsonString : str
            検索条件JSON文字列
        """

        # JSON文字列をデシリアライズ
        keywordsData = json.loads(searchConditionJsonString)

        # デシリアライズしたJSON文字列をループして配列に格納
        lstKeyworsString = list()
        for jsn_key in keywordsData:
            if type(keywordsData[jsn_key]) == str:
                if keywordsData[jsn_key] == '': continue
                if jsn_key != 'maxPageCount':
                    lstKeyworsString.append(jsn_key + '=' + keywordsData[jsn_key])
                else:
                    maxPageCount = keywordsData[jsn_key]
            elif type(keywordsData[jsn_key]) == list:
                keywordsSubList:list = keywordsData[jsn_key]
                if len(keywordsSubList) == 0: continue
                lstKeyworsString.append(jsn_key + '=' + ','.join(keywordsSubList))

        # 配列間を'&'で結合
        keywordsString = '&'.join(lstKeyworsString)

        # 検索キーワードを返す
        return keywordsString, maxPageCount
    
    @Logger.loggerDecorator('Init SearchResultData DataFrame')
    def initSearchResultDataColumns(self) -> DataFrame:
        
        """
        メルカリデータ格納用のPandasDataFrameを初期化する

        Parameters
        ----------
        None
        """

        return pd.DataFrame(columns=['itemId','itemUrl','itemName','itemPrice','itemPicUrl','soldout'])
    
    def createSearchResultDictionaryByWebDriver(self, element, dfItemInfo: DataFrame, dictItemInfoRowCount: int) -> dict:

        """
        スレイピング結果からDictionaryを生成する

        Parameters
        ----------
        element : any
            スクレイピング結果
        dfItemInfo : DataFrame
            メルカリデータDataFrame
        config : mercariConfig
            共通設定クラス
        dictItemInfoRowCount : int
            メルカリデータDictionary現在行数
        """

        # 取得した商品タグをループして検索結果ディクショナリを生成
        dictItemInfo = {}
        try:
            index = 0
            for elm in element.find_elements_by_tag_name('li'):
                try:
                    elems_a = elm.find_element_by_tag_name('a')
                    elems_m = elems_a.find_element_by_tag_name('mer-item-thumbnail')
                    index += 1

                    # 商品ID
                    itemUrl = elems_a.get_attribute('href')
                    itemId = itemUrl.split('/')[4]
                    # 商品名
                    itemNm = elems_m.get_attribute('item-name')
                    # 商品画像URL
                    itemPicUrl = elems_m.get_attribute('src')
                    # 価格
                    itemPrice = elems_m.get_attribute('price')
                    # SoldOut
                    soldOut = True if elems_m.get_attribute('sticker') else False
                    # ログ出力
                    Logger.logging.info('==========================================================')
                    Logger.logging.info(str(index + 1) + '/' + str(len(element.find_elements_by_tag_name('li'))))
                    Logger.logging.info('商品ID={}'.format(itemId))
                    Logger.logging.info('商品URL={}'.format(itemUrl))
                    Logger.logging.info('商品名={}'.format(itemNm))
                    Logger.logging.info('商品画像URL={}'.format(itemPicUrl))
                    Logger.logging.info('価格={}'.format(itemPrice))
                    Logger.logging.info('==========================================================')
                    # 取得データをディクショナリにセット
                    drItemInfo = pd.Series(data=['','','',0,'',False],index=dfItemInfo.columns)
                    drItemInfo['itemId'] = itemId
                    drItemInfo['itemUrl'] = itemUrl
                    drItemInfo['itemName'] = itemNm
                    drItemInfo['itemPrice'] = itemPrice
                    drItemInfo['itemPicUrl'] = itemPicUrl
                    drItemInfo['soldout'] = soldOut
                    dictItemInfo[index + dictItemInfoRowCount] = drItemInfo
                except:
                    # 例外をスローする
                    raise resultDataGenerateError
            
            # PandasData作成完了ログ
            Logger.logging.info('PandasData Create Complete')

        except resultDataGenerateError as e:
            # キャッチした例外をログ出力
            Logger.logging.error('PandasData Create Error')
            Logger.logging.error(e.args)
            dictItemInfo = {}

        # 戻り値を返す
        return dictItemInfo

    def createSearchResultDictionaryByBeutifulSoup(self, soup, dfItemInfo: DataFrame, dictItemInfoRowCount: int) -> dict:
        """
        スレイピング結果からDictionaryを生成する

        Parameters
        ----------
        soup : BeautifulSoup
            スクレイピング結果
        dfItemInfo : DataFrame
            メルカリデータDataFrame
        config : mercariConfig
            共通設定クラス
        dictItemInfoRowCount : int
            メルカリデータDictionary現在行数
        """

        # 商品タグ取得
        elems_items= soup.select(gv.mercariGetterConfig.ItemTagName)
        
        # 取得した商品タグをループして検索結果ディクショナリを生成
        dictItemInfo = {}
        try:
            for index in range(len(elems_items)):
                try:
                    # 商品ID
                    itemUrlTmp = elems_items[index].find_all('a')[0].get('href')
                    itemId = itemUrlTmp.split('/')[2]
                    itemUrl = gv.mercariGetterConfig.MercariUrl.rstrip('/') + itemUrlTmp
                    # 商品名
                    itemNm = elems_items[index].find_all('mer-item-thumbnail')[0].get('item-name')
                    # 商品画像URL
                    itemPicUrl = elems_items[index].find_all('mer-item-thumbnail')[0].get('src')
                    # 価格
                    itemPrice = elems_items[index].find_all('mer-item-thumbnail')[0].get('price')
                    # SoldOut
                    soldOut = True if elems_items[index].find_all('mer-item-thumbnail')[0].get('sticker') else False
                    # ログ出力
                    Logger.logging.info('==========================================================')
                    Logger.logging.info(str(index + 1) + '/' + str(len(elems_items)))
                    Logger.logging.info('商品ID={}'.format(itemId))
                    Logger.logging.info('商品URL={}'.format(itemUrl))
                    Logger.logging.info('商品名={}'.format(itemNm))
                    Logger.logging.info('商品画像URL={}'.format(itemPicUrl))
                    Logger.logging.info('価格={}'.format(itemPrice))
                    Logger.logging.info('==========================================================')
                    # 取得データをディクショナリにセット
                    drItemInfo = pd.Series(data=['','','',0,'',False],index=dfItemInfo.columns)
                    drItemInfo['itemId'] = itemId
                    drItemInfo['itemUrl'] = itemUrl
                    drItemInfo['itemName'] = itemNm
                    drItemInfo['itemPrice'] = itemPrice
                    drItemInfo['itemPicUrl'] = itemPicUrl
                    drItemInfo['soldout'] = soldOut
                    dictItemInfo[index + dictItemInfoRowCount] = drItemInfo
                except:
                    # 例外をスローする
                    raise resultDataGenerateError
            
            # PandasData作成完了ログ
            Logger.logging.info('PandasData Create Complete')

        except resultDataGenerateError as e:
            # キャッチした例外をログ出力
            Logger.logging.error('PandasData Create Error')
            Logger.logging.error(e.args)
            dictItemInfo = {}

        # 戻り値を返す
        return dictItemInfo

    class chrome(browserContainer.chrome):
        
        def __init__(self, _config: mercariConfig):
            super().__init__(_config)
            #self.cbCreateSearchResultDictionaryByWebDriver = self.createSearchResultDictionaryByWebDriver
            #self.cbCreateSearchResultDictionaryByBeutifulSoup = self.createSearchResultDictionaryByBeutifulSoup
            self.cbCreateSearchResultDictionaryByWebDriver = mercariDataSearch.createSearchResultDictionaryByWebDriver
            self.cbCreateSearchResultDictionaryByBeutifulSoup = mercariDataSearch.createSearchResultDictionaryByBeutifulSoup
        
    class firefox(browserContainer.firefox):
        
        def __init__(self, _config: mercariConfig):
            super().__init__(_config)
            #self.cbCreateSearchResultDictionaryByWebDriver = self.createSearchResultDictionaryByWebDriver
            #self.cbCreateSearchResultDictionaryByBeutifulSoup = self.createSearchResultDictionaryByBeutifulSoup
            self.cbCreateSearchResultDictionaryByWebDriver = mercariDataSearch.createSearchResultDictionaryByWebDriver
            self.cbCreateSearchResultDictionaryByBeutifulSoup = mercariDataSearch.createSearchResultDictionaryByBeutifulSoup
            
        #def createSearchResultDictionaryByWebDriver(self, element, dfItemInfo: DataFrame, dictItemInfoRowCount: int) -> dict:
        #    print('orverride-createSearchResultDictionaryByWebDriver')
        #    return super().createSearchResultDictionaryByWebDriver(element, dfItemInfo, dictItemInfoRowCount)

        #def createSearchResultDictionaryByBeutifulSoup(self, soup, dfItemInfo: DataFrame, dictItemInfoRowCount: int) -> dict:
        #    print('orverride-createSearchResultDictionaryByBeutifulSoup')
        #    return super().createSearchResultDictionaryByBeutifulSoup(soup, dfItemInfo, dictItemInfoRowCount)