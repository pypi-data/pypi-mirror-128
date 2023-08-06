# Vxy

#### 介绍
普通视频制作双排vr效果，确定切割率和左右x1，x2的关系和结果脚本。


#### 教程

1.  通过`pip install vr.xy`安装本模块
2.  `vr -h`查看模块参数
3.  `vr -p 0.7 -l 0.12 -r 0.18`用来获取双竖屏的x1,x2

#### 公式
$$
f(H)=
\begin{cases}
x_1=(\frac{1}{2}-L)WP & \\\\        
x_2=(1-\frac{P}{2}+PR)W
\end{cases}
$$

$$
f(V)=
\begin{cases}
x_1=... & \\\\        
y_1=... & \\\\        
x_2=... & \\\\        
y_2=...
\end{cases}
$$

$$
0.45 <= [1-(L+R)]P <= 0.55
$$

#### 图示说明

1.  左侧x1图示横向
![左侧x1图示横向](image/Imagevv.jpg)
2.  右侧x2图示横向
![右侧x2图示横向](image/Imagevv2.jpg)    

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
