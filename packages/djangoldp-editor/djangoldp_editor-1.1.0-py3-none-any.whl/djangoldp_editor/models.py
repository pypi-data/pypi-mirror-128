from django.db import models
from djangoldp.models import Model
from djangoldp_i18n.views import I18nLDPViewSet

class CodeFragment(Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    head = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(unique=True)
    class Meta:
        ordering = ['order']
    
    class Meta(Model.Meta):
        view_set = I18nLDPViewSet

    def __str__(self):
        return self.title

class HelloWorld(Model):
    helloword = models.CharField(max_length=255)

    def __str__(self):
        return self.helloword

class User(Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        anonymous_perms = ['add', 'change', 'delete', 'view']

    def __str__(self):
        return self.first_name