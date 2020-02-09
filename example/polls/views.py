from django.shortcuts import render

from .forms import SampleForm


def index(request):
    form = SampleForm()
    return render(request, "index.html", {"form": form})
