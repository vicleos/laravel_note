#### 错误信息

```
==> Downloading https://storage.googleapis.com/downloads.webmproject.org/release
##O#- #
curl: (35) Server aborted the SSL handshake
Error: Failed to download resource "webp"
Download failed: https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.0.tar.gz
```

原因是googleapis被墙了

解决方法：替换下载地址
```
brew edit webp
```
将下载地址 和 MD5 替换

```
    url "http://downloads.webmproject.org/releases/webp/libwebp-1.0.0.tar.gz"
    sha256 "84259c4388f18637af3c5a6361536d754a5394492f91be1abc2e981d4983225b"
```

- 参考：
https://www.jianshu.com/p/a9271e522edc
