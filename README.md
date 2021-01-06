# 自动生成xray-core的配置文件

## 使用方法

### 必须设置的环境变量

```
SERVER_NAME: 你的域名
CRT_FILE: 该域名对应的证书文件
KEY_FILE: 该域名对应的证书密钥文件
```

### 可选环境变量

```
CLIENT_PORT: 客户端端口号，默认为'10800'
PORT_PREFIX: 服务端各协议端口号前缀，默认为'71'；除443端口外，还会占用7112,7123,7134,7145端口
OUT_FOLDER: 配置文件输出目录，默认为'./out'
EMAIL: 客户端邮箱，默认为'generator@example.com'
```

配置完环境变量后运行```python run.py```

## 其他

1. 参考 [Xray-examples](https://github.com/XTLS/Xray-examples)
   / [VLESS-TCP-XTLS-WHATEVER](https://github.com/XTLS/Xray-examples/tree/main/VLESS-TCP-XTLS-WHATEVER)
