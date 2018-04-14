from .t_logic import TLogic


def render(template_, **kwargs):
    """
    usage:
        Response.render({
            'user': {
                'id': Holder('user.id', default='Hello world'),
                'nickname': Holder('user.nickname')
            }
        }, user=dict(id=1, nickname='test'))

    See more in t_logic.py

    :param template_:
    :param kwargs:
    :return:
    """
    output = {}
    for key, item in template_.items():
        if isinstance(item, dict):
            output[key] = render(item, **kwargs)
        elif isinstance(item, TLogic):
            output[key] = item.parse(render_=render, **kwargs)
        else:
            output[key] = item
    return output
