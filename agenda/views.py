from django.shortcuts import redirect, render,get_object_or_404
from .models import Contact
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


# Create your views here.
def index(request):
  contacts = Contact.objects.order_by('-id').filter(show=True)
  paginator = Paginator(contacts, 15)

  page = request.GET.get('p')
  contacts = paginator.get_page(page)

  return render(request, "index.html", {'contacts': contacts })


#Exibindo detalhes sobre algum contato da agenda.
def contact_details(request, contact_id):
  contact = get_object_or_404(Contact, id=contact_id)

  if not contact.show:
    raise Http404()


  return render(request, "contact_details.html", {'contact': contact })

def search(request):
  search = request.GET.get('search')
  
  if search is None or not search:
      messages.add_message(
        request, 
        messages.ERROR, 
        'Não é possível pesquisar sem digitar nada no campo de busca.')

      return redirect('index')

  fields = Concat('name', Value(' '), 'last_name')

  contacts = Contact.objects.annotate(
    full_name=fields
  ).filter(
    Q(full_name__icontains=search) | Q(email__icontains=search) | Q(telephone__icontains=search)
  )
  
  paginator = Paginator(contacts, 15)
  page = request.GET.get('p')

  contacts = paginator.get_page(page)

  return render(request, "search.html", {'contacts': contacts })