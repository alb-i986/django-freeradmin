from django.conf import settings
from django.db import models

from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError



class Vlan(models.Model):
  name = models.CharField(max_length=253, unique=True)
  description = models.CharField(max_length=253, blank=True)

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['name']



class Radcheck(models.Model):
  RADOP_CHECK_TYPES = (
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
  msg = "Inserire un indirizzo MAC nella forma 'FFFFFFFFFFFF' (12 caratteri esadecimali)"
  mac_address_validator = RegexValidator(r'^[0-9a-fA-F]{12,12}$', msg)

  username = models.CharField('MAC Address', max_length=64, unique=True, validators=[ mac_address_validator ])
  attribute = models.CharField(max_length=64, default='Cleartext-Password')
  op = models.CharField(max_length=2, choices=RADOP_CHECK_TYPES, default=':=')
  value = models.CharField(max_length=253, default=settings.FREERADMIN_RADCHECK_DEFAULT_PASSWORD)
  vlan = models.ForeignKey(Vlan)
  replies = models.ManyToManyField('Radreply', blank=True)

  def __unicode__(self):
      return self.username

  class Meta:
      ordering = [ 'username' ]



class Radreply(models.Model):
  RADOP_REPLY_TYPES = (
      ('=', '='),
      (':=', ':='),
      ('+=', '+='),
  )

  def validate_reply_attribute(attr):
      if attr == 'Extreme-Netlogin-Vlan':
        raise ValidationError(u'The attribute `%s` is managed internally by the system. Please, edit the vlan in the `radcheck` table, instead.' % attr)

  attribute = models.CharField(max_length=64, validators=[ validate_reply_attribute ])
  op = models.CharField(max_length=2, choices=RADOP_REPLY_TYPES, default='=')
  value = models.CharField(max_length=253)

  def __unicode__(self):
      return '%s %s %s' % (self.attribute, self.op, self.value)

  class Meta:
      ordering = [ 'attribute' ]
      verbose_name_plural = 'radreplies'
      unique_together = ('attribute', 'op', 'value')
