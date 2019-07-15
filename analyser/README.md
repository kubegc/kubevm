
## grep用法

```
$grep -5 ‘parttern’ inputfile //打印匹配行的前后5行
$grep -C 5 ‘parttern’ inputfile //打印匹配行的前后5行
$grep -A 5 ‘parttern’ inputfile //打印匹配行的后5行
$grep -B 5 ‘parttern’ inputfile //打印匹配行的前5行
```

## awk用法

```
^\s+            匹配行首一个或多个空格
\s+$            匹配行末一个或多个空格
^\s+|\s+$    同时匹配行首或者行末的空格
```
