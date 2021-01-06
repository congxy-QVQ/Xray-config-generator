import string
import random
import json
import os
from uuid import uuid4


class XrayConfig:
    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
    SERVER_FILE = 'config_server.json'
    CLIENT_VLTX_FILE = 'vless_tcp_xtls.json'
    CLIENT_VLTT_FILE = 'vless_tcp_tls.json'
    CLIENT_VLWT_FILE = 'vless_ws_tls.json'
    CLIENT_VMTT_FILE = 'vmess_tcp_tls.json'
    CLIENT_VMWT_FILE = 'vmess_ws_tls.json'
    CLIENT_TJTT_FILE = 'trojan_tcp_tls.json'

    def __init__(self):
        def read(path):
            with open(path, 'r') as f:
                d = json.load(f)
                return json.dumps(d)

        self.config_server = read(os.path.join(XrayConfig.BASE_PATH, XrayConfig.SERVER_FILE))
        client = os.path.join(XrayConfig.BASE_PATH, 'config_client')
        self.config_client_vltx = read(os.path.join(client, XrayConfig.CLIENT_VLTX_FILE))
        self.config_client_vltt = read(os.path.join(client, XrayConfig.CLIENT_VLTT_FILE))
        self.config_client_vlwt = read(os.path.join(client, XrayConfig.CLIENT_VLWT_FILE))
        self.config_client_vmtt = read(os.path.join(client, XrayConfig.CLIENT_VMTT_FILE))
        self.config_client_vmwt = read(os.path.join(client, XrayConfig.CLIENT_VMWT_FILE))
        self.config_client_tjtt = read(os.path.join(client, XrayConfig.CLIENT_TJTT_FILE))

    def replace(self, old: str, replace: str):
        self.config_server = self.config_server.replace(old, replace)
        self.config_client_vltx = self.config_client_vltx.replace(old, replace)
        self.config_client_vltt = self.config_client_vltt.replace(old, replace)
        self.config_client_vlwt = self.config_client_vlwt.replace(old, replace)
        self.config_client_vmtt = self.config_client_vmtt.replace(old, replace)
        self.config_client_vmwt = self.config_client_vmwt.replace(old, replace)
        self.config_client_tjtt = self.config_client_tjtt.replace(old, replace)

    def dump(self, folder='./'):
        os.makedirs(folder, exist_ok=True)

        def json_dump(s, f):
            d = json.loads(s)
            with open(os.path.join(folder, f), 'w') as file:
                json.dump(d, file, ensure_ascii=False, sort_keys=True, indent=2)

        json_dump(self.config_server, XrayConfig.SERVER_FILE)
        json_dump(self.config_client_vltx, XrayConfig.CLIENT_VLTX_FILE)
        json_dump(self.config_client_vltt, XrayConfig.CLIENT_VLTT_FILE)
        json_dump(self.config_client_vlwt, XrayConfig.CLIENT_VLWT_FILE)
        json_dump(self.config_client_vmtt, XrayConfig.CLIENT_VMTT_FILE)
        json_dump(self.config_client_vmwt, XrayConfig.CLIENT_VMWT_FILE)
        json_dump(self.config_client_tjtt, XrayConfig.CLIENT_TJTT_FILE)


class Tools:
    RANDOM_SEQ = string.digits + string.ascii_letters + string.digits
    USER = 'generator@example.com'

    @staticmethod
    def random():
        return ''.join([random.choice(Tools.RANDOM_SEQ) for i in range(16)])

    @staticmethod
    def uuid():
        return str(uuid4())


def generator(crt_file, key_file, server_name, user, port_prefix, client_port):
    config = XrayConfig()
    uuid = Tools.uuid()
    config.replace('UUID', uuid)
    config.replace('example.com', server_name)
    config.replace('TROJAN_PASSWORD', Tools.random())
    config.replace('VMESSWS', Tools.random())
    config.replace('WEBSOCKET', Tools.random())
    config.replace('VMESSTCP', Tools.random())
    config.replace('10800', client_port)
    config.replace('EMAIL', user)
    config.replace('CRT_FILE', crt_file)
    config.replace('KEY_FILE', key_file)
    config.replace('7112', port_prefix + '12')
    config.replace('7123', port_prefix + '23')
    config.replace('7134', port_prefix + '34')
    config.replace('7145', port_prefix + '45')
    return config


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
    env_dict = os.environ
    crt_file = env_dict.get('CRT_FILE')
    key_file = env_dict.get('KEY_FILE')
    server_name = env_dict.get('SERVER_NAME')
    client_port = env_dict.get('CLIENT_PORT', '10800')
    port_prefix = env_dict.get('PORT_PREFIX', '71')
    out_folder = env_dict.get('OUT_FOLDER', out)
    email = env_dict.get('EMAIL', Tools.USER)
    if not crt_file or not key_file or not server_name:
        print('环境变量中必须含有域名(SERVER_NAME)及对应的证书(CRT_FILE)和私钥(KEY_FILE)！')
        exit(1)
    config = generator(crt_file, key_file, server_name, email, port_prefix, client_port)
    config.dump(out_folder)
    print(f'成功！配置文件在目录`{out_folder}`下，客户端配置文件请根据情况选一即可。')
