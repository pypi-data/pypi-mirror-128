import os


def ai_init1(n):
    os.mkdir(n)
    os.mkdir(n+'/src')
    os.mkdir(n+'/datasets')
    os.mkdir(n+'/example')
    os.mkdir(n + '/doc')
    os.mkdir(n+'/service')
    os.mkdir(n + '/3rdparty')
    os.mkdir(n + '/models')
    with open(n+'/README.md','w') as f:
        f.write('''
## 环境依赖
 - 系统：ubuntu
 - 显卡：GeForce GTX 1080Ti
 - Driver Version：410.93
 - Anaconda：Anaconda3-5.0.0.1
 - Docker：Docker version  18.09.4
 - Nvidia-Docker：NVIDIA Docker  1.0.1

## 目录结构描述
```
├── README.md                   // help document
│
├── src                         // 可执行程序
│
├── datasets                    // 数据集
│
├── example                     // 示例代码和实例数据
│
├── doc                         // 文档集合
│
├── service                     // 部署信息
│
├── 3rdparty                    // 三方库集合
│
└── models                      // 数据集
```
        ''')

