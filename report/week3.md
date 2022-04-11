# Project Report - Week 3

# SI100B Project Report - Control Panel

> Please submit this report as a PDF file along with your code to receive full score of the project. 

## Workload Division

> - Fill in the names and email addresses of your group members and describe how you divide works among team members;

| Name   | Email Address                  | Responsible for             |
| ------ | ------------------------------ | --------------------------- |
| 彭程   | pengcheng2@shanghaitech.edu.cn | IPC |
| 迟择恩 | chize@shanghaitech.edu.cn      | web server |
| 刘翊航 | liuyh10@shanghaitech.edu.cn    | frontend |

## Preliminary Comment

> - Please cite any online or offline resources you consulted in this project;
> - Please describe the difficulties you encountered in this project;

### reference

- [runoob:redis.py tutorial](https://www.runoob.com/w3cnote/python-redis-intro.html) [github: redis.py](https://github.com/andymccurdy/redis-py) accessing redis in python.
- [好吃的野菜's 简书blog](https://www.jianshu.com/p/feb86c06c4f4) usage of `logging` module. 
- [tldr manual: curl](https://github.com/tldr-pages/tldr/blob/master/pages/common/curl.md) sending JSON HTTP POST with curl.
- [Flask offcial documentation](https://flask.palletsprojects.com/) how to implement a web server using `flask`.
- [Vue.js](https://cn.vuejs.org/) [Vuetify](https://vuetifyjs.com/) [runoob tutorials](https://www.runoob.com/) [MDN docs](https://developer.mozilla.org/en-US/docs/Web/Reference): for basic web frontend knowledge and techniques.

- frontend things
  - [Icon resource](https://www.flaticon.com/free-icon/web-crawler_2282201): Copyright © Freepik from [flaticon](https://www.  flaticon.com/)
  - [Same-origin Policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy): Understanding why cross-o  rigin API calls in Javascripts are banned. 
  - [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), i.e. Cross-Origin Resource Sharing: A possible solution t  o cross-origin API calls in Javascripts, attempted but failed.
  - [CORS Proxy](https://medium.com/nodejsmadeeasy/a-simple-cors-proxy-for-javascript-applications-9b36a8d39c51): A final sol  ution for the cross-origin API calls, implemented on the server side.
  - [Data URIs](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/data_URIs): A way to transmit images between server and cli  ent

### Encoutered difficulties

1. `redis.Redis.get` returns `None` when the given key doesn't exists. `try-except`
2. When subscribe or unsubscribe occurs, the subscriber will receive a message, which is annoying. use `redis.Redis.pubsub(ignore_subscribe_messages=True)`.


## Advanced: Use Flask and HTML

> Answering the following questions with a concrete example is desirable.
> 
> - How to serve the request sent from the client for a specific path? For example, if a request is requesting the path `/public` on your server and another one is requesting `/confidential` on your server, how could you distinguish them and send different responses?
> - How to serve the different request methods? For example, one request is sent to your server for the path `/public` with a `GET` method and another one with a `POST` method, how could you distinguish them and send different responses?
> - How to render a HTML template in Flask? How to create a simple template in Flask?
> - How to get the form data a user sends to your server in a `POST` request? Which data type is it?
> - How to specify the title of a web page? How to add a paragraph to a web page? How to add a title to a web page?
> - How to design a form on a web page? How to add text box to your form? How to add an option to your form?
> - How to send the content of the form to the server? What HTTP methods are generally used for those requests? In Flask, how do you handle the request containing a form?

1. The two request have different HTTP header.  

Flask will distinguish them and find the right functions to process the requests.
Use `Flask.route(URL,*args,**kwargs)` a decorator to register the view function for `URL` so that requests send to `URL` will trigger the corresponding view function.

For example,the index function will deal with requests send to `http://localhost:1926/index/`. Requesting `http://localhost:1926/moha/` will trigger moha and get `闷声发大财`.

```python
app = Flask(__name__)
@app.route('/index/')
def index():
	return render_template('index.html')
@app.route('/quote/')
def moha():
	return '闷声发大财'
app.run('localhost',1926)
```

2. Flask provides a global object called `flask.request`. We can get the request method from  `flask.request.method` attribute. 

Firstly, include `POST,PUT,DELETE` and other http methods in the `methods` parameter of `Flask.route`.  
Secondly, determine the current http method using `flask.request.method`


```pyhton
from flask import request
@app.route('/method/',methods=['GET','POST'])
def view_func():
	if request.method=='GET': return render_template('page.html')
	else: return 'post req'
```

3. Store the template jinja2 page in `templates` directory and use `render_template` function.

Flask use `jinja2` as the default template engine. `jinja2` provides control flows e.g. `{% if %}{% endif %},{% for i in qwq %} {% endfor %}`, variable substitution e.g. `{{ query_result }}` and other powerful features.

```html
<!--in templates/fl.html -->
<!doctype html>
<html>
	<head>
		<title>Hello from Flask</title>
	</head>
	<body>
		<h3> flights </h3>
		<hr/>
		<ul>
			{% for i in flights %}
				<li> <p>{{ i.iata }}</p> </li>
			{% endfor %}
		</ul>
		</body>
</html>
```

```python
@app.route('/flights')
def dynamic_page():
	return render_template('fl.html',flights=get_flights_data())
```



4. Access to the posted data in a form via `flask.request.form` which is a python dictionary.

```python
@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login_form.html')
	else:
		un = request.form.get('username','')
		pw = request.form.get('password','')
		if un=='zeminjiang' and pw=='19260817':
			return 'success'
		else:
			return "I'm angry"
```


5. How to specify the title of a web page? How to add a paragraph to a web page? How to add a title to a web page?
6. How to design a form on a web page? How to add text box to your form? How to add an option to your form?
7. How to send the content of the form to the server? What HTTP methods are generally used for those requests? In Flask, how do you handle the request containing a form?


For 5, use `<title>;<p>;<h1>,<h2>..<h6>` tags.  
For 6, use `<form>,<input>` tags.  
For 7, specify the `action,method` attribute of `form` tag. Generally, we use `POST` for a form. use `request.form` to access the form data in a view function.

```html
<html>
	<head> <title>simple html form demo</title> </head>
	<body>
		<h1>Simple HTML page</h1>
		<hr/>

		<h2>paragraph</h2>
		<p>I hate involution. My GPA dropped dramatically.</p>
		<hr/>

		<h2>form</h2>

		<form action="/config/" method="POST">
			<input type="radio" name="led-mode" value="normal">normal on<br>
			<input type="radio" name="led-mode" value="blink">twinkling<br>
			airport <input type="text" name="airport" placeholder="PuDong"><br>
			<input type="submit" value="submit">
		</form>

	</body>
</html>
```


## Implementation

> - How do you share the flight data between the crawler and the control panel? Which approach do you choose?
> - Which parameters in your program is allowed to be changed?

**NOTE:** Details can be found in `interface_docs/communication.md`

We store the flights data in `redis`. For crawler controlling, we implemented a message queue with `redis publish,subscribe`.  
To access `redis` in python, we use a third-party redis client called `redis.py` [the github repository](https://github.com/andymccurdy/redis-py). It can be found on PyPI and installed by `pip install redis`(or `pipenv install redis`).  
Use `c = Redis.redis(host,port)` to create a connection and `c.get,c.delete,c.publish,c.pubsub` to perform different actions.

In `crawler.py`, we created a redis connection, subscribe the `control-crawler-*` channels. In `Crawler.spin()`, the program  keep checking whether there are any message and change the corresponding parameters. After each fetch, we use `redis_connection.set('flights',json.dumps(flights))` to transform python objects in to json strings and store it in `redis`.  
In `server.py`, we process the POST requests and publish message to inform the crawler that the parameters should be changed. (We shouldn't share `redis.Redis` objects between threads, but establishing connection every time a request come cause high latency. Fortunately, `redis.py` provides a connection pool which helps to resolve the problem)



- `fetch-interval`: the crawler fetch flights data on flightaware every `fetch-interval` seconds.
- `token-life`: the crawler try to get a new token every `token-life` seconds.
- `range`: a four-tuple representing the lattitude,longtitude of the center and north-west corner. The crawler only fetchs flights which are in the range.
- `refresh-token`: refresh the token immediately.

Moreover, primary parameters of the `LEDcontroller` are also provided on the control panel.  


--------------

~~clone our repository and give it a try for now!~~
