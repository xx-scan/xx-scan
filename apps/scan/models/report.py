import uuid
from django.db import models

from .scan_cfg import ScanRecode, ScanScript


class ReportFormat(models.Model):
    scan_tool = models.ForeignKey(ScanScript, on_delete=models.CASCADE, related_name="scan_out_put_format")
    format_func = models.CharField(max_length=155, verbose_name="格式化函数", blank=True)


    class Meta:
        db_table = "report_formats"
        verbose_name = "报告格式化"


class ScanReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    scan_recode = models.ForeignKey(ScanRecode, on_delete=models.CASCADE, related_name="scan_output_report")
    report = models.TextField(verbose_name=u"格式化后的报告文本", default="")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "scan_reports"
        verbose_name = "扫描报告"


class Report2DbRun(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "report_import_runs"
        verbose_name = "执行报告导入"