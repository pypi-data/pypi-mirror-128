from pytdp.analyzer.api import DataScience
from pytdp.preprocessor.api import Missing
from pytdp.reader.api import Tdp_reader
from pytdp.bases.api import Base
import os

class TroublesomeData(DataScience, Missing, Tdp_reader, Base):
    def __init__(self,
                 data_list_or_directory = os.getcwd(), 
                 working_directory = os.getcwd(), 
                 detail = {
                     'auto' : False,
                     'model' : None,
                 }):

        
        super(TroublesomeData, self).__init__(data_list_or_directory, working_directory)

         
        ## 【１】可視化☛画像の保存
        ### 新しくplotフォルダを作成して画像の可視化及び変数格納を行うクラスを作成
        ### [] 散布図の描画
        ### [] ヒートマップの描画
        ### [] 棒グラフの描画
        ### [] 時系列グラフの描画
        
        ## 【２】前処理の追加
        ### 現在は条件を満たす列情報の削除のみにとどまっているので、欠損値を埋める処理についても追加していく
        ### また、欠損値だけではなく、多重共線性の排除や標準化なども行っていく。
        ### [] 特定の条件を満たす行情報の削除
        ### [] 欠損値の補完
        ### [] 異なるデータ同士の結合
        ### [] ダミー変数化
        ### [] 主成分分析
        
        ## 【３】分析の追加
        ### 現在は回帰分析のみ搭載しているので、分類分析なども追加していく
        ### クラスタリングや時系列の分析を追加予定
        ### [] 決定木分析の追加
        ### [] ランダムフォレストの追加
        ### [] SVMの追加
        ### [] 
        ### [] クラスタリングメソッドの追加
        ### [] クラスタリングの描画
        ### [] 
        ### [] アソシエーション分析

        ## 【４】検定の追加
        ### 様々なデータの検定を行っていく(可能であればデータを超えて)
        ### χ二乗検定
        ### t検定
        ### F検定
        ### フィッシャー検定
        ### 信頼区間

        if detail['auto'] :
            self.set_preprocess_key()
            self.delete_null()
            self.set_analyze_key()
            self.train_test_split()
            self.machine_learning(detail['model'])