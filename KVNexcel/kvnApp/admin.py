from django.contrib import admin
from kvnApp.models import Tasks, Profile, Transaction,UserSubscription,SubscriptionModule

class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'price', 'deadline', 'level', 'topic','is_available' , 'status'  , 'accepted_by')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'is_email_verified')
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ('date_joined', 'last_login')

class TransactionAdmin(admin.ModelAdmin):  
    list_display = ('item', 'amount', 'phone_number', 'timestamp')

class UserSubcriptionAdmin(admin.ModelAdmin):   
    list_display = ('user','module','transaction')

# class UserProgressionAdmin(admin.ModelAdmin):
#     list_display = ('user','course','topic','progress','hours_watched')
class SubscriptionModuleAdmin(admin.ModelAdmin):
    list_display = ('name','price')

# admin.site.register(UserProgress, UserProgressionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserSubscription, UserSubcriptionAdmin)
admin.site.register(SubscriptionModule, SubscriptionModuleAdmin)
