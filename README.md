# EdgeOne (国内版) 源站防护 IP 列表
本仓库使用腾讯云 API 自动收集并公布其 EdgeOne CDN 回源 IP 列表，作为免费版 EdgeOne 套餐下线「源站安全」功能后的替代。

根据腾讯云文档的建议，基于 GitHub Actions 实现每 3 天更新一次。

## 使用前须知
 1. 本仓库用以获取回源 IP 的订阅套餐为本人自购。虽然目前并无证据，但是**存在不同套餐/不同用户使用不同的回源 IP 的可能性**。
 2. 本仓库说使用的 API 获取的是 EdgeOne **国内版**的 IP 段，**可能与国际版 IP 地址段不同**。由于本人没有国际版付费订阅 EdgeOne，因此无法提供国际版相关 IP。
 3. 不排除腾讯使用隐写技术获其他技术特征，追踪「将源站 IP 分享出来的用户」的可能性。

## 获取 IP 列表
为了使主分支干净、整洁，自动获取并更新的 IP 列表保存于 [deploy](https://github.com/baobao1270/edgeone-ips/tree/deploy) 分支中。

同时我们提供个不同情况下可能需要的文件，以便您根据实际情况选择。

| 文件          | 说明                                            | 下载链接 |
| ------------ | ----------------------------------------------- | ------ |
| edgeone      | 所有（包括当前和计划下次更新）的回源 IPv4 + IPv6 列表  | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/edgeone)      [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/edgeone)      |
| edgeone-ipv4 | 所有（包括当前和计划下次更新）的回源 IPv4 列表         | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/edgeone-ipv4) [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/edgeone-ipv4) |
| edgeone-ipv6 | 所有（包括当前和计划下次更新）的回源 IPv6 列表         | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/edgeone-ipv6) [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/edgeone-ipv6) |
| current      | 当前正在使用的回源 IPv4 + IPv6 列表                 | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/current)      [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/current)      |
| current-ipv4 | 当前正在使用的回源 IPv4 列表                        | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/current-ipv4) [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/current-ipv4) |
| current-ipv6 | 当前正在使用的回源 IPv4 列表                        | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/current-ipv6) [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/current-ipv6) |
| planned      | 计划下次更新的回源 IPv4 + IPv6 列表，一般为空        | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/planned)       [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/planned)      |
| planned-ipv4 | 计划下次更新的回源 IPv4 列表，一般为空               | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/planned-ipv4)  [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/planned-ipv4) |
| planned-ipv6 | 计划下次更新的回源 IPv6 列表，一般为空               | [查看](https://github.com/baobao1270/edgeone-ips/blob/deploy/planned-ipv6)  [直链](https://raw.githubusercontent.com/baobao1270/edgeone-ips/refs/heads/deploy/planned-ipv6) |

## 自托管
若您对此仓库公布的 IP 列表有安全疑虑，或依旧想使用自己的订阅套餐获取 IP 列表，您可以在自己的机器上或其他地方生成 IP 列表。

要自己生成 IP 列表，您需要以下依赖：
 - 腾讯云账号，以及任意付费版本的 EdgeOne 套餐，并已绑定域名
 - 在控制台开启「源站防护」
 - 一个 Secret ID/Secret Key API 密钥；强烈建议您使用「子用户」功能创建一个仅用于获取 EdgeOne 回源 IP 的专用子用户并遵循最小化全县原则。
 - 运行此仓库程序的环境：
     - GitHub Actions；或：
         - Python 3.12 或更高版本
         - PDM: https://github.com/pdm-project/pdm

### 创建子用户并获取相关环境变量

在腾讯云控制台进入[「访问管理」——「用户列表」](https://console.cloud.tencent.com/cam)，然后点击「**新建用户**」，选择「快速创建」。用户名根据您的需要填写，「**访问方式**」仅勾选「**编程访问**」，「用户权限」暂不选择。创建完成后，会显示 Secret ID/Secret Key，需要记录并妥善保管。

然后进入[「策略」](https://console.cloud.tencent.com/cam/policy)，点击「**新建自定义策略**」，选择「**按策略语法创建**」，使用如下策略语法：

```json
{
    "statement": [
        {
            "action": [
                "teo:DescribeOriginACL",
                "teo:DescribeMultiPathGatewayOriginACL"
            ],
            "effect": "allow",
            "resource": [
                "*"
            ]
        }
    ],
    "version": "2.0"
}
```

**完成后，请添加刚刚创建的用户到该策略。**

最后登陆 [腾讯云 EdgeOne 控制台](https://console.cloud.tencent.com/edgeone/zones)，确保您已经有一个绑定过域名的付费版本的 EdgeOne 套餐，并开启「源站防护」功能。查找 `zone-xxxxxx` 格式的 Zone ID 并记录。

### 使用 GitHub 运行此项目
不建议 Fork 此仓库，而是手动进行上传。首先创建一个新的 GitHub 仓库，并在「**Settings**」——「**Secrets and variables**」——「**Actions**」中添加「**Repository secrets**」。您需要添加下面三个密钥：

 - `TENCENTCLOUD_SECRET_ID`: 创建新用户后提示的 Secret ID
 - `TENCENTCLOUD_SECRET_KEY`: 创建新用户后提示的 Secret Key
 - `TENCENTCLOUD_EDGEONE_ZONE_ID`: EdgeOne 开启「源站防护」功能的 Zone ID（`zone-xxxxxx` 格式）

完成后，clone 本仓库：

```shell
git clone https://github.com/baobao1270/edgeone-ips
cd  edgeone-ips && rm -rf .git
```

然后根据 GitHub 的提示，将本仓库重新初始化 Git 并上传到您刚刚创建的仓库中。

最后进入「Actions」选项卡，点击侧边栏「Fetch EegeOne IP Update」，选择「Run Workflow」进行首次运行。后续会按每 3 天一次的计划运行。

### 本地运行
首先克隆本仓库：

```shell
git clone https://github.com/baobao1270/edgeone-ips
```

然后使用 [PDM](https://github.com/pdm-project/pdm) 安装依赖：
```shell
cd  edgeone-ips
pdm install
```

然后将之前腾讯云控制台上操作所记录的信息设置为环境变量：
```shell
export TENCENTCLOUD_SECRET_ID=AK.....
export TENCENTCLOUD_SECRET_KEY=......
export TENCENTCLOUD_EDGEONE_ZONE_ID=zone-xxxxxx
```

至此即可直接运行：
```shell
pdm run run.py
```

## 许可
Python 代码以 MIT 协议许可。IP 列表本身不具有可获著作权的性质，个人认为可以等效于 CC-0。
