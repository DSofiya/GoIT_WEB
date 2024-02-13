from django.urls import path
from .views import (
    AddAuthorView,
    AddQuoteView,
    TagDetailView,
    AuthorDetailView,
)
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add_quote/", AddQuoteView.as_view(), name="add_quote"),
    path("add_author/", AddAuthorView.as_view(), name="add_author"),
    path("author/<str:pk>/", AuthorDetailView.as_view(), name="author"),
    path("quote_list/<str:name>/", TagDetailView.as_view(), name="quote_list"),
]
