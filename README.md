# Main
[测速源码](./net_core.py)

1. 运行需要先安装所需的第三方库
2. 请自行准备服务器下载链接，并设定好测试持续时间，建议先跑一分钟看一下效果
3. 会生成net.csv数据文件，可以使用excel自行查阅网速
4. 会生成net.jpg图片文件，是对net.csv数据的绘制，方便直观了解网速情况，（看下网络质量，是否会存在突然断流的情况）

# net_speed_check
真实网络测速，检测本地与服务器的网络速度生成CSV数据文件，并绘制网速图

# 背景
最近使用梯子时候感觉网络波动似乎有点大，网速时好时坏，所以就需要用数据来验证一下。

网络上很多测速的，但实际感觉很不准，实际体验并没有很多第三方测速网站显示的那么好看，于是基本上不看网络上的那些测速脚本，直接看Youtube，开启检查看视频的时候就可以顺便看看网速。

Youtube感觉还是比较准确的，但是我突然萌生了一个想法就是，我想知道一天哪些时间段属于网络高峰，即出国的流量集中的时间段，不可能看一天Youtube然后人为去记录。

于是想到把网络数据记录下来，正好自己的梯子流量自己用还是比较富裕的，所以可以用来挥霍一下

# 代码设计思路
编程语言：Python

是否需要第三方库：是

代码设计思路：

首先思考的是如何统计流量的问题，网上找到了psutil

其次是下载的思考，一开始想的是用Python自带的urllib，但是后面转念一想，既然必须要用到第三方库，何不直接使用最爱的requests呢？于是选择使用requests用于下载文件

接着自然就是使用 pandas 结合 matplotlib 来绘图了，毕竟用过很多次，相对而言熟悉了很多，不过老实说每次写的时候都是看着以前的代码，没有去查api了

这再一次强化了对于代码必须做总结的理念，每个人都应该造 “自己的代码轮子” ，这会让你下次 Coding 更快

绘图过程遇到了一些问题，就是需要获取电脑的分辨率信息，虽然知道 Qt 可以，毕竟用 Pyside6 很多次了，但就是不想使用，因为 Pyside6 比较大，安装费时

查找后得到了 win32api win32con，尺寸信息用于绘图时候设置图片大小，最后自然就是存储图片了

选择使用多进程来实现：进程A负责一直下载，进程B负责一直统计流量

设计时候就没考虑多线程，因为Python多线程本质是计算机的调度，不能并行，虽然不确定这个会不会有影响，但是直接使用多进程就不存在这个问题了。

这里还出现了一个问题，就是希望可以自定义下载时间，以秒计算，不然流量就算再多，也经不起这么烧

假定30Mbits/s，一天就需要消耗流量：`30*60*60*24/1024/8 = 316.40625 GB`

30/8 = 3.75 也就是网速3.73Bytes/s，代码以字节作为计算单位而非比特，字节与比特换算关系：1Byte=8bits

multiprocessing.Pool 查询官方文档是守护进程，所以只需要让主线程结束就可以了，完美解决终止死循环的子进程的问题

接着就是需要在服务器提供一个下载文件的链接，方法很多可以ftp，创建一个指定大小的文件 `fallocate -l 500m 500m.txt`

# 使用
一天316GB，对于1T流量，也就是3天多一点点而已，所以一定要设置好运行时间

由于计算的是本机的网络流量，所以如果本机除了访问服务器，还在访问其他网站之类的话，会造成偏高，所以使用时候请关闭其他应用，只连接服务器，这样最准确了

并且需要服务器提供一个可下载的文件链接，下载到本地后会自动移除，会不停下载该文件

# 服务器提供下载链接
基本上所有linux发行版都内置Python，我们使用Python3

直接开启http服务：`python3 -m http.server 80`

后台开启http服务：`nohup python3 -m http.server 80 &`

如果是后台开启http服务，那就需要相应的关闭操作：`ps -ef | grep python`，`kill -s 9 pid`

对上述命令做一些解释，python3是因为python3不完全兼容python2，目前基本都是python3，python2已成历史

后台服务顾名思义执行命令后会挂在后台不会被中断，对比直接开启，我们如果使用ctrl+c终端的话会立刻停止，由于持续测速，所以一直开着比较好

如果你不知道后台服务怎么关，那就 reboot 命令直接重启服务器，或者就让它挂着也无所谓了
# vultr服务器测速文件地址
```
vultr_server = [
    ["韩国 首尔","http://sel-kor-ping.vultr.com/vultr.com.100MB.bin"],
    ["日本 东京","http://hnd-jp-ping.vultr.com/vultr.com.100MB.bin"],
    ["新加坡","http://sgp-ping.vultr.com/vultr.com.100MB.bin"],
    ["悉尼","http://syd-au-ping.vultr.com/vultr.com.100MB.bin"],
    ["德国 法兰克福","http://fra-de-ping.vultr.com/vultr.com.100MB.bin"],
    ["荷兰 阿姆斯特丹","http://ams-nl-ping.vultr.com/vultr.com.100MB.bin"],
    ["英国 伦敦","http://lon-gb-ping.vultr.com/vultr.com.100MB.bin"],
    ["法国 巴黎","http://par-fr-ping.vultr.com/vultr.com.100MB.bin"],
    ["美东 华盛顿州 西雅图","http://wa-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美西 加州 硅谷","http://wa-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美西 加州 洛杉矶","http://lax-ca-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美东 芝加哥","http://il-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美中 德克萨斯州 达拉斯","http://tx-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美东 新泽西","http://nj-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美东 乔治亚州 亚特兰大","http://ga-us-ping.vultr.com/vultr.com.100MB.bin"],
    ["美东 佛罗里达州 迈阿密","http://fl-us-ping.vultr.com/vultr.com.100MB.bin"],
]
```



