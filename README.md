# api-server-flask

基于Flask框架上集成与封装了一些便捷功能，用于快速编写一个API服务。

## 实现功能

- 请求表单参数校验
- 返回数据模版化
- 自动根据上述配置动态生成文档
- 方便配置Authenticate功能

## 使用示例

```python
from kernel.controller import BaseController

controller = BaseController(
    name='name', import_name=__name__, prefix='/prefix') 


@controller.post('/post-method')
@controller.login_required()
@controller.add_apidoc()
def post_method():
    pass
```

### 请求参数校验

```python
from kernel.controller.webargs import fields

post_form = {
    'arg': fields.Str(required=True)
}
    
@controller.get('/use-args')
@controller.use_args(post_form, code=403)
def use_args(parsed):
    # 校验后的参数会以名为parsed的字典传入
    pass
```

### 结果模版返回

```python
from kernel.response import Response, THolder
    
response = {
    'res': THolder('res'),
    'user': {
        'id': THolder('user.id'),
        'name': THolder('user.name')
    }
}

@controller.get('/render-template')
@controller.add_apidoc(response=response)
def render_template():
    user = {'id': 1, 'name': 'user'}
    return Response.render(response, res='test', user=user)
```

更详细文档之后进行补充  
详情可参考app目录下示例
