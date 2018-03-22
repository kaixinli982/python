from django.contrib import admin

# Register your models here.
from mock_pro import models as mock_pro_models

# admin.site.register(mock_pro_models.Person)

# class ChoiceInline(admin.StackedInline):
#     model=polls_models.Choice
#     extra=3
class Data_list(admin.TabularInline):
    model=mock_pro_models.Request_Data
    #extra=3


class mock_proAdmin(admin.ModelAdmin):
    fields = ['url','data','type','name','sign']
    inlines = [Data_list]




admin.site.register(mock_pro_models.Request,mock_proAdmin)
admin.site.register(mock_pro_models.Log)
admin.site.register(mock_pro_models.Request_Unite)
