# coding:utf-8

## 审计员
def test_is_auditor(request):
    from ..models import UserProfile
    try:
        _identity = UserProfile.objects.filter(user=request.user)[0].identity
        if _identity:
            if _identity in ["SuperManager", "DbUser"]:
                return True
    except:
        pass
    if request.user.is_superuser:
        return True

# 管理员
def test_is_admin(request):
    from ..models import UserProfile
    try:
        _identity = UserProfile.objects.filter(user=request.user)[0].identity
        if _identity:
            if _identity in ["SuperManager"]:
                return True
    except:
        pass
    if request.user.is_superuser:
        return True

# 安全审计员
def test_is_securitier(request):
    from ..models import UserProfile
    try:
        _identity = UserProfile.objects.filter(user=request.user)[0].identity
        if _identity:
            if _identity in ["SuperManager", "NetworkManager"]:
                return True
    except:
        pass
    if request.user.is_superuser:
        return True