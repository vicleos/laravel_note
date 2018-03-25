
## 聊聊base62与tinyURL

### 【 序 】
base64大家肯定是很熟悉了，那base62是什么东东，它常被用来做短url的映射。

### 【 ascii编码的62个字母数字 】
```java
Value Encoding  Value Encoding  Value Encoding  Value Encoding
  0 a            17 r            34 I            51 Z
  1 b            18 s            35 J            52 0
  2 c            19 t            36 K            53 1
  3 d            20 u            37 L            54 2
  4 e            21 v            38 M            55 3
  5 f            22 w            39 N            56 4
  6 g            23 x            40 O            57 5
  7 h            24 y            41 P            58 6
  8 i            25 z            42 Q            59 7
  9 j            26 A            43 R            60 8
 10 k            27 B            44 S            61 9
 11 l            28 C            45 T
 12 m            29 D            46 U
 13 n            30 E            47 V
 14 o            31 F            48 W
 15 p            32 G            49 X
 16 q            33 H            50 Y
```
26个小写字母+26个大写字母+10个数字=62
```java
    public static final String BASE_62_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    public static final int BASE = BASE_62_CHAR.length();
```

### 【 62进制与十进制的映射 】
#### 62进制转10进制
还记得二进制转十进制的算法么，从右到左用二进制的每个数去乘以2的相应次方，次方要从0开始。62进制转10进制也类似，从右往左每个数*62的N次方，N从0开始。
```java
    public static long toBase10(String str) {
        //从右边开始
        return toBase10(new StringBuilder(str).reverse().toString().toCharArray());
    }

    private static long toBase10(char[] chars) {
        long n = 0;
        int pow = 0;
        for(char item: chars){
            n += toBase10(BASE_62_CHAR.indexOf(item),pow);
            pow++;
        }
        return n;
    }

    private static long toBase10(int n, int pow) {
        return n * (long) Math.pow(BASE, pow);
    }
```
#### 十进制转62进制
还记得十进制转二进制的算法么，除二取余，然后倒序排列，高位补零。转62进制也类似，不断除以62取余数，然后倒序。
```java
    public static String fromBase10(long i) {
        StringBuilder sb = new StringBuilder("");
        if (i == 0) {
            return "a";
        }
        while (i > 0) {
            i = fromBase10(i, sb);
        }
        return sb.reverse().toString();
    }

    private static long fromBase10(long i, final StringBuilder sb) {
        int rem = (int)(i % BASE);
        sb.append(BASE_62_CHAR.charAt(rem));
        return i / BASE;
    }
```
#### 短url的转换
主要思路，维护一个全局自增的id，每来一个长url，将其与一个自增id绑定，然后利用base62将该自增id转换为base62字符串，即完成转换。
```java
public class Base62UrlShorter {

    private long autoIncrId = 10000;

    Map<Long, String> longUrlIdMap = new HashMap<Long, String>();

    public long incr(){
        return autoIncrId ++ ;
    }

    public String shorten(String longUrl){
        long id = incr();
        //add to mapping
        longUrlIdMap.put(id,longUrl);
        return Base62.fromBase10(id);
    }

    public String lookup(String shortUrl){
        long id = Base62.toBase10(shortUrl);
        return longUrlIdMap.get(id);
    }
}
```
测试
```java
    @Test
    public void testLongUrl2Short(){
        Base62UrlShorter shorter= new Base62UrlShorter();
        String longUrl = "https://movie.douban.com/subject/26363254/";
        String shortUrl = shorter.shorten(longUrl);
        System.out.println("short url:"+shortUrl);
        System.out.println(shorter.lookup(shortUrl));
    }
```


- 参考：https://segmentfault.com/a/1190000010516708
