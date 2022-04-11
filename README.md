# SI 100B Project: Who is Flying over?

Welcome to the python programming project for SI 100B. In this project, you are going to build a web crawler that runs on a Raspberry Pi (a mini computer) to obtain real time flight data from a website called FlightRadar24 (or an alternative called FlightAware). You are going to control LED lights on an external circuit through the GPIO interface of your Raspberry Pi according to different scenarios and visualize your data analysis through graphs or a website. To be specific, you will build:

1. A crawler to get data from a flight information website;

2. A module that controls LED lights on an external circuit;

3. A module or a website that accepts input parameters to your crawler;

4. A module for analyzing and visualizing your data through plain graphs or a website.

All your programs run on a Raspberry Pi.

## Getting Started

You should have received a batch of gears from the SI 100B teaching team. Please take good care of them and make sure they are in a sound condition when you return them to us. Below is a list of components we hand out. Please check yours against them. If there is anything missing or broken, contact us as soon as possible so that we can give you a replacement.

| Item                 | Quantity |
| -------------------- | -------- |
| Raspberry Pi         | 1        |
| LED GPIO connector   | 1        |
| USB Charger          | 1        |
| Ethernet cable       | 1        |
| USB Ethernet adapter | 1        |
| LED                  | 4        |

First, you need to connect your Raspberry Pi to the Internet through Wi-Fi or the Ethernet port on your board. First, turn on the switch on the charger and connect your Pi to it. Your Pi will be powered up automatically. The red LED indicator on the corner of the board near the USB connector will light up if your Pi is on. The green LED indicator next to it will blink if your Pi’s SD card has been accessed.

After connecting your Pi to the network, you are going to figure out ways of extending I/O of your Pi. There are two ways of doing it. The first one is the simplest: you are directly connecting a monitor and a set of keyboard and mouse to it. The second one is to connect to it with SSH via network. The second approach is a little more complex but is recommended by the teaching team. We will give you bonus to your project if you choose the SSH way. Below are details for these two. 

### Connect with Keyboard and Mouse

The Pi itself is a single board computer that runs Linux. To make it fully functional, all you need to do is attaching a screen and a set of keyboard and mouse to it. 

The Pi comes with a HDMI port for connecting to your monitor and 4 USB ports for connecting with your mouse and keyboard. If you have compatible hardware, you can connect your Pi to them and use your Pi like what you will do with a normal computer. If you currently do not have them, you can choose to come to the computer lab in TBA. The hours of the lab will be announced on Piazza.

After the Pi boots up, the user interface will appear on the screen. If you choose to use the wire connection, just plug in a cable to the Ethernet port and the LED indicator on the port will be turned on and blink, which means a connection is established. Alternatively, you can connect to Wi-Fi. Simply choose the network you want to connect to from the drop-down menu on the upper right corner of the screen and log in with your credentials if asked. A side note is that if you are connecting to the campus network via the ShanghaiTech Wi-Fi or through an Ethernet port, you may need to do web portal authentication as you will do for any other devices using those two networks. You can simply open the FireFox browser on your Pi or use those handy [scripts](https://github.com/ShanghaitechGeekPie/WifiLoginer).

Alternatively, configuring your Pi with a SSH server and debugging on your own computer is also a feasible way.

### Connect with an SSH Terminal

If you do not have any USB keyboard, mouse or monitor, you may need to connect to the Pi via SSH.  SSH allows you to connect to your Pi from another computer securely in the same network. To enable SSH, simply follow the [instructions](https://www.raspberrypi.org/documentation/remote-access/ssh/) in the official documentation. If you have enabled SSH on your Pi, do remember to change your SSH login password. To change your password, simply run `passwd` on your terminal window after login. You may be prompted for your current password. If it is the case, the default password of your Pi is` raspberry`.

To connect to your Pi via SSH, you also need an SSH client on your computer. If it is running macOS or Linux, your computer is shipped with an SSH client. If you are using Windows, you are recommended to use the [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10). To connect to your Pi in this way, you will need to connect your Pi to your laptop with the Ethernet. You will need an Ethernet dongle for this purpose if your laptop is not equipped with Ethernet ports.

After connecting your Pi with your computer with cable, your computer and Pi will both negotiate a set of addresses in the same network called linked local address which could be used to connect to your Pi. Then in your terminal, you can connect to the Pi with `ssh pi@raspberrypi.local` . This way may not work out on some systems (esp. some version of Windows) with limited IPv4 link local address support or mDNS support; in this case, you need to assign your computer a static IP address in `169.254.0.0/16` (e.g., `169.254.100.100`), or consult this [article](https://raspberrypi.stackexchange.com/questions/85747/setting-a-static-ip-from-boot-drive-headless-static-ip) or this [article](https://www.cnblogs.com/sheng9hhd/p/10294859.html). Instructions for assigning static IP address to an interface could be found [here](https://support.apple.com/zh-cn/guide/mac-help/mchlp2718/mac) for macOS, [here](https://kb.netgear.com/27476/How-do-I-set-a-static-IP-address-in-Windows) for Windows or [here](https://danielmiessler.com/study/manually-set-ip-linux/) for Linux.

This will not give your Pi access to the Internet which is needed for this project. You may also need to connect your Pi to the campus wireless network. To do this, you can follow this [documentation](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) or simply attach a screen and a set of keyboard and mouse to your Pi and connect to `ShanghaiTech` or `eduroam` network (you only need to do this for once and your Pi should be able to connect to the network next time). You may need to do network login via the web portal. In this case, you may use those handy [scripts](https://github.com/ShanghaitechGeekPie/WifiLoginer).

### Get the Framework

We are distribting the framework with GitLab which you should be familar with in the Python Programming Part. The only difference is that in order to aid you to work with your teammates, we created a GitLab Group for each team which only your team member have access to. To get started, visit your code base in  **your team group** (whose name starts with *Python Project Team*).

### Install Dependency

Another thing you need to do is to install the required packages (dependencies) of the project. You can do this by downloading the packages from the PyPI. In the terminal of your Pi (or a shell SSHed into the Pi), in the root directory of your repo, execute the following:

```bash
pip3 install -r requirements.txt
```

`requirements.txt` records the detailed required packages.

## Overview

The project contains four parts. Each part requires you to implement a particular functionality of the project. Generally, you have one week of time to finish one part. At the end of each week, you are required to submit your implementation (Python code), a report on how you implement this part. Also, a face-to-face check will be arranged, requiring you to explain how your implementation works to a TA.

The 4 parts are:

- **[Part 1](./docs/README.part1.md)**: Build your web crawler;
- **[Part 2](./docs/README.part2.md)**: Control the LEDs via GPIO;
- **[Part 3](./docs/README.part3.md)**: Build control panel;
- **[Part 4](./docs/README.part4.md)**: Perform data visualization;

The specification for each part is located in` docs` directory of this repo. Check them for detailed requirements for each step.

This project (esp. the framework itself) is only supposed to work in a modern Linux system. During the face-to-face check, your project should only run on the Debian Linux on the Pi from the teaching team. During the face-to-face checking, demonstrating the project using other devices or OS is considered invalid and will face score deduction. However, you are highly encouraged to implement and debug it on your local system.

## Collaborating with Your Teammate(s)

The team size is 2 or 3. You need to describe how the workload is divided among the team members in your weekly project report. We take the workload division into consideration when grading.

The best practice is to use git as the versioning and collaborating tool with your teammate(s). With git, you can have a clean split between the *development* phase and the *test* phase. Commonly, you will finish the development phase (writing your prototype) on your own computer then synchronize the code to the Pi and complete your testing part.

We have created a Group on GitLab for each team in which you can collaborate with other members of your team.

## Submission

Submission of the project is on a per-team-basis. Your team need to submit the following every week in order to get full score:

* A report describing the work you have done in this week as PDF to Gradescope. One submission from one student is sufficent for a team. When multiple submissions present, we will grade the latest one;
* Your fully functional implementation of this week's task to GitLab by creating a new tag in **your team's** project codebase.

You also need to attend the face to face check arranged in the lecture time. The due date of your code and report and the time for check for each week is noted on the documentaion of each week in the `docs` directory of the codebase. The template of report is presented in the `reports` directory.

## Web basics

Instead of describing some concepts like TCP/IP in a tedious way, this part of the document is aimed at giving you some general ideas of web and (hopefully) helping you to understand how a web crawler works better in the following READMEs. So a basic understanding is enough - but if you are too confused to have a general idea, just search for the relative bold words (粗体字) in your browser. We don't specify every one of them since we don't want to flood you with tons of new and not-so-relevant ideas.

### Typical Web Request and Response

When you type in `https://sist.shanghaitech.edu.cn/` (a **URL**) in your browser and wait for the fully-loaded version of the SIST's website, you are actually watching your browser (called a **client**, or user agent) communicating with some computers in the clouds (the **server**). The Web uses a protocol called HTTP for this kind of communication. What the browser do is parsing the URL you typed in and search for the **IP address** corresponding to the domain `sist.shanghaitech.edu.cn` and forges a TCP connection with the IP. After connecting with the server, your browser sends out **HTTP requests** to the server. Then SIST's server receives the message and runs an application to process the request, after which an **HTTP response** message containing the result from the application is sent back to your browser.

 If all of these processes work smoothly, you will see a neat layout of the SIST website after your browser finishes rendering the message.

### HTTP Basics

HTTP, or the Hyper-text Transfer Protocol, is the underlying protocols used by web server and your web browsers to transfer data. In this part, we will describe **HTTP request** and **response** in detail - since this is important for your project.

An **HTTP request** includes 

- a request line - this includes how to forge a connection with the resource (a.k.a. **method**) including  `GET` and `POST` , which the resources you want to access (signatured by a **URL**), and the HTTP version;
- **request header fields** - they are basically some key-value pairs indicating information of the request;
- and an optional message body - this is what you need to consider when you want to post something.

An **HTTP response** includes

- a status line - this includes HTTP version, **status code** (this indicates the status of the request - is it successful? If an error has occurred, was it the problem of the server or the client?), and reason message;
- response header fields - this is similar with that of an HTTP request but indicates response information;
- and an optional message body - its form depends on the value of a key named `Content-Type` , which is specified in response's response header fields.

An example of **HTTP request** / **response** is given below. 

The client (user agent) sends out the following request

```
GET / HTTP/1.1
Host: www.example.com
User-Agent: curl/7.54.0
```

The server will typically reply with the following

```
HTTP/1.1 200 OK
Server: nginx/1.14.2
Date: Thu, 16 Jul 2020 12:42:13 GMT
Content-Type: text/html; charset=utf-8

<html>
<head>
<title>Welcome</title>
</head>
<body>
<p>It works!</p>
</body>
</html>
```

This conversation is basically for the client trying to get the `/` directory of the server `www.example.com`. The server replies with a `200` status code, indicating the request is successful and the content of the requested resource is attached below the headers as `<html>....</html>`. Other possible status codes include `400` indicating the client’s request could not be processed, `404` indicating the resource could not be found on the server and `500` indicating an error occurred inside the server when processing the request.

For more information about HTTP, see the [W3School](https://www.w3schools.com/whatis/whatis_http.asp) and [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview).

### HTML

HTTP solves the problem of transferring a file from a computer to another. HTML, or the **H**yper **T**ext **M**arkup **L**anguage, solves the problem of encoding the style information of a web page. It represents the documentation as a tree of labels.

For more information about the HTML, see [W3School](https://www.w3schools.com/whatis/whatis_html.asp) and [MDN](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics).

### What is web crawling?

After having a general idea of what is mentioned above, it is a reasonable time for you to understand what a web crawling is and how it works.

Web crawling or scraping is the practice of gathering data through any means other than a program directly interacting with an API (or, obviously, through a human using a web browser). This is most commonly accomplished by writing an automated program that queries a web server, requests data, get response and then parses the response message to extract needed information.

Specifically, for a general web crawler, it follows the following working pipeline:

- retrieving HTML data from a domain name; 
- parsing that data for target information;
- storing the target information;
- Optionally, moving to another page to repeat the process.

In this project, you will implement the first three of them. Have fun with it!