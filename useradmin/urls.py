from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "useradmin"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),

    #Path for Services
    path("services/", views.service_view, name="service-list"),
    path("add-service/", views.add_service_view, name="add-service"),
    path("<slug:slug>/edit-service/", views.edit_service_view, name="edit-service"),
    path("<slug:slug>/delete/", views.delete_service_view, name="delete-service"),
    path("service-details/<slug:slug>/", views.service_detail, name="service-detail"),


    #path for Projects
    path("projects/", views.project_view, name="project-list"),
    path("add-project/", views.add_project, name="add-project"),
    path("edit-project/<slug:slug>/", views.edit_project, name="edit-project"),
    path("delete-project/<slug:slug>/", views.delete_project, name="delete-project"),
    path("project-details/<slug:slug>/", views.project_detail, name="project-detail"),

    #Email Section
    path("emails/", views.email_view, name="email-list"),
    path("delete-email/<int:id>", views.delete_email, name="delete-email"),
    path("email/<int:id>/responded/", views.mark_as_responded,name="mark-as-responded"),

    #About us Section
    path("edit-about-us/", views.about_us_view, name="about-us"),

    #Contact Section
    path("contacts/", views.contact_view, name="contact-list"),
    path("edit-contact-details/", views.edit_contact_details, name="contact-details"),
    path("contact-detail/<int:id>/", views.contact_detail, name="contact-detail"),
    path("delete/<int:id>/", views.delete_contact_view, name="delete-contact"),
    path("contact/<int:id>/responded/", views.contact_response, name="contact-response"),

    #General Services Section
    path("general-services/", views.gen_service_list, name="gen-service-list"),
    path("general-services/add/", views.add_general_service, name="add-gen-service"),
    path('general-service/<int:service_id>/', views.general_service_detail, name='general-service-detail'),
    path("general-services/edit/<int:id>/", views.edit_general_service, name="edit-gen-service"),
    path("general-services/delete/<int:id>/", views.delete_gen_service, name="del-gen-service"),

    #Reviews Section
    path("reviews/", views.reviews_list, name="reviews-list"),
    path("add-reviews/", views.add_review, name="add-reviews"),
    path("edit-review/<int:id>/", views.edit_review, name="edit-review"),
    path("review-detail/<int:id>/", views.review_detail, name="review-detail"),
    path("delete-review/<int:id>/", views.delete_review, name="delete-review"),

    #Blogs Section
    path("blogs-list/", views.blog_list_view, name="blogs-list"),
    path("add-blog/", views.add_blog_view, name="add-blog"),
    path("edit-blog/<slug:slug>/", views.edit_blog_view, name="edit-blog"),
    path("blogs-details/<slug:slug>/", views.blog_details, name="blog-details"),
    path("delete/<slug:slug>/", views.delete_blog, name="delete-blog"),

    #Blog Replies Section
    path("blog-replies/", views.blog_reply_list, name="blog-reply-list"),
    path("reply-detail/<int:id>/", views.reply_detail_view, name="reply-detail"),
    path("delete-response/<int:id>/", views.delete_reply, name="delete-reply"),
    path("response/<int:id>/", views.reply_response, name="reply-response"),

    #UserAuths Section
    path("profile/", views.profile_view, name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password, name="change-password"),
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
