# TRA Best Price and Schedule query

搜尋最佳價格與如何轉乘台鐵安排。提供經濟緊縮想效益最大化最好安排。

台鐵目前採取電子票卡收費模式為：
1. 電子票卡刷卡進站 9 折優惠
2. 九折優惠限制為區間路程 70 公里內（可搭乘自強、莒光、各類區間車）
3. 超過每一公里按照自強價格收費

因此如果要效益最大化做法：
1. 就是電子票卡刷卡入站
2. 每 70 公里必須換乘（用電子票卡刷進刷出一次）
3. 換乘間格與時間的拿捏。例如：A 到 B 計 50 公里，B 到 C 計 50 公里，共計 100 公里; 需要 A -> B 轉乘，B -> C 轉乘; 轉乘所花費的時間需要被考量。原則上目前定義就是根據總時間長度來排序（依序一定是直達車、轉乘車）


## 資料來源與 API

+ [各站的營業里程](https://www.railway.gov.tw/tw/CP.aspx?sn=3611)
+ [台鐵七十公里里程](https://www.railway.gov.tw/tw/Kilometer.aspx?n=20998)
+ [台鐵電子票證價格說明](https://www.railway.gov.tw/tw/CP.aspx?sn=1312)
+ [公共運輸整合資料平台](https://ptx.transportdata.tw/PTX/Service?Transportation=%E8%87%BA%E9%90%B5)
+ [PTX API 文件](https://gist.github.com/ptxmotc/383118204ecf7192bdf96bc0197bb981)


## 開發模組

+ 資料取得模組
+ 規劃路徑以及查詢里程
+ 計算票價格