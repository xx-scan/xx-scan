# from django.contrib import admin
#
# # Register your models here.
#
# from website.settings import SITE_TITLE
# admin.site.site_header = SITE_TITLE
# admin.site.site_title = SITE_TITLE
#
#
# from .models import SelfOrderRule, SrciptRunRecode, \
#     ErrorCodeTemplate, UrlRuleManage, RuleFilesManage
#
# class SelfOrderRuleAdmin(admin.ModelAdmin):
#     list_display = ('rule_id', 'is_active', 'opreate_time', 'msg', 'type', 'gaim_str', 'stat_code')
#     search_fields = ('msg',)
#     list_filter = ('type', 'is_active', 'opreate_time')
#     list_per_page = 20
#
#     def get_ordering(self, request):
#         return ['is_active', 'opreate_time']
#
#     def get_search_results(self, request, queryset, search_term):
#         queryset, use_distinct = super().get_search_results(request, queryset, search_term)
#         try:
#             search_term_as_int = int(search_term)
#         except ValueError:
#             pass
#         else:
#             queryset |= self.model.objects.filter(age=search_term_as_int)
#         return queryset, use_distinct
#
#     actions = ['make_disactive', ]
#
#     def make_disactive(self, request, queryset):
#         queryset.update(is_active=False)
#     make_disactive.short_description = "批量失效"
#
# class UrlRuleManageAdmin(admin.ModelAdmin):
#     list_display = ('rule_id', 'request_params', 'type', 'request_partern', 'rule_except')
#     search_fields = ('type', )
#
# class RuleFilesManageAdmin(admin.ModelAdmin):
#     list_display = ('uniq_str', 'active_path', 'down_save_path', 'get_conf_url', 'failed_run_url')
#
# class WafRuleAdmin(admin.ModelAdmin):
#     list_display = ('rule_id', 'rule_msg_cn', 'rule_line', 'rule_categary', 'rule_file')
#
# admin.site.register(SelfOrderRule, SelfOrderRuleAdmin)
# # admin.site.register(WafRule, WafRuleAdmin)
# admin.site.register(SrciptRunRecode)
# admin.site.register(ErrorCodeTemplate)
# admin.site.register(UrlRuleManage, UrlRuleManageAdmin)
# admin.site.register(RuleFilesManage, RuleFilesManageAdmin)
# # admin.site.register(RuleTxt)
