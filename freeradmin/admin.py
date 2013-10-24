from django.contrib import admin
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from freeradmin.models import Raduser, Radcheck, Radreply, Radgroup, Vlan, Mac



# CUSTOM ADMIN FILTERs

class UsersByVlanListFilter(SimpleListFilter):
  # Human-readable title which will be displayed in the
  # right admin sidebar just above the filter options.
  title = 'VLAN'

  # Parameter for the filter that will be used in the URL query.
  parameter_name = 'vlan'

  def lookups(self, request, model_admin):
    """
    Returns a list of tuples. The first element in each
    tuple is the coded value for the option that will
    appear in the URL query (the VLAN name). The second element is the
    human-readable name for the option that will appear
    in the right sidebar (the VLAN name).
    """
    vlan_replies = Radreply.objects.filter(attribute=settings.FREERADMIN_VLAN_ATTRIBUTE)
    vlans = [ r.value for r in vlan_replies ]
    return [ ( v, v) for v in vlans ]

  def queryset(self, request, queryset):
    """
    Returns the filtered queryset based on the value
    provided in the query string and retrievable via
    `self.value()`.
    """
    if not self.value():
      return queryset
    else:
      return queryset.filter(radreplies__value=self.value())


# INLINES

class RadgroupInline(admin.TabularInline):
  model = Radgroup

class MacInline(admin.TabularInline):
  model = Mac



# MODELADMINs

class VlanAdmin(admin.ModelAdmin):
  fields = ( 'value', )
  list_display = ( 'value', )
  search_fields = [ 'value', ]
  #inlines = [ MacInline ]



class MacAdmin(admin.ModelAdmin):
  fields = ('username', 'vlan')
  list_display = ('username', 'vlan')

  list_filter = ('vlan', )
  search_fields = [ 'username', ]



class RaduserAdmin(admin.ModelAdmin):
  fields = ('username', 'vlan', 'radchecks', 'radreplies', 'radgroups' )
  filter_horizontal = [ 'radchecks', 'radreplies' ]
  list_display = ('username', 'vlan', )

  list_filter = ('vlan', 'radgroups__groupname')
  list_editable = ()
  search_fields = [ 'username', ]
  #def bulk_update_vlans(self, request, queryset):
  #  queryset.update(vlan=request.vlan)
  #bulk_update_vlans.short_description = 'VLAN Bulk Update'
  #actions = [ 'bulk_update_vlans', ]

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
admin.site.register(Mac, MacAdmin)
