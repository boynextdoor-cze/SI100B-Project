## specification for data&control channel data format

> 关于数据传输与控制信息传输的说明文档  
> ***TODO***:约定获取失败/修改失败时的相应.目前处理方式为: 所有失败操作,给出不为200的code.
> ***TODO***:约定LED controller的mode数据格式


- use `redis` as a message queue
- check [runoob: redis.py](https://www.runoob.com/w3cnote/python-redis-intro.html) and [redis.py 's github repository](https://github.com/andymccurdy/redis-py) for usage of `redis.py`


- `client = redis.Redis('localhost',6379)`
- 多次新建连接使用`redis.ConnectionPool`
- redis中,操作单个KV pair是atomic的
- `VERSION_CYCLE = 100000` 使用pipeline+watch进行transaction时,需要一个watch varible,一般是一个确定版本(数据被更新次数)的数,每到达VERCYC就从0开始.
- 信息使用publish/subscribe传输,避免使用锁
- 向redis写数据只能用bytes(如果是基本数据类型或者字符串,`redis.py`会自动转换)
- 从redis获取数据时会得到python的bytes,需要decode再parse

- redis上的一切数据应当合法,不做更多检查.
- 用户输入的合法性由flask web app校验.
- 向redis写入数据时请遵循约定.

### Crawler

向外给出数据和状态.Crawler只写,外部只读

- 航班数据: `KV('flights')`;JSON格式,最外层是list.
- 上次航班数据抓取时间: `KV('flights-upd')`; unix timestamp,正整数,秒,正整数,秒.
- 抓取范围: `KV('range')`;4-tuple of float,`(center_lat,center_lon,conrner_lat,corner_range)`
- 上次获取token的时间: `KV('token-upd')`; 日期格式为`year-month-day-hour-minute-second`
- 一次获取的token有效时长: `KV('token-life')`; 正整数,单位为秒
- 抓取数据间隔时间: `KV('fetch-interval')`; 正整数,单位为秒
- 当前使用的token: `KV('token')`; 字符串
- 向外部发送本次爬取结束的消息; `pub channel('control-data-update')`, 预期获取任意数据

由外部发给Crawler,休眠期间隔性读取

- 控制抓取范围;`sub channel('control-range')`,预期获取一个四元组,描述中心和左上角.
- 控制token预期有效时间;`sub channel('control-token-life')`,预期获取一个正整数,单位为秒.  
- 强制刷新token;`sub channel('control-token-refresh')`,预期获取任意非空数据,非None则立刻刷新token.  
- 控制爬取间隔;`sub channel('control-fetch-interval')`,预期获取单位为秒的正整数.



### LED Controller

向外给出状态.Controller只写,外部只读

- 重新计算LED输出状态的间隔;`KV('led-interval')`; 正整数,单位为秒
- active 表示是否启用;`KV('led-active')`; 0/1
- 显示模式;`KV('led-mode')`; 0/1表示常驻/闪烁
- 数量基准,表示以$10^base$为单位;`KV('led-base')`; 自然数.

由外部发送控制指令,休眠期间隔性读取

- 控制刷新时长;`sub channel('control-led-interval')`;预期获取单位为秒的正整数.
- 切换状态;`sub channel('control-led-active')`; 预期获取一个0/1的数字.
- 显示模式;`sub channel('control-led-mode')`;  预期获取一个0/1的数字.
- 数量基准;`sub channel('control-led-base')`;  预期获取一个自然数.



### Visualizer

向外给出状态.Visualizer只写，外部只读

- 列举全部可视化方式;`KV('vis-list')`; JSON对象，格式如下：

```javascript
{
  	"sponge": {//A unique identifier for locate the resource.
	   	"title": "SpongeBob SquarePants",//The title of the item
	   	"description": "A cartoon",//The description of the item
   	},
	"tom" : {
	   	"title": "Tom and Jerry",
	   	"description": "Another cartoon",
	}
}
```

- 获取对应可视化方式渲染好的图像;`KV('(id)')`; Data URI 格式的 SVG
- 获取图像渲染完成的时间;`KV('render-upd')`; 返回Unix timestamp



### Static Data Loader

向外给出状态，Static Data Loader只写， 外部只读

- 列举全部机场的信息;`KV('static-airports')`; JSON对象，格式如下：

```json
{
	"AAA": {
		"IATA": "AAA",
		"ICAO": "NTGA",
		"Airport name": "Anaa Airport",
		"Location served": [
			"Anaa",
			"Tuamotus",
			"French Polynesia"
		],
		"Time": "UTC\u221210:00",
		"DST": ""
	},
	"AAB": {
		"IATA": "AAB",
		"ICAO": "YARY",
		"Airport name": "Arrabury Airport",
		"Location served": [
			"Arrabury",
			"Queensland",
			"Australia"
		],
		"Time": "UTC+10:00",
		"DST": ""
	},
}
```
Data is from wikipedia.

### Web Server

#### 渲染页面

- `/,/index/,/home/,/config/`,都重定到`/config/`;获取控制面板的页面,只允许`GET`.
- `/page-not-found/`访问未确定的路由,应当被重定向到这里.



#### 获取数据,使用动词GET

- `GET /flights/` 所有航班数据,JSON

成功code=200,并在body中给出数据.

1. `flights`,一个列表,每个元素表示一个航班的信息.
2. `flights-upd`,unix timestamp的秒部分,正整数.

返回数据格式举例

```json
{ 'flights': [
			{
				"altitude":331,
				"arrival":"WNZ",
				"departure":"PEK",
				"ident":"CCA1539",
				"groundspeed":552,
				"heading":116,
				"latitude":31.67223,
				"longitude":120.23004 },
			{
				"altitude":194,
				"arrival":"KMG",
				"departure":"YIW",
				"ident":"CES5764",
				"groundspeed":357,
				"heading":271,
				"latitude":29.49742,
				"longitude":119.24318 }
		],
	"flights-upd": 1607697543
}
```


- `GET /crawler/` 返回爬虫状态,JSON

成功code=200,并在body中给出数据.

1. `token-life` A positive integer, unit: second, range: $[30, 90]$.
2. `token-upd` The unix timestamp, positive integers, unit: second.
3. `interval` A positive integer, unit: second, range: $[10, 60]$.
4. `range` A 4-tuple{center_lat, center_lon, corner_lat, corner_lon}, centered at (center_lat, center_lon) with top-left corner at (corner_lat, corner_lon). range: for latitudes, [-90, 90]; for longtitudes, [-360, 360]. 
5. `token` A string, indicating the token being used.
(The range here is just a temporary solution, you can change it but please communicate well)

返回数据格式举例

```json
{
	"token-life": 30,
	"token-upd": 1607393500,
	"interval": 10,
	"range": {
		"center_lat": 30,
		"center_lon": 110,
		"corner_lat": 34,
		"corner_lon": 120,
	}
}
```


- `GET /led/`

成功code=200,并在body中给出数据.

1. `interval` 正整数,单位为秒.
2. `active` 数字0/1.
3. `base` 数量基准,一个自然数.
4. `mode` 显示模式,一个自然数.

```json
{
	"interval": 5,
	"active": 1,
	"base": 0,
	"mode": 1
}
```


- `GET /agg/`

Result HTTP code 200 on success, result the data in JSON format in response text.

1. `list`: A dictionary representing the types of aggregation. Any object in the dictionary has the following format. 
```javascript
{
  	"sponge": {//A unique identifier for locate the resource.
	   	"title": "SpongeBob SquarePants",//The title of the item
	   	"description": "A cartoon",//The description of the item
   	},
	"tom" : {
	   	"title": "Tom and Jerry",
	   	"description": "Another cartoon",
	}
}
```

- `GET /agg/{id}`

Result HTTP code 200 on success, result the data in data URI format(not JSON) in response text. 
1. `image`: A base64 encoded svg in data URI format. 

- `GET /agg/last-render-timestamp/` 返回`render-upd`.JSON

```json
{"render-upd": 1607697543}
```

#### 修改状态,使用动词POST,参数在body中以JSON给出

- `POST /crawler/` 用于修改爬虫状态,格式与获取状态的相应相同(增加`"token-refresh":1`来要求强制刷新token),不做修改的状态可以null或者不填写.数据合法性由server验证.  

数据合法,成功将状态更新消息发送给crawler;则code=200.  
其他情况给出给出`status_code = 4xx,5xx`并在body中给出错误信息的plaintext.  


数据范围约束:

1. `token-life` 应当大于0,应当不小于crawler的fetch interval.
2. `interval` 应当不低于10.
3. `range` latitude在$[-90,90]$,longitude在$[-180,180]$.
4. `token-refresh` 无约束


- `POST /led/` 用于LED控制器状态,格式与获取状态的相应相同,不做修改的状态可以null或者不填写.数据合法性由server验证.

数据合法,成功将状态更新消息发送给LEDcontroller;则code=200.
其他情况给出给出`status_code = 4xx,5xx`并在body中给出错误信息的plaintext.  


数据范围约束:

1. `interval` 不大于crawler的fetch interval,大于0.  
2. `active` 仅限数字0或1.
3. `base` 使得$10^{base}$不超过全球航班数量峰值即可. 目前全球航班在$10^5$数量级,于是$base\in \{0,1,2,3,4,5\}$
4. `mode` 0或1分别对应常亮和闪烁.


- `POST /proxy/` To help scripts running on clients to send HTTP requests. Because of the same origin policies of browers, javascript is banned from sending XHR requests to different origins. Hence, there is a need for a server side proxy to help client pass the restriction of same origin policies. 

1. `_url` The url for the HTTP request.
2. `_method` The method used for the HTTP request. Avaliable values: 'GET' or 'POST'. Other parameters would cause the server return HTTP status code 500.
3. `(others)` Would be treated us the data to be sent to the target HTTP url. If the method is 'GET', they would be attached to the url; If the method is 'POST', it would be treated as the body(in JSON format) .

Response: would copy the response body for the target request, with HTTP status code 200(except the method is not allowed, in this case, the server will return HTTP status code 500 ). 


#### 向LEDcontroller/crawler发送消息


- 控制抓取范围;`pub channel('control-range')`
- 控制token预期有效时间;`pub channel('control-token-life')`
- 强制刷新token;`pub channel('control-token-refresh')`
- 控制爬取间隔;`pub channel('control-fetch-interval')`


- 控制刷新时长,`pub channel('control-led-interval')`
- 切换状态,`pub channel('control-led-active')`
- 显示模式,`pub channel('control-led-mode')`;
- 数量基准,`pub channel('control-led-base')`;
## specification for data&control channel data format

> 关于数据传输与控制信息传输的说明文档  
> ***TODO***:约定获取失败/修改失败时的相应.目前处理方式为: 所有失败操作,给出不为200的code.
> ***TODO***:约定LED controller的mode数据格式


- use `redis` as a message queue
- check [runoob: redis.py](https://www.runoob.com/w3cnote/python-redis-intro.html) and [redis.py 's github repository](https://github.com/andymccurdy/redis-py) for usage of `redis.py`


- `client = redis.Redis('localhost',6379)`
- 多次新建连接使用`redis.ConnectionPool`
- redis中,操作单个KV pair是atomic的
- `VERSION_CYCLE = 100000` 使用pipeline+watch进行transaction时,需要一个watch varible,一般是一个确定版本(数据被更新次数)的数,每到达VERCYC就从0开始.
- 信息使用publish/subscribe传输,避免使用锁
- 向redis写数据只能用bytes(如果是基本数据类型或者字符串,`redis.py`会自动转换)
- 从redis获取数据时会得到python的bytes,需要decode再parse

- redis上的一切数据应当合法,不做更多检查.
- 用户输入的合法性由flask web app校验.
- 向redis写入数据时请遵循约定.

### Crawler

向外给出数据和状态.Crawler只写,外部只读

- 航班数据: `KV('flights')`;JSON格式,最外层是list.
- 上次航班数据抓取时间: `KV('flights-upd')`; unix timestamp,正整数,秒,正整数,秒.
- 抓取范围: `KV('range')`;4-tuple of float,`(center_lat,center_lon,conrner_lat,corner_range)`
- 上次获取token的时间: `KV('token-upd')`; 日期格式为`year-month-day-hour-minute-second`
- 一次获取的token有效时长: `KV('token-life')`; 正整数,单位为秒
- 抓取数据间隔时间: `KV('fetch-interval')`; 正整数,单位为秒
- 当前使用的token: `KV('token')`; 字符串
- 向外部发送本次爬取结束的消息; `pub channel('control-data-update')`, 预期获取任意数据

由外部发给Crawler,休眠期间隔性读取

- 控制抓取范围;`sub channel('control-range')`,预期获取一个四元组,描述中心和左上角.
- 控制token预期有效时间;`sub channel('control-token-life')`,预期获取一个正整数,单位为秒.  
- 强制刷新token;`sub channel('control-token-refresh')`,预期获取任意非空数据,非None则立刻刷新token.  
- 控制爬取间隔;`sub channel('control-fetch-interval')`,预期获取单位为秒的正整数.



### LED Controller

向外给出状态.Controller只写,外部只读

- 重新计算LED输出状态的间隔;`KV('led-interval')`; 正整数,单位为秒
- active 表示是否启用;`KV('led-active')`; 0/1
- 显示模式;`KV('led-mode')`; 0/1表示常驻/闪烁
- 数量基准,表示以$10^base$为单位;`KV('led-base')`; 自然数.

由外部发送控制指令,休眠期间隔性读取

- 控制刷新时长;`sub channel('control-led-interval')`;预期获取单位为秒的正整数.
- 切换状态;`sub channel('control-led-active')`; 预期获取一个0/1的数字.
- 显示模式;`sub channel('control-led-mode')`;  预期获取一个0/1的数字.
- 数量基准;`sub channel('control-led-base')`;  预期获取一个自然数.



### Visualizer

向外给出状态.Visualizer只写，外部只读

- 列举全部可视化方式;`KV('vis-list')`; JSON对象，格式如下：

```javascript
{
  	"sponge": {//A unique identifier for locate the resource.
	   	"title": "SpongeBob SquarePants",//The title of the item
	   	"description": "A cartoon",//The description of the item
   	},
	"tom" : {
	   	"title": "Tom and Jerry",
	   	"description": "Another cartoon",
	}
}
```

- 获取对应可视化方式渲染好的图像;`KV('(id)')`; Data URI 格式的 SVG
- 获取图像渲染完成的时间;`KV('render-upd')`; 返回Unix timestamp



### Web Server

#### 渲染页面

- `/,/index/,/home/,/config/`,都重定到`/config/`;获取控制面板的页面,只允许`GET`.
- `/page-not-found/`访问未确定的路由,应当被重定向到这里.



#### 获取数据,使用动词GET

- `GET /flights/` 所有航班数据,JSON

成功code=200,并在body中给出数据.

1. `flights`,一个列表,每个元素表示一个航班的信息.
2. `flights-upd`,unix timestamp的秒部分,正整数.

返回数据格式举例

```json
{ 'flights': [
			{
				"altitude":331,
				"arrival":"WNZ",
				"departure":"PEK",
				"ident":"CCA1539",
				"groundspeed":552,
				"heading":116,
				"latitude":31.67223,
				"longitude":120.23004 },
			{
				"altitude":194,
				"arrival":"KMG",
				"departure":"YIW",
				"ident":"CES5764",
				"groundspeed":357,
				"heading":271,
				"latitude":29.49742,
				"longitude":119.24318 }
		],
	"flights-upd": 1607697543
}
```


- `GET /crawler/` 返回爬虫状态,JSON

成功code=200,并在body中给出数据.

1. `token-life` A positive integer, unit: second, range: $[30, 90]$.
2. `token-upd` The unix timestamp, positive integers, unit: second.
3. `interval` A positive integer, unit: second, range: $[10, 60]$.
4. `range` A 4-tuple{center_lat, center_lon, corner_lat, corner_lon}, centered at (center_lat, center_lon) with top-left corner at (corner_lat, corner_lon). range: for latitudes, [-90, 90]; for longtitudes, [-180, 180]. 
5. `token` A string, indicating the token being used.
(The range here is just a temporary solution, you can change it but please communicate well)

返回数据格式举例

```json
{
	"token-life": 30,
	"token-upd": 1607393500,
	"interval": 10,
	"range": {
		"center_lat": 30,
		"center_lon": 110,
		"corner_lat": 34,
		"corner_lon": 120,
	}
}
```


- `GET /led/`

成功code=200,并在body中给出数据.

1. `interval` 正整数,单位为秒.
2. `active` 数字0/1.
3. `base` 数量基准,一个自然数.
4. `mode` 显示模式,一个自然数.

```json
{
	"interval": 5,
	"active": 1,
	"base": 0,
	"mode": 1
}
```


- `GET /agg/`

Result HTTP code 200 on success, result the data in JSON format in response text.

1. `list`: A dictionary representing the types of aggregation. Any object in the dictionary has the following format. 
```javascript
{
  	"sponge": {//A unique identifier for locate the resource.
	   	"title": "SpongeBob SquarePants",//The title of the item
	   	"description": "A cartoon",//The description of the item
   	},
	"tom" : {
	   	"title": "Tom and Jerry",
	   	"description": "Another cartoon",
	}
}
```

- `GET /agg/{id}`

Result HTTP code 200 on success, result the data in data URI format(not JSON) in response text. 
1. `image`: A base64 encoded svg in data URI format. 

- `GET /agg/last-render-timestamp/` 返回`render-upd`.JSON

```json
{"render-upd": 1607697543}
```

#### 修改状态,使用动词POST,参数在body中以JSON给出

- `POST /crawler/` 用于修改爬虫状态,格式与获取状态的相应相同(增加`"token-refresh":1`来要求强制刷新token),不做修改的状态可以null或者不填写.数据合法性由server验证.  

数据合法,成功将状态更新消息发送给crawler;则code=200.  
其他情况给出给出`status_code = 4xx,5xx`并在body中给出错误信息的plaintext.  


数据范围约束:

1. `token-life` 应当大于0,应当不小于crawler的fetch interval.
2. `interval` 应当不低于10.
3. `range` latitude在$[-90,90]$,longitude在$[-180,180]$.
4. `token-refresh` 无约束


- `POST /led/` 用于LED控制器状态,格式与获取状态的相应相同,不做修改的状态可以null或者不填写.数据合法性由server验证.

数据合法,成功将状态更新消息发送给LEDcontroller;则code=200.
其他情况给出给出`status_code = 4xx,5xx`并在body中给出错误信息的plaintext.  


数据范围约束:

1. `interval` 不大于crawler的fetch interval,大于0.  
2. `active` 仅限数字0或1.
3. `base` 使得$10^{base}$不超过全球航班数量峰值即可. 目前全球航班在$10^5$数量级,于是$base\in \{0,1,2,3,4,5\}$
4. `mode` 0或1分别对应常亮和闪烁.


- `POST /proxy/` To help scripts running on clients to send HTTP requests. Because of the same origin policies of browers, javascript is banned from sending XHR requests to different origins. Hence, there is a need for a server side proxy to help client pass the restriction of same origin policies. 

1. `_url` The url for the HTTP request.
2. `_method` The method used for the HTTP request. Avaliable values: 'GET' or 'POST'. Other parameters would cause the server return HTTP status code 500.
3. `(others)` Would be treated us the data to be sent to the target HTTP url. If the method is 'GET', they would be attached to the url; If the method is 'POST', it would be treated as the body(in JSON format) .

Response: would copy the response body for the target request, with HTTP status code 200(except the method is not allowed, in this case, the server will return HTTP status code 500 ). 


#### 向LEDcontroller/crawler发送消息


- 控制抓取范围;`pub channel('control-range')`
- 控制token预期有效时间;`pub channel('control-token-life')`
- 强制刷新token;`pub channel('control-token-refresh')`
- 控制爬取间隔;`pub channel('control-fetch-interval')`


- 控制刷新时长,`pub channel('control-led-interval')`
- 切换状态,`pub channel('control-led-active')`
- 显示模式,`pub channel('control-led-mode')`;
- 数量基准,`pub channel('control-led-base')`;
