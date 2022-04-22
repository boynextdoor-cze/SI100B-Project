# Project Report - Week 1 #

The report is finished by collaboration

## Workload Division ##

| Name   | Email Address                  | Responsible for                                              |
| ------ | ------------------------------ | ------------------------------------------------------------ |
| 彭程   | pengcheng2@shanghaitech.edu.cn | Focusing on HTTP-related knowledge, searching for reference and reading them<br />Consequently reviewing crawler code |
| 迟择恩 | chize@shanghaitech.edu.cn      | Analyzing data source from the website and basically implementing the crawler program |
| 刘翊航 | liuyh10@shanghaitech.edu.cn    | Writing interface document of the output data (for submissions afterwards) and adding small details to the code e.g. automatically obtaining token from the webpage |

## Preliminary Comment ##

#### Reference

- https://piazza.com/class_profile/get_resource/keihltlrsa273/ki9psuqgut31fs
	Week1(python-project) tutorial slides
- https://www.runoob.com/http/http-tutorial.html
	a tutorial on HTTP written in Chinese.
- https://blog.csdn.net/ysblogs/article/details/88530124
	A blog posted by ys recording how to include the "User-Agent" field in HTTP header when using requests.
- https://www.w3cschool.cn/http/
	TA recommended resource for http protocol.
- https://piazza.com/class_profile/get_resource/keihltlrsa273/ki8wxifbdo05jq
	How to get access to PI via SSH.
- https://docs.python.org/3/library/re.html
	official document for `re` module in python standard libarary. Teaching us how to use regex to extract valuable things from unstructured data.
- https://requests.readthedocs.io/en/master/
	the document for `requests ` a HTTP client module.
- https://www.runoob.com/git/git-tutorial.html
	a tutorial on git, explaining basic concepts used in git and the usage of git-cli.
- https://baike.baidu.com/item/IPv4
	baidu baike entry for IPV4. We got to known the meaning of `192.168.0.0/16`.
- https://wiki.archlinux.org/index.php/NetworkManager
	Network configuration on linux(using networkmanager)
- https://wiki.archlinux.org/index.php/Network_configuration#Static_IP_address
	How to set static IP on raspberrypi.

#### Encountered difficulties

- How to manually set the range of longitude and latitude in the request so that we can get the data from a certain area
- How to understand the paraments in the data source and how to verify our guesses
- How to automatically get the token
- How to find out the meanings of the response fields

## Data Source ##

- URL1:https://zh.flightaware.com/ajax/vicinity_aircraft.rvt?&minLon=81.5625&minLat=-28.100624084472656&maxLon=180&maxLat=9.03900146484375&token=9e355d25f4bd2ab6dbd05a77ee2e5043aada8710

Method: `GET`

Response format (for body) is supposed to be a json string. However the `Content-Type` is set to be `text/html; charset=utf-8`

Conversion method: We used `json.loads()` to convert it into a Python object

Explanation:

1. `https://`  Protocol

2. `zh.flightaware.com`  Host

3. `/ajax/vicinity_aircraft.rvt`  Path to the resources

4. `?&minLon=81.5625&minLat=-28.100624084472656&maxLon=180&maxLat=9.03900146484375&token=9e355d25f4bd2ab6dbd05a77ee2e5043aada8710`  Query string with parameters separated by `&`

	Remark: Semi-columns can also be used as the separators of parameters

The HTTP response consist of a header and a body separated by `\r\n\r\n`.

The header consists of status code, explanation for body and other MISC information.

An example of header:  

```Plain Text
HTTP/1.1 200 OK
Server: nginx/1.17.9
Date: Tue, 08 Dec 2020 06:13:35 GMT
Content-Type: text/html;charset=utf-8
Content-Length: 24391
Connection: keep-alive

{"type":"FeatureCollection"}
```

The body is a JSON string representing a javascript object.
A json object is a set of KV pairs, where K is a string and V is another valid JSON object (can be string, number, boolean, null, array or object)

##### Interpretations of the response body (only reserved essential data that README.md required, removed unnecessary parts): #####

The `features` field is an array of flight objects. 

For every flight:

- The `gemoetry:coordinates` field indicates where the airplane was, the first parameter is the longitude and the second one is the latitude

- The `properties` field:

	- `direction`: The number is an angle indicating to which direction the plane is heading. The angle range is from 0° to 359°, where 0° is north, 45° is northeast, 90° is east, 135° is southeast, 180° is south, 225° is southwest, 270° is west and 315° is northwest.

		On the website, there are some arrows indicating the approximate direction of the head of the plane. To clearly explain it would be quite complicated, so the further explanation will be given in face-to-face check section.

	- `ident`: The flight number of the flight which consists of a prefix (capital letters only) representing the airline and a suffix (Arabic numerals only) to uniquely code the flight

	- `iata` in fields of `origin` and `destination`: The International Air Transport Association Airport Code of the departure airport and destination airport

	- `altitude`: The present altitude of the plane. **To be noticed**, actually, the unit of the data is `Hundreds of feet`. For example, if the data is `360`, then the actual altitude is `36000ft`, and according to the unit conversion, consider international system of units, it is approximately equivalent to `10972.8m`, which would be displayed on the website. How we found such property will be further explained in face-to-face check section.

	- `groundspeed`: The plane's speed to the ground. **To be noticed**, actually, the unit of the data is `knot`. For example, if the data is `360`, it means the present speed is `360kn`, and according to the unit conversion, consider international system of units, it is approximately equivalent to `666.72km/h`, which would be displayed on the website. How we found such property will be further explained in face-to-face check section.

```json
{
    "type":"FeatureCollection",
    "features":
    [
        {
            "geometry":
            {
                "type":"Point",
                "coordinates":[40.50629,51.76492]
            },
            "properties":
            {
                "direction":359,
                "ident":"AFL501",
                "origin":
                {
                    "iata":"TLV",
                },
                "destination":
                {
                    "iata":null,
                },
                "altitude":360,
                "groundspeed":449
            }
        }
    ]
}
```

- URL2:https://zh.flightaware.com/live/

Method: `GET`

Response format: `text/html`

Conversion method: We used `re`(regular expression) to extract the token

Explanation:

1. `https://`  Protocol
2. `zh.flightaware.com`  Host
3. `/live/`  Path to the resources

```Plain Text
HTTP/1.1 200 OK
Server: nginx/1.17.9
Date: Tue, 08 Dec 2020 06:50:49 GMT
Content-Type: text/html;charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive

<html>
<head></head>
<body>
	<script>var mapGlobals = {"VICINITY_TOKEN":"12154b0c2c75c8106af1276a0203a771c8d89731","DEBUG_ENABLED":false};</script>
</body>
</html>
```

The header is similar with the previous one, so the explanation is omitted.

Explanation of body:
The body is written in HTML describing a webpage, including content of the webpage, hyperlinks to other webpages and links to static files. However, they do not matter.
What really matters is that we found the `token` in the script tag.

Remark: We also find something really useful in the script tag. This will be further explained in face-to-face check section.

## Implementation ##

used packages and modules are listed below.

- `requests` for sending HTTP requests and parsing HTTP response.
- `re` for regular expression support. We used regex to extract token from webpages.
- `json` for conversion between JSON strings and python objects.
- `time` for `time.sleep(interval)`. The crawler would fetch flights data every `interval` seconds to protect our IP address from being banned by the server.
- `pprint` for prettifying the debug output.

