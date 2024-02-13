from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# from django.http import Http404
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .utils import get_mongodb
from .forms import AddQuoteForm, AuthorForm, QuoteForm
from bson.objectid import ObjectId
# from .models import Tag


def main(request, page=1):
    per_page = 10
    template_name = "quotes/index.html"
    db = get_mongodb()
    quotes = db.quoters.find()
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        template_name,
        context={"quotes": quotes_on_page, "paginator": paginator},
    )


class AuthorDetailView(View):
    template_name = "quotes/author.html"

    def get(self, request, pk: str):
        db = get_mongodb()
        author = db.authors.find_one({"_id": ObjectId(pk)})
        print(author)
        return render(request, self.template_name, context={"author": author})


class AddAuthorView(CreateView):
    template_name = "quotes/add_author.html"
    form_class = AuthorForm
    success_url = reverse_lazy("quotes:quote_list")


class TagDetailView(View):
    template_name = "quotes/quote_list .html"

    def get(self, request, name: str):
        db = get_mongodb()
        quotes = list(db.quoters.find({"tags": name}))
        context = {"tag": name, "quotes": quotes}
        return render(request, self.template_name, context)


class AddQuoteView(CreateView):
    template_name = "quotes/add_quote.html"
    form_class = QuoteForm
    success_url = reverse_lazy("quotes:quote_list")

    def get(self, request):
        form = AddQuoteForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            return redirect("quotes:quote_list")
        return render(request, self.template_name, {"form": form})
