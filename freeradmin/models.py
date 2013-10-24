from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError



class Raduser(models.Model):
  """ A user is allowed to authenticate to the freeradius server.
      A user may have many Radchecks and many Radreplies.
      A user representing a MAC must have a VLAN associated.
  """
  msg = "Please enter a MAC address in the form 'FFFFFFFFFFFF' (12 hexadecimal characters)"
  mac_address_validator = RegexValidator(r'^[0-9a-fA-F]{12,12}$', msg)

  username = models.CharField('MAC Address', max_length=64, unique=True, validators=[ mac_address_validator ])
  vlan = models.ForeignKey('Vlan', null=True, related_name='mac')
  radchecks = models.ManyToManyField('Radcheck', blank=True)
  radreplies = models.ManyToManyField('Radreply', blank=True)
  radgroups = models.ManyToManyField('Radgroup', blank=True)

  def __unicode__(self):
    return self.username

  class Meta:
    ordering = ['username']


class MacManager(models.Manager):
  """ The Manager for a MAC.
      It implements the constraint "MACs are a subset of Radusers"
  """
  def get_query_set(self):
    return super(MacManager, self).get_query_set().exclude(username='DEFAULT')

class Mac(Raduser):
  """ A MAC address is a Raduser in the business domain,
      where it is characterized only by a MAC address and a VLAN.
  """

  objects = MacManager()

  def address(self):
    return self.username

  class Meta:
    proxy = True



class Radgroup(models.Model):
  """ A group of Radusers sharing a set of radchecks and radreplies.
  """
  groupname = models.CharField(max_length=64, unique=True)
  priority = models.IntegerField(default=1)
  radchecks = models.ManyToManyField('Radcheck', blank=True)
  radreplies = models.ManyToManyField('Radreply', blank=True)

  def __unicode__(self):
    return self.groupname

  class Meta:
    ordering = ['groupname']



class Radcheck(models.Model):
  """ The check items are a list of attributes used to match the incoming request.
  """
  RACHECK_OPERATORS = (
    ('=', '='),
    (':=', ':='),
    ('==', '=='),
    ('+=', '+='),
    ('!=', '!='),
    ('>', '>'),
    ('>=', '>='),
    ('<', '<'),
    ('<=', '<='),
    ('=~', '=~'),
    ('!~', '!~'),
    ('=*', '=*'),
    ('!*', '!*'),
  )
  attribute = models.CharField(max_length=64, default='Cleartext-Password')
  op = models.CharField(max_length=2, choices=RACHECK_OPERATORS, default=':=')
  value = models.CharField(max_length=253)

  def __unicode__(self):
    return '%s %s %s' % (self.attribute, self.op, self.value)

  class Meta:
    ordering = [ 'attribute' ]
    unique_together = ('attribute', 'op', 'value')



class RadreplyManager(models.Manager):
  """ Exludes the radreplies for VLANs
  """
  def get_query_set(self):
    return super(RadreplyManager, self).get_query_set().exclude(attribute=settings.FREERADMIN_VLAN_ATTRIBUTE)

class Radreply(models.Model):
  """ The attributes which will be used in the reply to a request.
  """
  RADREPLY_OPERATORS = (
    ('=', '='),
    (':=', ':='),
    ('+=', '+='),
  )

  objects = RadreplyManager()

  def validate_reply_attribute(attr):
    if attr == settings.FREERADMIN_VLAN_ATTRIBUTE:
      raise ValidationError(u'The attribute %s is not allowed here. Please, go to the admin page for VLANs, instead.' % settings.FREERADMIN_VLAN_ATTRIBUTE)

  attribute = models.CharField(max_length=64, validators=[ validate_reply_attribute ])
  op = models.CharField(max_length=2, choices=RADREPLY_OPERATORS, default='=')
  value = models.CharField(max_length=253)

  def __unicode__(self):
    return '%s %s %s' % (self.attribute, self.op, self.value)

  class Meta:
    ordering = [ 'attribute' ]
    verbose_name_plural = 'radreplies'
    unique_together = ('attribute', 'op', 'value')


class VlanManager(models.Manager):
  """ Filters only the radreplies for VLANs
  """
  def get_query_set(self):
    return super(VlanManager, self).get_query_set().filter(attribute=settings.FREERADMIN_VLAN_ATTRIBUTE)

class Vlan(Radreply):

  objects = VlanManager()

  def name(self):
    return self.value

  def save(self, *args, **kwargs):
      self.attribute = settings.FREERADMIN_VLAN_ATTRIBUTE
      self.op = '='
      super(Vlan, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.value

  class Meta:
    proxy = True
    ordering = ['value']
