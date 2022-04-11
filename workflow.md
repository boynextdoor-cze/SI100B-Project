# workflow&schedule for SI100B-PYproj

## members

- cze: responsible for data retrieving/formating/cleaning
- lyh: responsible for frontend+data visualization
- pc:  responsible for backend


## workflow


1. **finish your share of work ASAP**
2. record encountered difficulties and solution (`when,what` describe the issue; `why,how` show the process of resolving the problem)
3. prepare for questions that TAs might ask in F2F check.


4. explain these things to teammates.
5. code review


## reminder

- academic integrity
- make record of everything(what have you seen and what have you done)
- help each other
- be friendly, be patient
- `TimeToStop = None`
- don't worry to branch out when necessary
- write clear,complete commit message


## todo

- [x] Merge `redis-communication` branch into `master`
- [x] Fix `range` field for `GET /crawler/,POST /crawler/` (`interface_docs/communication.md`,`web_server/server.py`,client side is involved)
- [x] Fix `LED controller`, 合理使用PWM避免频闪
- [x] Design and implement `LEDcontroller.mode`
- [ ] Support for more LED display mode.
- [ ] Add a LED-BLUE to show whether the amount of flights is too large to display on the LED array.
- [ ] Add data validation on server side.
- [ ] Resolve the None return value from `redis.get`
- [ ] Add 'watch-mode' for the project. client side and server side are involved
- [ ] Show prettified and formated raw data json on web client.
