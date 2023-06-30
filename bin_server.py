import os
import http.server
import socketserver
import json
from libs import truecolors

__webp_ = "31338"           # bin server port
__file__ = "./ELF_file/"      # bin server port
Host_IP = ""


def read_config_ip():
    filename = 'ip_config.ini'
    with open(filename, 'r') as file:
        json_data = json.load(file)
    RelayIP = json_data['RelayIP']
    targetIP = json_data['targetIP']
    return RelayIP, targetIP


def ServeHTTP():
    web_dir = os.path.join(os.path.dirname(__file__),'bin')    # 到bin資料夾下面抓出可執行檔
    os.chdir(web_dir)                                           # 切換當前路徑到新路徑上
    Handler = http.server.SimpleHTTPRequestHandler              # 提供HTTP請求服務
    httpd = socketserver.TCPServer((Host_IP, int(__webp_)), Handler)  # 掛載TCP服務
    truecolors.print_info("Webserver started at:"+Host_IP +":"+ __webp_)  #顯示服務運行在-IP-PORT
    httpd.serve_forever()


if __name__ == '__main__':
    Host_IP, targerIP = read_config_ip()
    ServeHTTP()