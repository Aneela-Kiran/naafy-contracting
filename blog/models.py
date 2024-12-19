from django.db import models
from django.utils.text import slugify

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    quotes = models.CharField(max_length=500, default="You Have the Power To Change the World!")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latest = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blogs"

# BlogImage Model
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return f"Image for {self.blog.title}"

    class Meta:
        verbose_name_plural = "Blog Images"

# BlogReply Model
class BlogReply(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)  # Removed unique=True
    phone_no = models.CharField(max_length=15)  # Changed to CharField
    reply = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    response = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} sent a reply on {self.blog.title}"
    
class Quotation(models.Model):
    quote = models.CharField(max_length=300)
    person_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quote