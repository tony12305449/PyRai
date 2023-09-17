# Pyrai - Mirai python variant

這項Mirai工作是基於研究與學習用途，依照簡易功能所實現出來的

其中有幾項功能是需要設定的，在後續也會說明

在開始操作之前，首先需要先進行設定ip_config.ini程式檔，將RelayIP設定為本機端IP位置，Target端僅用來測試單一目標裝置用，如無則免設定

首先，我們實現的Mirai主要提供```Scanner.py```、```Loader.py```、```CNC.py``` 、```bin_server.py``` 和 ```relay.py```

而其他資料夾像是```ELF_file```、```device_side```則是感染裝置的原始碼以及檔案

```Scanner.py```內部中，主要提供生成IP以及掃瞄是否有開啟22、23 port，並且會用內建的帳號密碼清單組進行brute force，其中```main```的位置呼叫Scanner函數調用可以設定的args有兩個，Scanner(choose,ip)
如果choose==1時則會進行全域掃描將192.168.0.1~192.168.254.255都進行掃描並record
如果將choose設定為2時則需要帶入ip位置針對該ip位置進行掃描

```Loader.py```，可以將掃描器中獲得到的IP以及帳號密碼進行帶入，帶入後會依照SSH或是Telnet進行登入，並下達指令進行感染下載完成移植動作。
在```doSSHLogin(ip, port, user, pass_)```、```doTelnetLogin(ip, port, user, pass_)```兩個函數中都是帶入ip、port、username、password進行存取，如果port為22請使用doSSHLogin，若port 23則使用doTelnetLogin



