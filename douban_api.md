## 登录接口

使用 douban.fm 并不需要使用豆瓣的 OAuth 认证，只需要简单地把用户名密码 POST 过去，并保存 Token 和 Expire 即可。

* URL: `http://www.douban.com/j/app/login`

* Method: `POST`

* Arguments: 
    
    * `app_name`: `radio_desktop_win`
    
    * `version`: `100`
    
    * `email`: `用户帐号`
    
    * `password`: `明文密码`

* Header: `Content-Type: application/x-www-form-urlencoded`

* Response ( `application/json` )

登录成功（`r`的值为`0`）

```json
{
    "user_id": "<user_id>",
    "err": "ok",
    "token": "<token_string>",
    "expire": "<expire_time_in_millisecond>",
    "r": 0,
    "user_name": "钟小腾",
    "email": "<user_account>"
}
```

登录失败（`r`为`1`，`err`会给出错误原因）

```json
{
    "r": 1,
    "err": "wrong_password"
}
```

在获得`user_id`，`token`和`expire`后，保存起来，在使用获取歌曲列表、红心等API时，把它们放到请求参数中即可。

*若使用 http://douban.fm 这个页面所使用的接口，则需要先获取Cookies，并在每次请求都要发Cookies，相对比较麻烦*

## 获取频道列表

这个接口获取的频道列表是一个比较固定的列表，并非douban.fm网页版上那么多样的列表。网页版的频道列表是直接服务器生成在HTML里面的，无法直接获得（可使用爬虫），但它的`channel_id`可以用，如有兴趣可把这些`channel_id`收集起来。

* URL: `http://www.douban.com/j/app/radio/channels`

* Method: `GET`

* Arguments: None

* Response ( `application/json` ):

```json
{
    "channels": [
        {
            "name": "私人兆赫",
            "seq_id": 0,
            "abbr_en": "My",
            "channel_id": 0,
            "name_en": "Personal Radio"
        },
        {
            "name": "华语",
            "seq_id": 1,
            "abbr_en": "CH",
            "channel_id": 1,
            "name_en": "Chinese"
        },
        {
            "name": "欧美",
            "seq_id": 2,
            "abbr_en": "EN",
            "channel_id": 2,
            "name_en": "Euro-American"
        },
        ...
}
```

如上可看出，有频道名，有`channel_id`，这个id用于请求相应的歌曲列表。`seq_id`只是一个简单的列表排序`index`，可忽略

## 歌曲列表

歌曲列表的获取最为复杂，其参数也比较多

* URL: `http://www.douban.com/j/app/radio/people`

* Method: `GET`

* Arguments:

<table width="100%">
   <tr>
      <td>参数名</td>
      <td>是否必选</td>
      <td>参数类型</td>
      <td>值</td>
      <td>备注</td>
   </tr>
   <tr>
      <td>app_name</td>
      <td>必选</td>
      <td>string</td>
      <td>radio_desktop_win</td>
      <td>固定</td>
   </tr>
   <tr>
      <td>version</td>
      <td>必选</td>
      <td>int</td>
      <td>100</td>
      <td>固定</td>
   </tr>
   <tr>
      <td>user_id</td>
      <td>非必选</td>
      <td>string</td>
      <td>user_id</td>
      <td>若已登录，则填入</td>
   </tr>
   <tr>
      <td>expire</td>
      <td>非必选</td>
      <td>int</td>
      <td>expire</td>
      <td>若已登录，则填入</td>
   </tr>
   <tr>
      <td>token</td>
      <td>非必选</td>
      <td>string</td>
      <td>token</td>
      <td>若已登录，则填入</td>
   </tr>
   <tr>
      <td>sid</td>
      <td>非必选</td>
      <td>int</td>
      <td>song id</td>
      <td>在需要针对单曲操作时需要</td>
   </tr>
   <tr>
      <td>h</td>
      <td>非必选</td>
      <td>string</td>
      <td>最近播放列表</td>
      <td>单次报告曲目播放状态，其格式是 <code>|sid:报告类型|sid:报告类型</code> </td>
   </tr>
   <tr>
      <td>channel</td>
      <td>非必选</td>
      <td>int</td>
      <td>频道id</td>
      <td>获取频道时取得的channel_id</td>
   </tr>
   <tr>
      <td>type</td>
      <td>必选</td>
      <td>string</td>
      <td>报告类型</td>
      <td>需要调用的接口类型，也是使用下表的报告类型</td>
   </tr>
</table>

其中<b>报告类型</b>是以下的一种类型，都是一个字母。

<table width="100%">
   <tr>
      <td>类型</td>
      <td>需要参数</td>
      <td>含义</td>
      <td>报告长度</td>
   </tr>
   <tr>
      <td>b</td>
      <td>sid</td>
      <td>bye，不再播放</td>
      <td>短报告</td>
   </tr>
   <tr>
      <td>e</td>
      <td>sid</td>
      <td>end，当前歌曲播放完毕，但是歌曲队列中还有歌曲</td>
      <td>短报告</td>
   </tr>
   <tr>
      <td>n</td>
      <td></td>
      <td>new，没有歌曲播放，歌曲队列也没有任何歌曲，需要返回新播放列表</td>
      <td>长报告</td>
   </tr>
   <tr>
      <td>p</td>
      <td></td>
      <td>playing，歌曲正在播放，队列中还有歌曲，需要返回新的播放列表</td>
      <td>长报告</td>
   </tr>
   <tr>
      <td>s</td>
      <td>sid</td>
      <td>skip，歌曲正在播放，队列中还有歌曲，适用于用户点击下一首</td>
      <td>短报告</td>
   </tr>
   <tr>
      <td>r</td>
      <td>sid</td>
      <td>rate，歌曲正在播放，标记喜欢当前歌曲</td>
      <td>短报告</td>
   </tr>
   <tr>
      <td>u</td>
      <td>sid</td>
      <td>unrate，歌曲正在播放，标记取消喜欢当前歌曲</td>
      <td>短报告</td>
   </tr>
</table>

* Response ( `application/json` ):

所有的这些都会返回一个json字符串，其中都会包括歌曲列表（上面得到的歌曲URL，只会在一定时间内有效，过期之后就不能再访问了，因此猜测每次访问都返回一些歌曲就是想更新一下后面的曲库，因为当前这首不能播了，很可能后面的也不能播）。

`r`若为`1`即出错，`err`里面会写上出错原因，而`r`为`0`即调用成功。

其中的歌曲列表格式是

```json
{
    "r": 0,
    "version_max": 100,
    "song": [
        {
            "album": "/subject/5952615/",
            "picture": "http://img3.douban.com/mpic/s4616653.jpg",
            "ssid": "e1b2",
            "artist": "Bruno Mars / B.o.B",
            "url": "http://mr3.douban.com/201308250247/4a3de2e8016b5d659821ec76e6a2f35d/view/song/small/p1562725.mp3",
            "company": "EMI",
            "title": "Nothin' On You",
            "rating_avg": 4.04017,
            "length": 267,
            "subtype": "",
            "public_time": "2011",
            "sid": "1562725",
            "aid": "5952615",
            "sha256": "2422b6fa22611a7858060fd9c238e679626b3173bb0d161258b4175d69f17473",
            "kbps": "64",
            "albumtitle": "2011 Grammy Nominees",
            "like": 1
        },
        ...
    }
}
```

参数都可以直接从名字看出其意义
* `album` 专辑跳转地址
* `picture` 专辑图片地址
* `ssid` 未知
* `artist` 艺术家
* `url` 歌曲的URL
* `company` 唱片公司
* `title` 歌曲名
* `rating_avg` 平均分数
* `length` 长度
* `subtype` 子类型（有些广告的字类型会是T）
* `public_time` 出版年份
* `sid` 歌曲id
* `aid` 专辑id
* `kbps` 码率
* `albumtitle` 专辑名
* `like` 是否已喜欢，0为false，1为true