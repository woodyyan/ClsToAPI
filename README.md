Forward CLS logs to ES / Splunk
===

### 功能描述

自动把 `cls` 的日志转发到 `ES` 和 `Splunk`，函数的默认行为转发到 ES，如果 `SPLUNK_URL` 和 `SPLUNK_TOKEN` 在环境变量中同时被设置，会同时日志转发到 `Splunk`

解析时会自动把 `content` 的内容 反序列化并展开到根节点，方面下游的系统进行检索：  

CLS Sample input:

```json
{
    "records": [
        {
            "timestamp": 1653523171317573400,
            "content": "{\"SCF_Alias\":\"\",\"SCF_Duration\":\"0\",\"SCF_FunctionName\":\"log-test\",\"SCF_Level\":\"INFO\",\"SCF_LogTime\":\"1653523171317573463\",\"SCF_MemUsage\":\"0.00\",\"SCF_Message\":\"START RequestId: 1fd17775-fdaa-4eb9-b33a-3fa5fabb3865\",\"SCF_Namespace\":\"default\",\"SCF_Qualifier\":\"$LATEST\",\"SCF_RequestId\":\"1fd17775-fdaa-4eb9-b33a-3fa5fabb3865\",\"SCF_RetryNum\":\"0\",\"SCF_StartTime\":\"1653523171317\",\"SCF_StatusCode\":\"202\",\"SCF_Type\":\"Platform\"}"
        }
    ]
}
```

Sample output:

```json
[
    {
        "timestamp": 1653523171317573400,
        "SCF_Alias": "",
        "SCF_Duration": "0",
        "SCF_FunctionName": "log-test",
        "SCF_Level": "INFO",
        "SCF_LogTime": "1653523171317573463",
        "SCF_MemUsage": "0.00",
        "SCF_Message": "START RequestId: 1fd17775-fdaa-4eb9-b33a-3fa5fabb3865",
        "SCF_Namespace": "default",
        "SCF_Qualifier": "$LATEST",
        "SCF_RequestId": "1fd17775-fdaa-4eb9-b33a-3fa5fabb3865",
        "SCF_RetryNum": "0",
        "SCF_StartTime": "1653523171317",
        "SCF_StatusCode": "202",
        "SCF_Type": "Platform"
    }
```


### 函数配置

SCF 配置:

```bash
函数名称	ClsToES
函数类型	Event函数
运行环境	Python 3.6
内存	512MB
执行超时时间	30秒
```


环境变量:

```bash
API_Key=xxxxxx # ES Key
URL=https://sample_es_url.com # ES API地址
SPLUNK_INDEX=sample_index # Splunk Index
SPLUNK_SOURCETYPE=sample_sourcetype # Splunk SourceType
SPLUNK_TOKEN=yyyyyy # Splunk Http Collector Token
SPLUNK_URL=https://http-inputs-zzzzz.com/services/collector/raw # Splunk URL 地址
```

### Links

- [Set up http collector in Splunk](https://docs.splunk.com/Documentation/Splunk/8.2.6/Data/UsetheHTTPEventCollector)
- [ES index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html)