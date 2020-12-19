from django.db import models
from django.utils.text import slugify

class Paragraph(models.Model):
    content = models.TextField()
    post = models.ForeignKey("Post",related_name='paragraphs',on_delete=models.CASCADE,blank=True,null=True)
    
    class Meta:
        ordering = ['id',]

class Post(models.Model):
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=120)
    header_image = models.ImageField(blank=True,null=True,upload_to='blog')
    title = models.CharField(max_length=300,unique=True)
    slug = models.SlugField(max_length=1000,blank=True,null=True,unique=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)
        
    
