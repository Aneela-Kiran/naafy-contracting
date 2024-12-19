from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, BlogImage, BlogReply, Quotation
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
# Create your views here.
def blog_list(request):
    blogs = Blog.objects.all().order_by("-id")
    quote = Quotation.objects.all().first()
    paginator = Paginator(blogs, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj" : page_obj,
        "quote" : quote,
    }
    return render(request, "blog/blog.html", context)

@csrf_protect
def blog_details(request, slug):

    # Fetch the blog post based on the slug
    blog = get_object_or_404(Blog, slug=slug)

    # Handle form submission
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        reply = request.POST.get("reply")
        
        # Simple validation
        if name and email and reply:
            # Create and save the BlogReply instance
            BlogReply.objects.create(
                blog=blog,
                name=name,
                email=email,
                phone_no=phone_no,
                reply=reply
            )
            # Redirect to the same blog detail page to prevent form resubmission on refresh
            return redirect('blog:blog-details', slug=slug)
        else:
            # Handle form validation errors
            error_message = "Please fill in all required fields."

    else:
        error_message = None

    # Get the previous and next blog posts
    previous_blog = Blog.objects.filter(created_at__lt=blog.created_at).order_by('-created_at').first()
    next_blog = Blog.objects.filter(created_at__gt=blog.created_at).order_by('created_at').first()

    # Fetch blog images
    blog_images = BlogImage.objects.filter(blog=blog)

    context = {
        'blogs': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'blog_images': blog_images,
        'error_message': error_message,  # Pass the error message to the template
    }

    return render(request, "blog/blog-detail.html", context)