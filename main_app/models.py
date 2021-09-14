from django.db.models import Model, CharField, TextField, BooleanField, ForeignKey
from django.db.models.fields import DateField, DateTimeField, IntegerField
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField, ImageField

# Create your models here.

class Journal(Model):
  name = CharField(max_length=100)
  birthdate = DateField(auto_now=False, auto_now_add=False)
  total_memories = IntegerField(default=0)
  created_at = DateTimeField(auto_now_add=True)
  user = ForeignKey(User, on_delete=CASCADE, related_name='journals')

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']



class Memory(Model):
  title = CharField(max_length=200)
  content = TextField(max_length=500)
  created_at = DateTimeField(auto_now_add=True)
  is_public = BooleanField(default=False)
  photo = ImageField(upload_to='media/', blank=True, null=True)
  journal = ForeignKey(Journal, on_delete=CASCADE, related_name='memories')

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['created_at']

class Album(Model):
  title = CharField(max_length=200)
  description = CharField(max_length=300)
  created_at = DateTimeField(auto_now_add=True)
  user = ForeignKey(User, on_delete=CASCADE, related_name='albums')

  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ['created_at']



class Photo(Model):
  picture = ImageField(upload_to='media/')
  title = CharField(max_length=200)
  description = CharField(max_length=300)
  created_at = DateTimeField(auto_now_add=True)
  is_public = BooleanField(default=False)
  album = ForeignKey(Album, on_delete=CASCADE, related_name='photos')

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['created_at']