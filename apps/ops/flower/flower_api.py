from agent.api.devices.ips.settings import prefix, PREFIX_LJ, PREFIX_DL

# https://flower.readthedocs.io/en/latest/api.html

class ApiINfo(object):
    def __init__(self, url, method='post', name='', desc='', params='', example='', auth=True, response_eg='', data='', _type='c'):
        self.url = url
        self.method = method
        self.name = name
        self.desc = desc
        self.params = params
        self.example = example
        self.auth = auth
        self.response_eg = response_eg
        self.prefix = prefix
        self.data = data
        self._type = _type

    def todict(self):
        return dict(
            url=self.url,
            method=self.method,
            name=self.name,
            desc=self.desc,
            params=self.params,
            example=self.example,
            auth=self.auth,
            response_eg=self.response_eg,
            prefix=self.prefix,
            data=self.data,
            _type=self._type
        )

    def __str__(self):
        return str(self.todict())


IPS_API = [
    ApiINfo(method='post', url='/auth/sign', name='登陆', example='POST /auth/sign username=aq009 password=999999', auth=False, _type='login'),
    ApiINfo(method='post', url=PREFIX_LJ + '/auth/auth', name='鉴权', example='POST /auth/auth sessionid=<>'),
    ApiINfo(method='get',  url=PREFIX_LJ + '/admin/', name='获取所有用户', example='GET /admin'),

]