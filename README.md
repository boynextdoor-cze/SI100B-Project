# SI100B Project: Who is Flying over?

Welcome to the python programming project for SI 100B. In this project, you are going to build a web crawler that runs on a Raspberry Pi (a mini computer) to obtain real time flight data from a website called FlightRadar24 (or an alternative called FlightAware). You are going to control LED lights on an external circuit through the GPIO interface of your Raspberry Pi according to different scenarios and visualize your data analysis through graphs or a website. To be specific, you will build:

1. A crawler to get data from a flight information website;

2. A module that controls LED lights on an external circuit;

3. A module or a website that accepts input parameters to your crawler;

4. A module for analyzing and visualizing your data through plain graphs or a website.

All your programs run on a Raspberry Pi.

## Overview

The project contains four parts. Each part requires you to implement a particular functionality of the project. Generally, you have one week of time to finish one part. At the end of each week, you are required to submit your implementation (Python code), a report on how you implement this part. Also, a face-to-face check will be arranged, requiring you to explain how your implementation works to a TA.

The 4 parts are:

- **[Part 1](./docs/README.part1.md)**: Build your web crawler;
- **[Part 2](./docs/README.part2.md)**: Control the LEDs via GPIO;
- **[Part 3](./docs/README.part3.md)**: Build control panel;
- **[Part 4](./docs/README.part4.md)**: Perform data visualization;

## How to run the Project?

1. Install dependency

	```
	pip3 install -r requirements.txt
	```

2. In terminal run

	```
	python main.py
	or
	python3 main.py
	```

3. If the response of server is normal, enter `localhost:8000` in browser address bar, then you can see a beautifully rendered webpage.

4. You can change the arguments in the interactive interface, and see the visualized results in `Map` bar and `Data Visualization` bar.