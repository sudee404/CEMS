from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from .models import Event, Category


# Create your views here.

def index(request):
    context = {}
    context['upcoming'] = Event.objects.all()

    return render(request, 'index.html', context)


def dashboard(request, pk):
    return render(request, 'dashboard.html', {})


def gallery(request):
    return render(request, 'gallery.html', {})


def contact(request):
    return render(request, 'contacts.html', {})


class EventCreateView(CreateView):
    model = Event
    fields = ('title', 'guests', 'description',
              'start_date', 'end_date', 'poster')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by('-pk')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            category_name = request.GET.get("category")
            print(f'\nCat : {category_name}\n')
            category = Category.objects.get(name=category_name)
            event = form.save(commit=False)
            event.category = category
            event.host = request.user
            event.save()
            return JsonResponse({'status': 'success', 'url': event.get_absolute_url()})
        print(f'Eheeeaaa')

        return JsonResponse({'status': 'error', 'errors': form.errors})


class CategoryCreateView(CreateView):
    model = Category
    fields = ('__all__')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})


class EventListView(ListView):
    model = Event
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        query = self.request.GET.get("query")
        if query:
            context['query'] = query

        category = self.request.GET.get("category")
        if category:
            context['select_category'] = category

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        category = self.request.GET.get('category')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        if category:
            queryset = queryset.filter(
                Q(category__name__iexact=category)
            )

        return queryset


class EventDetailView(DetailView):
    model = Event


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "index_app/profile.html"
