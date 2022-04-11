# Crawler Interfaces Document #

## update

- retrievaled data is stored in both `file:///tmp/flights.json` and `redis://localhost/flights`
- stored as json string, example showed below.
- `json.load` will deal with `null/NAN,None` properly, don't panic.
- Here is [a tutorial for python redis client](https://www.runoob.com/w3cnote/python-redis-intro.html) in Chinese on runoob. 

### Explanation ###

输入数据为两个二元组tuple,第一个tuple是loc,第二个tuple是rng

loc和rng的第一个元素代表纬度,第二个元素代表经度,四个元素均为float类型

```python
example=Fr24Crawler((a1,b1),(a2,b2))
```

人为定义一个范围,定义方式为:选取一个正方形区域,它的中心点就是loc,左上角是rng,正方形的其他三个边角可以相应地计算得到

这样最后上网爬取的航班,其坐标会被严格框定在这个正方形区域内

在fr24_crawler.py文件里, Class是Fr24Crawler, 里面两个method分别是get_data_once和spin

一开始执行spin这个method,在里面每十秒执行一次get_data_once,进行数据爬取和筛选

### Output ###

爬取的原始文件输出到origin_data.json，处理后的数据输出到output.json

输出的数据是list套dict, list当中的每一个dict都代表一个航班的所有信息

dict的各个索引:

| readme中文 | readme英文        | output索引名 | origin_data索引树                       |
| ---------- | ----------------- | ------------ | --------------------------------------- |
| 经度       | longitude         | longitude    | ["geometry"] ["coordinates"] [0]        |
| 纬度       | latitude          | latitude     | ["geometry"] ["coordinates"] [1]        |
| 航向       | heading           | heading      | ["properties"] ["direction"]            |
| 海拔高度   | altitude          | altitude     | ["properties"] ["altitude"]             |
| 地速       | ground speed      | groundspeed  | ["properties"] ["groundspeed"]          |
| 航班号     | flight number     | ident        | ["properties"] ["ident"]                |
| 出发机场   | departure airport | departure    | ["properties"] ["origin"] ["iata"]      |
| 到达机场   | arrival airport   | arrival      | ["properties"] ["destination"] ["iata"] |

Remark: 关于数据单位, `altitude` 会在代码中执行单位转换,由百英尺转换为米, `groundspeed` 单位是节

注:

origin_data当中coordinates是一个二元list,第一个元素是经度,第二个元素是纬度

Here's an example of output:
```json
[
    {
        "longitude": 120.44936,
        "latitude": 30.23611,
        "heading": 243,
        "ident": "CDC8626",
        "departure": null,
        "arrival": null,
        "altitude": -2,
        "groundspeed": 127
    },
    {
        "longitude": 121.79855,
        "latitude": 31.11445,
        "heading": 342,
        "ident": "CJT1403",
        "departure": "NRT",
        "arrival": null,
        "altitude": -1,
        "groundspeed": 118
    },
    {
        "longitude": 119.32055,
        "latitude": 33.47627,
        "heading": 317,
        "ident": "CES771",
        "departure": "PVG",
        "arrival": "AMS",
        "altitude": 301,
        "groundspeed": 441
    }
]
```

### Remarks ###

1.readme当中还要获取 squawk number (应答机编号) 和 registration number (国籍注册号), 但是flightaware网站上的信息当中没有这两条.根据piazza上面刁子豪的指示,这两条忽略

2.由于网站自身原因,有一些数据可能会不存在(例如海拔altitude和地速groundspeed),经过处理后,这些本应存在但实际上不存在的数据,在python中赋值为None,输出到json中后显示为null;有一些数据本身就是null(例如到达机场arrival),输出之后依旧为null

3.控制面板上输入参数的时候, 中心点坐标和左上角坐标必须合法. 经过计算后, 它们所框定的正方形其他三个顶点坐标也必须合法. 合法是指: 经度范围`[-360,360]`, 纬度范围 `[-90,90]`. 如果用户输入的数据不合法, 必须重新输入