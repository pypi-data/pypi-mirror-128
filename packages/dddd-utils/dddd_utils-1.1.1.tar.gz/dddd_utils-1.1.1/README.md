# 带带弟弟小工具

1.功能

- 爬虫基类
- 爬虫基类2（selenium）
- mail
- ftp 下载；删除
- retry 重试器，只支持在类中使用
- mysql 操作类
- get_ffdm_api 斐斐打码
   ```python
   # 示例
   from dddd_utils import get_ffdm_api
   config = {
     "pd_id": "",
     "pd_key": "",
     "app_id": "",
     "app_key": ""
   }
   api = get_ffdm_api(**config)
   pred_type = "20400"  # 
   code_image_path = ""
   res = api.PredictFromFile(pred_type, code_image_path)  # 返回详细识别结果
   print(res.pred_rsp.value)
   ```

---

2. 使用
    ```shell
    pip install -i https://pypi.org/simple/ dddd-utils
    ```

3. 打包
    ```shell
    python3 -m build

    python3 -m twine upload --repository testpypi dist/*
    
    python3 -m twine upload --repository pypi dist/*
    ```
