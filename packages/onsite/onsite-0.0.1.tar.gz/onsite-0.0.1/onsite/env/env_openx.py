import numpy as np
import xml.dom.minidom
from shapely.ops import cascaded_union
from shapely.geometry import Polygon
from itertools import combinations

class EnvOpenx():
    """根据OpenScenario文件进行测试，目前仅根据轨迹数据进行回放测试

    """

    def __init__(self):
        self.car_length = 4.924
        self.car_width = 1.872
        self.l = 3  # 车辆轴距，单位：m
        self.dt = 0.04 # 每秒25帧
        self.metric = 'danger'
        self.vehicle_array = None #存储当前场景车辆信息
        self.vehicle_list = None
        self.max_t = 0 #纪录场景持续的时间

    def init(self, path=None):
        if not path:
            path = './test_scenario/follow1.xosc'
        else:
            assert(path.split('.')[-1] == "xosc")
        # 读取OpenScenario文件
        self.data = xml.dom.minidom.parse(path).documentElement
        # 记录每辆车的轨迹，存在dic里面
        self.traj = {}
        for act in self.data.getElementsByTagName('Act'):
            name = act.getAttribute('name')
            self.traj[name] = {}
            for point in act.getElementsByTagName('Vertex'):
                t = point.getAttribute('time')
                t = round(float(t), 2)
                if t > self.max_t:
                    self.max_t = t
                loc = point.getElementsByTagName('WorldPosition')[0]
                self.traj[name][t] = {}
                self.traj[name][t]['x'] = loc.getAttribute('x')
                self.traj[name][t]['y'] = loc.getAttribute('y')
                
        # 计时器归0, 测试结果归0
        self.t = round(0, 2)
        self.result = 0
        self.vehicle_array = np.zeros((1, len(self.traj.keys()), 6))
        self.vehicle_list = list(self.traj.keys())
        self.vehicle_list[0] = 'ego'

        # 将所有车辆设置到0时刻位置
        i = 0
        for vehi in self.traj.keys():
            if self.t in self.traj[vehi].keys():
                self.vehicle_array[:,i,0] = self.traj[vehi][self.t]['x']
                self.vehicle_array[:,i,1] = self.traj[vehi][self.t]['y']
                self.vehicle_array[:,i,2] = 0 # speed 没有数值
                self.vehicle_array[:,i,3] = 0 # 转向角 没有数值
            self.vehicle_array[:,i,4] = self.car_length
            self.vehicle_array[:,i,5] = self.car_width
            i += 1
        state = self.get_state()
        return state

    def update(self, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        ##############更新时间步
        # 前进一个时间步长
        self.t += self.dt 
        ###############更新本车信息
        a, rot = action
        # 首先根据旧速度更新本车位置
        # 更新X坐标
        self.vehicle_array[:, 0, 0] += self.vehicle_array[:, 0,
                                           2] * self.dt * np.cos(
                self.vehicle_array[:, 0, 3])  # *np.pi/180
        # 更新Y坐标
        self.vehicle_array[:, 0, 1] += self.vehicle_array[:, 0,
                                        2] * self.dt * np.sin(
            self.vehicle_array[:, 0, 3])  # *np.pi/180
        # 更新本车转向角
        self.vehicle_array[:, 0, 3] += self.vehicle_array[:, 0,
                                       2] / self.l * np.tan(rot) * self.dt
        # 更新本车速度
        self.vehicle_array[:, 0, 2] += a * self.dt
        self.vehicle_array[:, 0, 2] = np.clip(self.vehicle_array[:, 0, 2], 0,
                                              1e5)
        ##############更新背景车信息
        t = round(float(self.t), 2)
        i = 1
        for vehi in self.vehicle_list[1:]: #对于除本车以外的车辆，直接从字典中取数据
            if t in self.traj[vehi].keys():
                self.vehicle_array[:,i,0] = self.traj[vehi][t]['x']
                self.vehicle_array[:,i,1] = self.traj[vehi][t]['y']
                self.vehicle_array[:,i,2] = 0 # speed 暂时没有数值
                self.vehicle_array[:,i,3] = 0 # 转向角 暂时没有数值
            i += 1

        judge_value,done = self.judge()
        # 如果此次更新完，时间已走完，则终止测试
        if round(float(self.t), 2) >= self.max_t:
            done = 1
        return judge_value,done

    def judge(self):
        if self.metric in ['danger','danger_union','danger_v','dqn','minimum_adjusted_TTC']:   
            result = 0
            done = 0
            intersection = []
            poly_zip = [self.get_poly(param)[0] for param in self.vehicle_list if self.vehicle_array[0, self.vehicle_list.index(param), 0]>5]
            intersection = cascaded_union(
                [a.intersection(b) for a, b in combinations(poly_zip, 2)]
                ).area
            # print(self.vehicle_array)
            # print(intersection)
        if self.metric == "danger":
            if intersection > 0:
                result = 1
                done = 1

        return result,done

    def get_state(self):
        '''返回所有数据
        
        '''
        state = self.vehicle_array.copy()
        return state

    def step(self,action):
        reward, done = self.update(action)
        obeservation = self.get_state()
        return obeservation, reward, done, None

    def get_poly(self, name):
        """根据车辆名字获取对应的，符合shapely库要求的矩形。

        这是为了方便地使用shapely库判断场景中的车辆是否发生碰撞

        :param name:车辆的名字
        :return: 一列对应的shapely图形
        """
        ego = self.vehicle_array[:, self.vehicle_list.index(name), :].copy()
        alpha = np.arctan(ego[:, 5] / ego[:, 4])
        diagonal = np.sqrt(ego[:, 5] ** 2 + ego[:, 4] ** 2)
        poly_list = []
        x0 = ego[:, 0] + diagonal / 2 * np.cos(ego[:, 3] + alpha)
        y0 = ego[:, 1] + diagonal / 2 * np.sin(ego[:, 3] + alpha)
        x2 = ego[:, 0] - diagonal / 2 * np.cos(ego[:, 3] + alpha)
        y2 = ego[:, 1] - diagonal / 2 * np.sin(ego[:, 3] + alpha)
        x1 = ego[:, 0] + diagonal / 2 * np.cos(ego[:, 3] - alpha)
        y1 = ego[:, 1] + diagonal / 2 * np.sin(ego[:, 3] - alpha)
        x3 = ego[:, 0] - diagonal / 2 * np.cos(ego[:, 3] - alpha)
        y3 = ego[:, 1] - diagonal / 2 * np.sin(ego[:, 3] - alpha)
        for i in range(x0.shape[0]):
            poly_list += [Polygon(((x0[i], y0[i]), (x1[i], y1[i]),
                                   (x2[i], y2[i]), (x3[i], y3[i]),
                                   (x0[i], y0[i]))).convex_hull]
        return poly_list

