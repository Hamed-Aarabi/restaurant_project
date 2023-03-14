from django.contrib import admin
from .models import Client, Otp, Address
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import ClientChangeForm, ClientCreationForm



class AddressAdmin(admin.TabularInline):
    model = Address


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = ClientChangeForm
    add_form = ClientCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('username','email','profile_pic')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    inlines = (AddressAdmin,)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    # ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Client, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone','expired')
    list_filter = ('expired',)



