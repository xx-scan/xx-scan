from django.http import JsonResponse, HttpResponse, StreamingHttpResponse


from ..utils.unix_commads import sshclient_execmd
def ssh_command(request):
    if request.method=="POST":
        # 远程连接服务器
        # curl -d "execmd=docker images -a" http://localhost:3322/waf/mg/ssh_cmd"
        # return HttpResponse(sshclient_execmd(execmd=request.POST["execmd"]).decode('unicode-escape'))
        return HttpResponse(sshclient_execmd(execmd=request.POST["execmd"]).decode('utf-8'))


from django.conf.urls import url
test_urlpatterns = [
    url(r'^ssh_cmd$', ssh_command, name="远程URL命令"),

]