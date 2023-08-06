
**使用教程**
```python
import kancylog as log

log.debug("debug log")
log.info("info log")
log.warn("warn log")
log.error("error log")
log.success("success log")
log.log("good log", "GOOD")
```

1）文字效果
```text
2021-11-26 23:23:44.006274 DEBUG 112828 <mainthread> - [log_tests.py::3] : debug log
2021-11-26 23:23:44.006274  INFO 112828 <mainthread> - [log_tests.py::4] : info log
2021-11-26 23:23:44.006274  WARN 112828 <mainthread> - [log_tests.py::5] : warn log
2021-11-26 23:23:44.006274 ERROR 112828 <mainthread> - [log_tests.py::6] : error log
2021-11-26 23:23:44.006274    OK 112828 <mainthread> - [log_tests.py::7] : success log
2021-11-26 23:23:44.006274  GOOD 112828 <mainthread> - [log_tests.py::8] : success log
```

2）图片效果
![img.png](https://images.cnblogs.com/cnblogs_com/kancy/2069805/o_211126152754_img.png)
