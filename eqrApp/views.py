from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import SaveOrderOfService
from django.shortcuts import get_object_or_404
from .models import Employee, OrderOfService


def context_data():
    context = {
        'page_name' : '',
        'page_title' : 'Chat Room',
        'system_name' : 'SISTEMA DE CONTROLE DE PATRIMÔNIO - ALFA',
        'topbar' : True,
        'footer' : True,
    }

    return context


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['employees'] = models.Employee.objects.count()
    context['ordens'] = models.OrderOfService.objects.count()
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def employee_list(request):
    context =context_data()
    context['page'] = 'employee_list'
    context['page_title'] = 'Lista de Bens'
    context['employees'] = models.Employee.objects.all()

    return render(request, 'employee_list.html', context)

@login_required
def manage_employee(request, pk=None):
    context =context_data()
    if pk is None:
        context['page'] = 'add_employee'
        context['page_title'] = 'Cadastro de Patrimônio'
        context['employee'] = {}
    else:
        context['page'] = 'edit_employee'
        context['page_title'] = 'Update Employee'
        context['employee'] = models.Employee.objects.get(id=pk)

    return render(request, 'manage_employee.html', context)

@login_required
def save_employee(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent into the request."

    else:
        if request.POST['id'] == '':
            form = forms.SaveEmployee(request.POST, request.FILES)
        else:
            employee = models.Employee.objects.get(id = request.POST['id'])
            form = forms.SaveEmployee(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                messages.success(request, f"{request.POST['employee_code']} has been added successfully.")
            else:
                messages.success(request, f"{request.POST['employee_code']} has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")
                    resp['msg'] += str(f"[{field.label}] {error}")

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Employee ID is Invalid")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(id=pk)
        return render(request, 'view_id.html', context)

@login_required
def view_scanner(request):
    context = context_data()
    return render(request, 'scanner.html', context)


@login_required
def view_details(request, code = None):
    if code is None:
        return HttpResponse("Employee code is Invalid")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(employee_code=code)
        return render(request, 'view_details.html', context)

@login_required
def delete_employee(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No data has been sent into the request."
    else:
        try:
            models.Employee.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Employee has been deleted successfully.')
        except:
            resp['msg'] = "Employee has failed to delete."

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def order_of_service_list(request):
    context = context_data()
    context['page'] = 'order_of_service_list'
    context['page_title'] = 'Lista de Ordens de Serviço'
    context['orders'] = models.OrderOfService.objects.all()
    return render(request, 'order_of_service_list.html', context)


@login_required
def manage_order_of_service(request, pk=None):
    context = context_data()
    if pk is None:
        context['page'] = 'add_order_of_service'
        context['page_title'] = 'Cadastro de Ordem de Serviço'
        order_of_service_instance = None
    else:
        context['page'] = 'edit_order_of_service'
        context['page_title'] = 'Editar Ordem de Serviço'
        order_of_service_instance = get_object_or_404(models.OrderOfService, id=pk)

    if request.method == 'POST':
        form = forms.SaveOrderOfService(request.POST, instance=order_of_service_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ordem de Serviço salva com sucesso.')
            return redirect('order-of-service-list')
    else:
        form = forms.SaveOrderOfService(instance=order_of_service_instance)

    context['form'] = form
    return render(request, 'manage_order_of_service.html', context)



@login_required
def view_order_details(request, pk=None):
    if pk is None:
        return HttpResponse("ID da Ordem de Serviço é inválido")
    context = context_data()
    context['order'] = get_object_or_404(models.OrderOfService, id=pk)
    return render(request, 'view_order_details.html', context)


@login_required
def delete_order(request, pk=None):
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = "Nenhum dado foi enviado na requisição."
    else:
        try:
            order = get_object_or_404(models.OrderOfService, id=pk)
            order.delete()
            resp['status'] = 'success'
            messages.success(request, 'Ordem de Serviço foi deletada com sucesso.')
        except Exception as e:
            resp['msg'] = f"Falha ao deletar a ordem de serviço. Erro: {str(e)}"
    return HttpResponse(json.dumps(resp), content_type="application/json")