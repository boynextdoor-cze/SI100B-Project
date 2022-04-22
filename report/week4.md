# Project Report - Week 4

The report is finished by collaboration

## Workload Division ##

| Name   | Email Address                  | Responsible for                                                      |
| ------ | ------------------------------ | -------------------------------------------------------------------- |
| 彭程   | pengcheng2@shanghaitech.edu.cn | Implementing visualization images with matplotlib on backend.        |
| 迟择恩 | chize@shanghaitech.edu.cn      | Implementing communication part between client side and server side. |
| 刘翊航 | liuyh10@shanghaitech.edu.cn    | Implementing UI.                                                     |

## Preliminary Comment ##

#### Reference

- [matplotlib official document:tutorial](https://matplotlib.org/tutorials/index.html) Data visualization with matplotlib matplotlib.
- [flask official document](https://flask.palletsprojects.com/) Build simple webapp with flask framework.
- [jinja2 official document](https://jinja.palletsprojects.com/) Resolve the conflits between jinja2 and vue.js
- [MDN docs: data URI](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/data_URIs) Transmit images between server and client.
- [geeksforgeeks: vector graphics&raster graph](https://www.geeksforgeeks.org/vector-vs-raster-graphics/) The differences between raster graphics and vector graphics, this is the reason why we chose SVG(Scalable Vector Graphics).
- [stackoverflow: how to extend the margin at the bottom of a figure](https://stackoverflow.com/questions/27878217/how-do-i-extend-the-margin-at-the-bottom-of-a-figure-in-matplotlib) Fix bugs: the figure in matplotlib may exceeed the range of the image. 
- [stackoverflow: misplaced xlabel in matplotlib](https://stackoverflow.com/questions/27083051/matplotlib-xticks-not-lining-up-with-histogram) How to fix the misplaced ticks on the x-axis. 
- [Vue.js official site](https://cn.vuejs.org/) Use vue.js to create a responsive client side application.
- [Vuetify.js official site](https://vuetifyjs.com/) Create a fancy UI with the help of Vuetify.
- [vuejs CLI usage](https://cli.vuejs.org/) How to manage your node.js project with vue-cli.
- [axios official site](http://www.axios-js.com/) Send XHR(AJAX) with axios.
- [MDN docs:pushState](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState) How to use pushState API to create a non-refresh page.
- [numpy manual](https://numpy.org/doc/1.19/) A easier way to process data.

#### Encountered difficulties

- How to avoid figure exceeding the border of the image in matplotlib 
- How to fix the misplaced ticks on the x-axis
- How to make a responsive, non-refresh client side program. 
- How to communicate between client side and server side. 
- Matplotlib halted because of thread unsafety.  

## Advanced: `matplotlib` and Flask

- How to create a plot in `matplotlib`?
  
```python
    from matplotlib.figure import Figure
    # Import figure from matplotlib.
    matplotlib.use("AGG")  
    # Using a matplotlib bultin non-interactive backend, supporting "raster graphics -- high quality images using the Anti-Grain Geometry engine"
    matplotlib.interactive(False) # Turn out the interactive backend.
    # Using non-interactive backend on web servers are more efficient,
    # while using interacive backend can create a interactive refreshing images.  

    x = np.linspace(-1, 1, 100)
    # Using numpy to create 100 numbers, uniformly distributed in [-1, 1].
    fig = Figure(figsize=[8, 4])
    # Create a figure with size 8 inches(width) by 4 inches(height). 
    fig.subplots().plot(x, x**2)
    # Plot y = x ** 2 on the figure.
    fig.savefig(path, format="png")
    # Save the figure as PNG. 
```

- How to draw line graph (折线图), histogram (直方图), bar chart (条形图) and pie chart (饼状图)?

```python
    axs = fig.subplots()
    # Find the axis system for the figure.  
    # For line graph:
    axs.plot([1, 2, 3, 4], [1, 4, 2, 3])
    # Pass Xs and Ys to the plot function, it will draw a line graph.
    # For histogram:
    axs.hist(self.data, bins=range(0, 15000+1500, 1500),
        color=colors['teal lighten-2'])
    # Pass data(an array), bins(an array) to the hist function. 
    # This is used in the data visualization part.
    # For bar charts:
    axs.bar(['cze', 'pc', 'lyh', 'diaozh'], [4, 4, 0, 10**8])
    # Pass a array for labels, another array for values. 
    # For pie chart:
    axs.pie(np.array(list(self.arrival.values())) / (self.weight_all),
                          labels=self.arrival.keys(),
                          colors=colors.values())
    # Pass a list of data, labels of it.
    # This is used in the visualization part. 
```

- How to change the legend, x-axis label and y-axis label of a graph?

```python
    axs.legend((line1, line2, line3), ('label1', 'label2', 'label3'))
    # Draw 3 legends respectively for line1, line2 and line3
    axs.set_xlabel("The x-axis label you want to change")
    axs.set_ylabel("The y-axis label you want to change")
```
- How to save the plot as a image?

```python
    fig.savefig(path, format="png")
    # Pass the path parameter with the path you want to save, and the format parameter with the format. 
```

- How to serve image (or any static file) with Flask?

```python
    # Method 1
    
    # Put any static files you want to send to the client side in the folder "/static", "/" is the root of your website. Access the file you want to send directly. Let's say, you save an image named "test.png" under /static, and the server is running on local host, then you should access 'http://localhost/static/test.png'
    
    # Method 2, using flask send_file method like follows:
    
    return send_file("templates/index.html")
    # The string passed as the parameter is the relative path of the file to be sent. 
```

- How to add a route (that handles new URLs) to Flask?

```python
    # use decoraters like the following examples
    # the string is the path in the URL, while the methods indicating the capable methods to be received by the server. 
    # the decoraters decorate the methods who handles this request.
    @web_server.route('/', methods=['GET'])
    @web_server.route('/index/', methods=['GET'])
    @web_server.route('/home/', methods=['GET'])
    @web_server.route('/config/', methods=['GET'])
    @web_server.route('/vis/', methods=['GET'])
    @web_server.route('/about/', methods=['GET'])
    @web_server.route('/raw/', methods=['GET'])
    def vue_interface():
        return send_file("templates/index.html")
```

- How to render a HTML template with Flask with parameters?

```python
    # Use render_template function in Flask
    render_template('test.html.jinja', test=True, year=time.localtime(time.time())[0])
```
For example, the former call the render_template function. Jinja will search test.html.jinja file in the /templates folder, and replace the `{{ year }}` with the server time. And the following "inner HTML" will be shown if `test` is `True`. 
```HTML
    This year is {{ year }}. 
    {% if test %}
        <br />
        This is a test version. Don't run it in production environments.
    {% endif %}
```

## Implementation

- Describe the overall workflow of this part of this project, including answers to the following bulletin points.
    - When do you update your graph? When the new data comes, or when the user request comes?   
        When the data from the crawler is updated, and user click on the refresh button. 
    - How do you store the data used for rendering the graph?
        Use `json.dumps(pyobj)` to serialize a python object and store it in redis as JSON string. Use `redis.py` for access redis KV cache in python(create a connection(or client) object, use `conn.set,conn.get` to manipulate KV pairs, and `conn.pubsub` for implementing publisher/subscriber model).
    - How do you store the graph after being rendered by `matplotlib`?
        ```python
            fig.savefig('test.svg', format="svg")
            # Use the fig.savefig funtion
        ```
    - How is the image served to the user?
        Through the vue.js client side program, using `<img>` tag, like follows:
        ```HTML
            <img src="The source of the images" style="width: (The width of the image); height: (The height of the image)" />
        ```
        The sources of the images are data URI. A data URI is contructed as below:
        ```
            data:[<mediatype>][;base64],<data>
        ```