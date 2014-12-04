# Ping++ Python SDK


Ping++ Python SDK，基于 [Ping++ HTTP REST API 接口](https://pingplusplus.com/document/api/) 开发。


### 安装说明

> 依赖 [requests](https://github.com/kennethreitz/requests): HTTP for Humans，推荐！

```
python setup.py install
```


## 基本函数接口

### 设置api_key

```python

import pingpp

pingpp.api_key='api_key'
```

### 创建Charge对象

#### 使用类接口

```python
ch = pingpp.Charge.objects.create(order_no="123ffffgdaf34", amount=10,
                                  app={'id': 'app_1Kenv5f5GiDCKWLW'},
                                  channel='upmp',
                                  currency='cny',
                                  client_ip='127.0.0.1',
                                  subject='iphone',
                                  body='hello')
print ch.id, ch
```

#### 创建对象

```python
ch = pingpp.Charge(order_no="123ffffgdaf34", amount=10,
                   app={'id': 'app_1Kenv5f5GiDCKWLW'},
                   channel='upmp',
                   currency='cny',
                   client_ip='127.0.0.1',
                   subject='iphone',
                   body='hello')
ch.save()
print ch.id, ch
```
创建错误，抛出相应异常。

### 查找Charge对象

#### 使用get接口

```python
ch = pingpp.Charge.objects.get(charge_id='charge_id')
print ch.id, ch
```

查找成功，返回Charge对象; 失败则抛出相应异常。


### 查询Charge对象列表

```python
chs = pingpp.Charge.objects.filter(limit=5)
print len(chs)
for ch in chs:
    print ch.id, ch
```

查询成功，返回 charge列表; 失败则抛出相应异常。

### 创建Refund对象

#### 使用类接口

```python
re = pingpp.Refund.objects.create(charge_id=ch.id,
                                  amount=100,
                                  description="hello")
print re.id, re
```

#### 创建对象

```python
re = pingpp.Refund(charge_id=ch.id,
                   amount=100,
                   description="hello")
re.save()
print re.id, re
```
创建错误，抛出相应异常。

### 查找Refund对象

#### 使用get接口

```python
re = pingpp.Refund.objects.get(charge_id=ch.id, refund_id=re.id)
print re.id, re
```

查找成功，返回Refund对象; 失败则抛出相应异常。


### 查询Refund对象列表

```python
res = pingpp.Refund.objects.filter(charge_id=ch.id, limit=5)
print len(res)
for re in res:
    print re.id, re
```

查询成功，返回 Refund列表; 失败则抛出相应异常。
