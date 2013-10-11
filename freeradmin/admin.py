from django.contrib import admin

from freeradmin.models import Raduser, Radcheck, Radreply, Radgroup, Vlan


# INLINEs

class RaduserInline(admin.TabularInline):
  model = Raduser
  # fields = ('username', )




# MODELADMINs

class VlanAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', )
  #inlines = [ RaduserInline, ]
  search_fields = [ 'name', ]

class RaduserAdmin(admin.ModelAdmin):
  fields = ('username', 'vlan', 'radchecks', 'radreplies', 'radgroups' )
  filter_horizontal = [ 'radchecks', 'radreplies' ]
  list_display = ('username', 'vlan', )
  list_filter = ('vlan',)
  search_fields = [ 'username', ]

class RadgroupAdmin(admin.ModelAdmin):
  # fields = ('name', 'vlan', 'radchecks', 'radreplies', 'radgroups' )
  list_display = ('groupname', 'priority', )
  filter_horizontal = [ 'radchecks', 'radreplies' ]
  search_fields = [ 'groupname', ]

class RadcheckAdmin(admin.ModelAdmin):
  list_display = ('attribute', 'op', 'value')
  list_filter = ('attribute', )
  search_fields = [ 'attribute', 'value' ]

class RadreplyAdmin(admin.ModelAdmin):
  list_display = ('attribute', 'op', 'value')
  list_filter = ('attribute', )
  search_fields = [ 'attribute', 'value' ]



admin.site.register(Raduser, RaduserAdmin)
admin.site.register(Radgroup, RadgroupAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Radcheck, RadcheckAdmin)
admin.site.register(Radreply, RadreplyAdmin)

