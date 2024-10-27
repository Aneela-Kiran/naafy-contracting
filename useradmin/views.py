from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact, Email, Reviews, ContactDetails
from services.models import Service, Project, ProjectImages
from blog.models import Blog, BlogImage, BlogReply
from aboutus.models import About
from .forms import ServiceForm, ProjectImagesForm, ProjectForm, ReviewsForm, BlogImagesForm, BlogForm, ProfileForm, ContactDetailsForm, AboutUsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.paginator import Paginator

User = get_user_model()

@login_required
def dashboard_view(request):
    contacts = Contact.objects.all().order_by("-id")
    emails = Email.objects.all()
    services = Service.objects.all()
    blogs = Blog.objects.all()
    context = {
        "contacts" : contacts,
        "emails" : emails,
        "services" : services,
        "blogs" : blogs,
    }
    return render(request, "useradmin/dashboard.html", context)


''' *******************SERVICE SECTION******************************* '''
@login_required
def service_view(request):
    services = Service.objects.all().order_by("-id")
    paginator = Paginator(services, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "services" : page_obj,
    }
    return render(request, "useradmin/service-list.html", context)


def service_detail(request, slug):
    service = Service.objects.get(slug=slug)
    context = {
        "service" : service,
    }
    return render(request, "useradmin/service-detail.html", context)


def add_service_view(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Added Successfully!")
            return redirect("useradmin:service-list")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    return render(request, "useradmin/add-service.html", {"form" : form})

def edit_service_view(request ,slug):
    service = Service.objects.get(slug=slug)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Editied Sucessfully!")
            return redirect("useradmin:service-list")
    else:
        form = ServiceForm(instance=service)
    context = {
        "form" : form,
        "service" : service
    }
    return render(request, "useradmin/edit-service.html", context)

def delete_service_view(request, slug):
    service = Service.objects.get(slug=slug)
    service.delete()
    messages.success(request, "Service Deleted Successfully!!")
    return redirect("useradmin:service-list")

''' *******************PROJECT SECTION******************************* '''
@login_required
def project_view(request):
    projects = Project.objects.all().order_by("-id")
    paginator = Paginator(projects, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "projects" : page_obj,
    }
    return render(request, "useradmin/project-list.html", context)

def project_detail(request, slug):
    project = Project.objects.get(slug=slug)
    project_images = ProjectImages.objects.filter(project=project)
    context = {
        "project" : project,
        "images" : project_images,
    }
    return render(request, "useradmin/project-detail.html", context)

def add_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST, request.FILES)
        
        if project_form.is_valid():
            project = project_form.save()

            # Get the list of uploaded images
            images = request.FILES.getlist('image')

            # Loop through the images and save them individually
            for image in images:
                ProjectImages.objects.create(project=project, image=image)

            return redirect('useradmin:project-list')  # Redirect after success
    else:
        project_form = ProjectForm()
        image_form = ProjectImagesForm()

    context = {
        'project_form': project_form,
        'image_form': image_form,
    }
    return render(request, 'useradmin/add-project.html', context)

def edit_project(request, slug):
    # Fetch the project by id or return 404 if not found
    project = get_object_or_404(Project, slug=slug)

    # Fetch related images for the project
    images = ProjectImages.objects.filter(project=project)

    if request.method == "POST":
        # Form to edit the project details
        project_form = ProjectForm(request.POST, instance=project)
        image_form = ProjectImagesForm(request.POST, request.FILES)

        if project_form.is_valid():
            updated_project = project_form.save()

            # Check if new images are uploaded
            if request.FILES.getlist('image'):
                # Remove old images if you want to replace them (optional)
                images.delete()

                # Add new images
                for img in request.FILES.getlist('image'):
                    ProjectImages.objects.create(project=updated_project, image=img)

            messages.success(request, "Project updated successfully!")
            return redirect('useradmin:project-list')

        else:
            messages.error(request, "Error updating the project.")

    else:
        # Load the form with existing project data
        project_form = ProjectForm(instance=project)
        image_form = ProjectImagesForm()

    return render(request, 'useradmin/edit-project.html', {
        'project_form': project_form,
        'image_form': image_form,
        'project': project,
        'images': images,
    })

def delete_project(request, slug):
    project = Project.objects.get(slug=slug)
    project.delete()
    messages.success(request, "Project Deleted Successfully!!")
    return redirect("useradmin:project-list")

''' *******************EMAIL SECTION******************************* '''
@login_required
def email_view(request):
    emails = Email.objects.all().order_by("-id")
    paginator = Paginator(emails, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "emails" : page_obj,
    }
    return render(request, "useradmin/email-list.html", context)

def delete_email(request, id):
    email = Email.objects.get(id=id)
    email.delete()
    messages.success(request, "Email Deleted Successfully!!")
    return redirect("useradmin:email-list")

def mark_as_responded(request, id):
    email = Email.objects.get(id=id)

    email.responded = True
    email.save()

    messages.success(request, "Changed to Responded!")
    return redirect("useradmin:email-list")

''' *******************Contact SECTION******************************* '''
@login_required
def contact_view(request):
    contacts = Contact.objects.all().order_by("-id")
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/contact-list.html", {"contacts":page_obj})

def contact_detail(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, "useradmin/contact-detail.html", {"contact" : contact})

def delete_contact_view(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    messages.success(request, "Successfully Deleted!!")
    return redirect("useradmin:contact-list")

def contact_response(request, id):
    contact = Contact.objects.get(id=id)

    contact.responded = True
    contact.save()

    messages.success(request, "Changed to Responded!")
    return redirect("useradmin:contact-list")

''' *******************Reviews Section******************************* '''
@login_required
def reviews_list(request):
    reviews = Reviews.objects.all().order_by("id")
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/reviews-list.html", {"reviews": page_obj})

def review_detail(request, id):
    review = get_object_or_404(Reviews, id=id)
    return render(request, "useradmin/review-detail.html", {"review": review})

def add_review(request):
    if request.method == "POST":
        form = ReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect("useradmin:reviews-list")
        else:
            messages.error(request, "Failed to Add! Please Try Again!")
    else:
        form = ReviewsForm()
    return render(request, "useradmin/add-review.html", {"form" : form})

def edit_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    if request.method == "POST":
        form = ReviewsForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review Updated Successfully!")
            return redirect("useradmin:reviews-list")
        else:
            messages.error(request, "Failed! Please Try Again")
    else:
        form = ReviewsForm(instance=review)
    return render(request, "useradmin/edit-review.html", {"form": form, "review":review})

def delete_review(request ,id):
    review = get_object_or_404(Reviews, id=id)
    review.delete()
    messages.warning(request, "Review Deleted!")
    return redirect("useradmin:reviews-list")

''' *******************Blog Section******************************* '''
@login_required
def blog_list_view(request):
    blogs = Blog.objects.all().order_by("-id")
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/blogs-list.html", {"blogs" : page_obj})

def blog_details(request, slug):
    blogs = get_object_or_404(Blog, slug=slug)
    blog_images = BlogImage.objects.filter(blog=blogs)
    context = {
        "blogs" : blogs,
        "images" : blog_images
    }
    return render(request, "useradmin/blog-details.html", context)

def add_blog_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()

            images = request.FILES.getlist('image')

            for i in images:
                BlogImage.objects.create(blog=blog, image=i)
            messages.success(request, "Successfully Added!")
            return redirect("useradmin:blogs-list")
        messages.error(request, "Failed! Try Again!")
    else:
        blog_form = BlogForm()
        image_form = BlogImagesForm()

    context = {
        "form" : blog_form,
        "image_form" : image_form,
    }
    return render(request, "useradmin/add-blog.html", context)

def edit_blog_view(request, slug):
    # Fetch the project by id or return 404 if not found
    blog = get_object_or_404(Blog, slug=slug)

    # Fetch related images for the project
    images = BlogImage.objects.filter(blog=blog)

    if request.method == "POST":
        # Form to edit the project details
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        image_form = BlogImagesForm(request.POST, request.FILES)

        if blog_form.is_valid():
            updated_blog = blog_form.save()

            # Check if new images are uploaded
            if request.FILES.getlist('image'):
                # Remove old images if you want to replace them (optional)
                images.delete()

                # Add new images
                for img in request.FILES.getlist('image'):
                    BlogImage.objects.create(blog=updated_blog, image=img)

            messages.success(request, "Blog updated successfully!")
            return redirect('useradmin:blogs-list')

        else:
            messages.error(request, "Error updating the Blog.")

    else:
        # Load the form with existing Blog data
        blog_form = BlogForm(instance=blog)
        image_form = BlogImagesForm()

    context = {
        'form': blog_form,
        'image_form': image_form,
        'blog': blog,
        'images': images,
    }

    return render(request, 'useradmin/edit-blog.html', context)

def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    blog.delete()
    messages.warning(request, "Deleted!")
    return redirect("useradmin:blogs-list")

''' *******************Blog Reply Section******************************* '''
@login_required
def blog_reply_list(request):
    replies = BlogReply.objects.all()
    return render(request, "useradmin/blog-reply-list.html", {"replies":replies})

def reply_response(request, id):
    reply = BlogReply.objects.get(id=id)

    reply.response = True
    reply.save()

    messages.success(request, "Changed to Responded!")
    return redirect("useradmin:blog-reply-list")

def delete_reply(request, id):
    reply = BlogReply.objects.get(id=id)
    reply.delete()
    messages.success(request, "Deleted Successfully!")
    return redirect("useradmin:blog-reply-list")

def reply_detail_view(request, id):
    reply = get_object_or_404(BlogReply, id=id)
    return render(request, "useradmin/reply-detail.html", {"reply" : reply})

''' *******************Blog Reply Section******************************* '''
@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('useradmin:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'useradmin/profile.html', {'form': form, 'profile':profile})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("useradmin:dashboard")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
            
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are successfully logged In!")
                return redirect("useradmin:dashboard")
            else:
                messages.error(request, "User doesn't exist!!")

        except:
            messages.error(request, f"User with {username} doesn't exist")

    return render(request, "useradmin/login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('useradmin:login')

@login_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password Miss-Matched!!")
            return redirect("useradmin:change-password")
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect("useradmin:login")
        else:
            messages.error(request, "Old Password is not correct")
            return redirect("useradmin:change-password")
    return render(request, "useradmin/change-password.html")

''' *******************Contact Details Section******************************* '''
@login_required
def edit_contact_details(request):
    contact_details = ContactDetails.objects.first()
    if request.method == "POST":
        form = ContactDetailsForm(request.POST, instance=contact_details)
        if form.is_valid():
            form.save()
            messages.success(request, "Edited Successfully!")
            return redirect("useradmin:contact-details")
        else:
            messages.error(request, "Oops! Something went Wrong!")
    else:
        form = ContactDetailsForm(instance=contact_details)
    return render(request, "useradmin/edit-contact-details.html", {"form":form})

''' *******************Contact Details Section******************************* '''
@login_required
def about_us_view(request):
    about_us = About.objects.all().first()
    if request.method == "POST":
        form = AboutUsForm(request.POST, instance=about_us)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully!")
            return redirect("useradmin:about-us")
        messages.warning(request, "Please Try Again!")
    else:
        form = AboutUsForm(instance=about_us)
    return render(request, "useradmin/about-us.html", {"form" : form})