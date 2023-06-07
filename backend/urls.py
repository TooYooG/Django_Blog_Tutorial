from django.urls import path
from backend.views import add_book, show_books


urlpatterns = [
    path("add_book", add_book,),
    path("show_books", show_books,),
]