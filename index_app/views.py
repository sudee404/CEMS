from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from .models import Event, Category, Guest
from django.contrib.auth.decorators import login_required

User = get_user_model()


#################################################
################ Global views ###################
#################################################

def index(request):
    context = {}
    context['upcoming'] = Event.objects.all()

    return render(request, 'index.html', context)

@login_required(login_url='login')
def dashboard(request, pk):
    context = {}
    mode = request.GET.get('mode')
    my_user = User.objects.get(id=pk)
    if mode and mode == 'guest':
        context['events'] = Event.objects.filter(
            guest__user=my_user)

        return render(request, 'dashboard_guest.html', context)
    
    context['events'] = Event.objects.filter(
        host=my_user)
    
    return render(request, 'dashboard_host.html', context)


def gallery(request):
    return render(request, 'gallery.html', {})


def contact(request):
    return render(request, 'contacts.html', {})


#################################################
########### Event related views #################
#################################################

# Create
class EventCreateView(generic.CreateView):
    """Creates an event object
    """
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
            category = Category.objects.get(name=category_name)
            event = form.save(commit=False)
            event.category = category
            event.host = request.user
            event.save()
            return JsonResponse({'status': 'success', 'msg': 'Event added successfully', 'url': event.get_absolute_url()})

        return JsonResponse({'status': 'error', 'errors': form.errors})

# Read


class EventListView(generic.ListView):
    """Returns a list of available events 
    """

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


class EventDetailView(generic.DetailView):
    """Returns a single event object
    """
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['attending'] = Guest.objects.filter(
                user=self.request.user, event_id=self.kwargs['pk'])
            context["owner"] = self.model.objects.filter(
                id=self.kwargs['pk'], host=self.request.user)

        return context


# Update
class EventUpdateView(generic.UpdateView):
    model = Event
    fields = ('title', 'guests', 'description',
              'start_date', 'end_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by('-pk')
        context["event"] = self.model.objects.get(id=self.kwargs['pk'])

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            event = form.save(commit=False)
            event.category = Category.objects.get(
                name=request.GET.get("category"))
            event.host = request.user
            event.save()
            return JsonResponse({'status': 'success', 'msg': 'Event updated successfully', 'url': event.get_absolute_url()})
        return JsonResponse({'status': 'error', 'errors': form.errors})


# Delete
class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = 'event-list'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

#################################################
########### Category related views ##############
#################################################


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ('__all__')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})


#################################################
########### User related views #################
#################################################

class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "index_app/profile.html"


#################################################
########### Guest related views #################
#################################################
@login_required(login_url='login')
def add_guest(request, pk):
    event = Event.objects.get(id=pk)
    user = request.user
    try:
        guest = Guest.objects.create(user=user, event=event)
        guest.save()
        return redirect('event-detail', pk=pk)

    except:
        return redirect('event-detail', pk=pk,)
