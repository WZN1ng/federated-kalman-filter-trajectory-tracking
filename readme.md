# 基于联合卡尔曼滤波的轨迹跟踪算法

​	本项目作为现代数字信号处理课程设计，仅供参考。

### 一、数据清洗

​	利用NGSIM车辆轨迹数据集进行仿真，该数据集由美国交通部提供，面向自动驾驶等方向的研究，其中记录了超过上千辆车在各时刻的位置、速度等信息。

​	由于原始数据非常庞大且复杂，我们难以直接使用，所以需要对数据进行清洗。首先对数据集按照总帧数进行排序，选取其中记录条数最多的若干量车作为研究对象。抽取选中车辆的有效信息并按帧编号排序后分别保存为各个车辆的有效数据集，方便后续读取使用。抽取的信息栏目具体如下表所示。

| 信息栏目   | 数据集表示  |
| ---------- | ----------- |
| 车辆编号   | Vehicle_ID  |
| 帧编号     | Frame_ID    |
| 总出现帧数 | Total_Frame |
| 相对横坐标 | Local_X     |
| 相对纵坐标 | Local_Y     |
| 车辆速度   | v_Vel       |
| 车辆加速度 | v_Acc       |

### 二、卡尔曼滤波

​	针对该数据集，各局部节点均采用卡尔曼滤波方法来实现对车辆轨迹的追踪和预测。由于需要模拟多传感器的情况，所以将数据集中的相关数据假定为真实状态信息，在读取数据时每个传感器都在此基础上附加一个白噪声作为各自的观测信息。为每个局部滤波器设置了不同的随机数种子，以此确保各局部滤波器添加的观测噪声是无关的。

​	设实验对象的状态转移方程和观测方程分别为：

$$
X_k=FX_{k-1}+W_{k-1}\tag{1}
$$

$$
Y_k=HX_k+V_k\tag{2}
$$

​	其中，$X_k,Y_k$分别表示$k$时刻的状态向量和观测向量，$F_{k,k-1},H_k$分别是状态转移矩阵和观测矩阵，$W_{k-1},V_k$分别是系统噪声和观测噪声（此处均定义为零均值的白噪声，$\mu_W=\mu_V=0,\sigma_W=\sigma_V=1$）。

​	针对该具体问题，由于数据集是由摄像头获取的，其加速器数据的准确性存疑，所以将状态向量设为$X_k=(x_k,v_{x,k},y_k,v_{y,k})$，其中$x_k,y_k$是车辆位置的坐标，$v_{x,k},v_{y,k}$ 是车辆速度在坐标轴方向的两个分量。考虑到观测信息作为传感器直接获得的数据，将其假设为GPS或其他定位传感器，获取数据集中可靠性最高的位置数据即$Y_k=(x_k,y_k)$ 。

​	由此，状态转移矩阵和观测矩阵如下所示，由物理建模得到，其中$dt=0.1$。

$$
F=\left[\matrix{1 & dt & 0 & 0 \\
						0 &  1 & 0 & 0 \\
						0 &  0 & 1 & dt\\
						0 &  0 & 0 &  1}\right],H=\left[\matrix{1 & 0 & 0 & 0\\
							0 & 0 & 1 & 0}\right]
$$

​	各局部滤波器分别对自身数据进行迭代，完成对目标车辆轨迹的追踪和预测。设各局部滤波器的初始状态$X_0=(x_0,0,y_0,0)$，初始误差矩阵为$E_{0,0}=0_{4×4}$。记$Q_{W,k},Q_{V,k}$分别为系统噪声和观测噪声的相关矩阵，其迭代过程如下：

​	一步预测方程：

$$
\hat{X}_{k+1|k}=FX_k\tag{3}
$$

​	预测误差递归方程：

$$
E_{k+1|k} = FE_{k|k}F^T+Q_{W,k}\tag{4}
$$

​	计算卡尔曼增益：

$$
G_{k+1}=E_{k+1|k}H^T(HE_{k+1|k}H^T+Q_{V,k+1})^{-1}\tag{5}
$$

​	根据观测校正预测：

$$
X_{k+1}=\hat{X}_{k+1|k}+G_{k+1}(Y_{k+1}-H\hat{X}_{k+1|k})\tag{6}
$$

​	校正误差递归方程：

$$
E_{k+1|k+1} = (I-G_{k+1}H)E_{k+1|k}\tag{7}
$$

​	上述即为局部滤波器一轮迭代的全部计算过程。

### 三、联合滤波示意图

<img src="/DSP/res/federated kalman.png" alt="img" style="zoom: 50%;" />

<img src="/DSP/res/framework.png" alt="img" style="zoom: 67%;" />

### 四、仿真结果

在数据集预处理过程中，抽取了7辆车（编号分别为75、137、1170、1210、1325、2435、2484）的轨迹数据作为仿真基础数据。仿真参数设置如下表：

| 参数名称               | 参数值 |
| ---------------------- | ------ |
| 局部滤波器(终端)数量   | 10     |
| 全局滤波器(服务器)数量 | 1      |
| 是否同步更新           | True   |
| 最大迭代次数           | 1000   |
| 局部滤波器更新间隔     | 5      |
| 时间元dt               | 0.1    |
| 系统噪声标准差         | 1      |
| 观测噪声标准差         | 1      |

经过联合卡尔曼滤波器处理，其轨迹跟踪及预测效果分别如下图所示：

<img src="/DSP/res/Trajectory of Car 75.png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Trajectory of Car 137.png" alt="img" style="zoom:40%;" />

<img src="/DSP/res/Trajectory of Car 1170.png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Trajectory of Car 1210.png" alt="img" style="zoom:40%;" />

<img src="/DSP/res/Trajectory of Car 1325.png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Trajectory of Car 2435.png" alt="img" style="zoom:40%;" />

<img src="/DSP/res/Trajectory of Car 2484.png" alt="img" style="zoom:40%;" />

​	由上图可知，红色叉号表示对车辆轨迹的追踪预测，蓝色小点表示车辆的实际轨迹，两者的拟合得相对较好，这说明对车辆轨迹的追踪和预测任务大体上得到了完成。下面将详细分析误差情况。

### 五、误差分析

选取其中较为均衡的137号车作为分析对象，不同更新间隔得到的均方误差如下图所示：

<img src="/DSP/res/Error of Different Intervals (Car 137).png" alt="img" style="zoom: 67%;" />

​	由上图可以看出，随着更新间隔的增大，误差也会快速增大。最左侧的误差可能是由于初始状态设置的与实际值相差较大，尤其是其中的速度分量直接置为0，但实际情况可能不是这样，所以需要一个拟合的过程。而右侧突然剧增的误差可能对应着轨迹中137号车辆的一个急转向动作，如下图绿圈中所标注的。此时，由于惯性滤波器预测可能会和实际位置有较大的偏差。而当车辆平稳直线行驶时，由上图可以看出更新间隔对误差的影响几乎不存在，因此这说明了小的更新间隔能够为滤波器提供更高的跟踪容错率，使其在实验对象属性发生快速变化时能够得到及时调整。

<img src="/DSP/res/Trajectory of Car 137(2).png" alt="img" style="zoom: 67%;" />

​	其他车辆数据集轨迹追踪的误差随更新间隔的变化如下所示：

<img src="/DSP/res/Error of Different Intervals (Car 75).png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Error of Different Intervals (Car 1170).png" alt="img" style="zoom:40%;" />

<img src="/DSP/res/Error of Different Intervals (Car 1210).png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Error of Different Intervals (Car 1325).png" alt="img" style="zoom:40%;" />

<img src="/DSP/res/Error of Different Intervals (Car 2435).png" alt="img" style="zoom:40%;" /><img src="/DSP/res/Error of Different Intervals (Car 2484).png" alt="img" style="zoom:40%;" />

​	对比轨迹图可以发现，车辆运动轨迹越复杂，转向越多，大更新间隔带来的精度损失就越明显。因此，在实际应用中，选取合适的更新间隔才能达成精度与效率之间的平衡。
