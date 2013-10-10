from django.contrib import admin

from freeradmin.models import Radcheck, Radreply, Vlan

# INLINEs

class RadcheckInline(admin.TabularInline):
  model = Radcheck
  fields = ('username', )
  readonly_fields = ('op', 'attribute', 'value' )

class RadreplyInline(admin.TabularInline):
  model = Radreply
  fields = ('attribute', 'op', 'value' )


# MODELADMINs

class RadcheckAdmin(admin.ModelAdmin):
  fields = ('username', 'vlan', 'replies')
  filter_horizontal = [ 'replies' ]
  list_display = ('username', 'vlan', )
  list_filter = ('vlan',)
  readonly_fields = ('op', 'attribute', 'value' )
  search_fields = [ 'username', ]

class RadreplyAdmin(admin.ModelAdmin):
  fields = ('attribute', 'op', 'value')
  list_display = ('attribute', 'op', 'value')
  list_filter = ('attribute', )
  search_fields = [ 'attribute', 'value' ]



class VlanAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', )
  inlines = [ RadcheckInline, ]
  search_fields = [ 'name', ]




admin.site.register(Radcheck, RadcheckAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Radreply, RadreplyAdmin)
