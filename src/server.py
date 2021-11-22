from socketserver import BaseRequestHandler, ThreadingTCPServer
import os
import configparser

from functools import lru_cache  # 引入缓存 Least Recently Used，最近最少使用

from time import ctime


# 把传进去的字符串，转换成字典，将字典的结构为    字符：字符个数
def Createdic(a):
    # 去除空格
    a = a.replace(" ", "")
    # 创建一个空字典
    dic = {}
    for i in a:
        # 统计
        dic[i] = a.count(i)
    return dic


# sunday算法比kmp算法要快了不少
@lru_cache(None)  # 添加缓存
def sunday(S, T):
    # return S.find(T)

    ls, lt = len(S), len(T)
    d = 0
    # 记录下标
    while d <= ls - lt and T in S:
        # 保证T有成为S子串的前提下并且循环
        if S[d:d + lt] == T:
            # 如果符合，返回下标
            return d
        else:
            p = T.rfind(S[d + lt])
            # 返回字符串最后一次出现的位置，如果没有匹配项则返回-1
            if p == -1:
                # 没有匹配，跳子串长度个距离
                d += lt + 1
            else:
                # 有匹配，对齐查看是否全部匹配
                d += lt - p
    return -1


@lru_cache(None)  # 添加缓存
def score_en(mon, son):
    mon = mon.lower()
    son = son.lower()

    if sunday(mon, son) != -1:
        sum_score = 100

        return sum_score
    else:
        dic = {}
        list = mon.split(" ")
        # print(list)
        for i in list:
            dic[i] = list.count(i)
            # print(dic)

        list = son.split(" ")
        dic2 = {}  # 被匹配的数组。
        for i in list:
            i = i.lower()
            dic2[i] = list.count(i)
            # print(dic)
        sum_score = 0

        for key in dic2:
            # print(dic2[key])
            # print(key in dic.keys())
            # 判断key是不是在第一个数组里面
            if key in dic.keys():

                if dic[key] == dic2[key]:
                    # dic3[key] = 1;
                    sum_score += 1

                elif dic2[key] >= 1 & dic2[key] <= 5:

                    sum_score += 0.15 * dic2[key]
                else:
                    pass
        return sum_score


@lru_cache(None)  # 添加缓存
def score(mom_string, son_string):
    # 在执行的时候先用sunday算法匹配，如果匹配成功会返回一个索引值，匹配不成功的话就就返回-1，进入模糊处理
    sum_score = 0
    if sunday(mom_string, son_string) != -1:
        sum_score = 100  # 匹配成功的话，就直接把sum_score,直接搞到最大。
        return sum_score

    dic = Createdic(mom_string)
    dic2 = Createdic(son_string)

    for key in dic2:

        # 判断key是不是在第一个mom_string字符串里面
        if key in dic.keys():
            # 如果里面的字典中对应的key  value值相同，那么就先把他的总分加 1
            if dic[key] == dic2[key]:
                # dic3[key] = 1;
                sum_score += 1

            # 
            elif dic2[key] >= 1 & dic2[key] <= 5:
                # dic3[key] = 0.5;
                sum_score += 0.15 * dic2[key]
        else:
            # dic3[key]=0
            pass
    # print(dic3)
    return sum_score


# 加载配置文件
def load_path():
    # 得到父目录
    proDir = os.path.split(os.path.realpath(__file__))[0]
    pproDir = proDir.split("\\")[0] + "\\" + proDir.split("\\")[1]

    configPath = os.path.join(pproDir, "conf.ini")
    print(configPath)
    paths = configparser.ConfigParser()
    # 注意这个 read自能读绝对路径，不能读相对路径
    paths.read(configPath, encoding='utf-8')
    return paths


BUF_SIZE = 1024
STATE = '1'  # 默认的数据状态




class Handler(BaseRequestHandler):

    def handle(self):
        global request, response, STATE
        address, pid = self.client_address
        print(address, pid, " has been connected!")
        try:
            while True:

                data = self.request.recv(BUF_SIZE)
                data = data.decode('utf-8')  # 将字节码解码成字符码
                print(' received-->%s\n%s' % (ctime(), data))  # 输出收到的信息

                data = data.split("\n")[0]  # 去除回车字符
                # 判断发出的数据是不是为null的
                if len(data) < 1:
                    data = "您当前发送的数据为空哦，请您重新输入哟~"
                    self.request.sendall(data.encode('utf-8'))  # 将信息发送给客户端
                    print("返回的数据是：", data)
                    continue

                # 输入发送的信息
                if data == '1':
                    print("你已进入闲聊模式")
                    request = paths.get("chat", "request")
                    response = paths.get("chat", "response")
                    data = "你已进入闲聊模式"
                    STATE = '1'  # 修改状态
                    self.request.sendall(data.encode('utf-8'))  # 将信息发送给客户端
                    continue

                if data == '2':
                    request = paths.get("poems", "request")
                    response = paths.get("poems", "response")
                    data = "你已进入古诗模式"
                    STATE = '2'  # 修改状态
                    self.request.sendall(data.encode('utf-8'))  # 将信息发送给客户端
                    continue

                if data == '3':
                    request = paths.get("english", "request")
                    response = paths.get("english", "response")
                    data = "你以进入英文模式"
                    STATE = '3'  # 修改状态
                    self.request.sendall(data.encode('utf-8'))  # 将信息发送给客户端
                    continue

                say_word = data

                f = open(request, 'r', encoding='utf-8')
                f_reply = open(response, 'r', encoding='utf-8')
                lines = f.readlines()
                lines_reply = f_reply.readlines()
                c_score = []

                if STATE == '1' or STATE == '2':
                    for line in lines:
                        c_score.append(score(line, say_word))

                if STATE == '3':
                    for line in lines:
                        c_score.append(score_en(line, say_word))

                if STATE == '2':
                    data = lines[c_score.index(max(c_score))].split("\n")[0] + "," + lines_reply[c_score.index(max(c_score))]
                else:
                    data = lines_reply[c_score.index(max(c_score))]


                self.request.sendall(data.encode('utf-8'))  # 将信息发送给客户端
        except BaseException:
            print(address, pid, " has been exit!")


if __name__ == '__main__':
    paths = load_path()
    response = paths.get("chat", "request")
    request = paths.get("chat", "response")

    HOST = '127.0.0.1'  # 配置主机名
    PORT = 8998  # 配置端口号
    ADDR = (HOST, PORT)
    server = ThreadingTCPServer(ADDR, Handler)  # 参数为监听地址和已建立连接的处理类
    print('wait connect....')
    server.serve_forever()  # 监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
    print(server)
