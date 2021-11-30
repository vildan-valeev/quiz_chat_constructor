from django.contrib import admin
from .models import Constructor, Staff, Service, Category, Event, Image, CompanyType, DefaultStaff, DefaultService, \
    DefaultCategory, BotText
from django.db import models
from django.forms import TextInput, Textarea, JSONField


#
# class StaffInline(admin.TabularInline):
#     model = Staff


class BotTextInline(admin.TabularInline):
    model = BotText
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class BotTextAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'text_id', 'const', 'created', 'updated']
    list_display_links = ['id']
    list_editable = ['text', 'text_id']
    # inlines = [ServiceInline, ]
    list_filter = ['text_id', 'const', ]
    save_on_top = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30})},
    }


class ConstructorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    inlines = [BotTextInline]
    save_on_top = True
    readonly_fields = ['created', 'updated']
    # formfield_overrides = {
    #     models.TextField: {'widget': JSONField(attrs={'rows': 4, 'cols': 40})},
    # }
    # def save_model(self, request, obj, form, change):
    #
    #     if not change and form.has_changed():  # new  post created
    #         super(ConstructorAdmin, self).save_model(request, obj, form, change)
    #         post_signal.send(self.__class__, instance=obj, change=change, updatedfields=form.changed_data)
    #         print('Constructor created')
    #     elif change and form.has_changed():  # post is actually modified )
    #         super(ConstructorAdmin, self).save_model(request, obj, form, change)
    #         post_signal.send(self.__class__, instance=obj, change=change, updatedfields=form.changed_data)
    #         print('Constructor modified')
    #     elif change and not form.has_changed():
    #         print('Constructor not created or not updated only saved ')


class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    # inlines = [ServiceInline, ]
    save_on_top = True


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'start', 'end', ]
    list_display_links = ['id', 'name']
    # inlines = [ServiceInline, ]
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    list_display_links = ['id', 'title']
    list_filter = ['const']
    # inlines = [StaffInline, ]
    save_on_top = True


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'duration', ]
    list_display_links = ['id', 'name']
    # inlines = [StaffInline, ]
    save_on_top = True


class DefaultCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company_type', ]
    list_display_links = ['id', 'title', ]
    # inlines = [StaffInline, ]
    filter_horizontal = ['service', ]
    save_on_top = True


class DefaultServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'duration',]
    list_display_links = ['id', 'name']
    # inlines = [StaffInline, ]
    # filter_horizontal = ['service', ]
    # list_editable = ['staff']
    save_on_top = True


class DefaultStaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company_type', ]
    list_display_links = ['id', ]
    # inlines = [StaffInline, ]
    list_editable = ['name', 'company_type', ]
    save_on_top = True
    save_as = True


admin.site.register(Image)
admin.site.register(CompanyType)
admin.site.register(BotText, BotTextAdmin)
admin.site.register(Constructor, ConstructorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(DefaultStaff, DefaultStaffAdmin)
admin.site.register(DefaultService, DefaultServiceAdmin)
admin.site.register(DefaultCategory, DefaultCategoryAdmin)
