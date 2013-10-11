from django.db import models

from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError



class Raduser(models.Model):
  """ A user who is allowed to authenticate to the freeradius server.
    A user may have many Radchecks and many Radreplies.
    A user must have associated a VLAN.
  """
  msg = "Please enter a MAC address in the form 'FFFFFFFFFFFF' (12 hexadecimal characters)"
  mac_address_validator = RegexValidator(r'^[0-9a-fA-F]{12,12}$', msg)

  username = models.CharField('MAC Address', max_length=64, unique=True, validators=[ mac_address_validator ])
  radchecks = models.ManyToManyField('Radcheck', blank=True)
  radreplies = models.ManyToManyField('Radreply', blank=True)
  radgroups = models.ManyToManyField('Radgroup', blank=True)
  vlan = models.ForeignKey('Vlan')

  def __unicode__(self):
    return self.username

  class Meta:
    ordering = ['username']



class Radgroup(models.Model):
  """ A group of Radusers. 
  """
  groupname = models.CharField(max_length=64, unique=True)
  priority = models.IntegerField(default=1)
  radchecks = models.ManyToManyField('Radcheck', blank=True)
  radreplies = models.ManyToManyField('Radreply', blank=True)

  def __unicode__(self):
    return self.groupname

  class Meta:
    ordering = ['groupname']



class Vlan(models.Model):
  name = models.CharField(max_length=253, unique=True)
  description = models.CharField(max_length=253, blank=True)

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['name']



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



class Radreply(models.Model):
  """ The attributes which will be used in the reply to a request.
  """
  RADREPLY_OPERATORS = (
    ('=', '='),
    (':=', ':='),
    ('+=', '+='),
  )
  def validate_reply_attribute(attr):
    if attr == 'Extreme-Netlogin-Vlan':
      raise ValidationError(u'The attribute `%s` is managed internally by the system. Please, edit the vlan in the `radcheck` table, instead.' % attr)

  #attribute = models.CharField(max_length=64, validators=[ validate_reply_attribute ])
  attribute = models.CharField(max_length=64)
  op = models.CharField(max_length=2, choices=RADREPLY_OPERATORS, default='=')
  value = models.CharField(max_length=253)

  def __unicode__(self):
    return '%s %s %s' % (self.attribute, self.op, self.value)

  class Meta:
    ordering = [ 'attribute' ]
    verbose_name_plural = 'radreplies'
    unique_together = ('attribute', 'op', 'value')
