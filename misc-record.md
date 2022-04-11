# Record-MISC

> - random thought on the project
> - encountered issues and workaround/solution

## 2020.12.22: double run

### description

运行main,观察log.  
发现visualizer的log有两份,crawler的log偶尔也会有两份.


### exploration&explanation

1. 起初认为两次log是同一个process输出,是通信出了问题(可能是个race-condition)导致消息被收发两次.  
   于是在visualizer的log中插入pid,ppid.发现他们来自不同进程.  
   所有log中插入pid信息,并使用工具观察进程树.  
	 发现多出来的visualizer process的parent process并不是main或者main的child proc.
2. 尝试让main只启动visualizer,发现问题消失,意识到这是其他的进程影响了它.  
   进一步尝试定位问题:有start server则出现上述问题,不让main启动web server则不会出现问题.  
3. 尝试让run server在start crawler,start LEDcontroller,start visualizer之前/之后运行.问题仍然出现.  
4. 此时意识到是run server的调用树中包含fork,复制了main的代码,导致重复执行.  
5. 查阅资料发现flask在debug mode下会有fork操作. 关闭debug再次运行main,问题消失.


### workaround

关闭flask web app的debug mode.



