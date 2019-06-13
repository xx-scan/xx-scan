def put_log(type="脚本日志", desc="", extra=""):
    from services.models import PlatOptHistory
    PlatOptHistory.objects.create(
        type=type,
        desc=desc,
        extra=extra
    )
    return

    try:
        from services.models import PlatOptHistory
        PlatOptHistory.objects.create(
            type=type,
            desc=desc,
            extra=extra
        )
    except:
        import logging
        logging.error("==========="+desc+"=============")