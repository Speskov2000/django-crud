from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ProductForm
from .models import Product
from learnDjango.views import isTokenValid


# получение всех товаров из бд
def index(request):
    products = Product.objects.all()
    return render(
            request,
            "firstapp/index.html",
            {"auth": request.session['jwtUser']['auth'], "products": products})


# Вывешивание товара на продажу
@isTokenValid
def create(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            product = Product()
            product.user_id = request.session['jwtUser']['user_id']
            product.user_name = request.session['jwtUser']['user_name']
            product.name = productForm.cleaned_data["name"]
            product.description = productForm.cleaned_data["description"]
            product.price = productForm.cleaned_data["price"]
            product.save()
            return HttpResponseRedirect("/product/")
        else:
            return render(
                    request, "firstapp/create.html", {"form": productForm})
    else:
        return render(request, "firstapp/create.html", {"form": ProductForm()})


# Изменение товара
@isTokenValid
def update(request, id):
    # Проверка авторизован ли юзер
    if request.session['jwtUser']['auth']:
        return HttpResponse("<h2>Необходимо войти в\
аккаунт для изменения товара</h2>")
    try:
        product = Product.objects.get(id=id)

        # Проверка владельца товара
        if request.session['jwtUser']['user_id'] != product.user_id:
            return HttpResponse("<h2>Вы не можете изменить не свой товар</h2>")

        # Обработка post запроса
        if request.method == "POST":
            productForm = ProductForm(request.POST)
            # Проверка корректности введённых данных
            if productForm.is_valid():
                product.name = productForm.cleaned_data["name"]
                product.description = productForm.cleaned_data["description"]
                product.price = productForm.cleaned_data["price"]
                # Обновить
                product.save(update_fields=["name", "description", "price"])
                return HttpResponseRedirect("/product/")
            else:
                return render(
                        request,
                        "firstapp/updateUser.html",
                        {"form": productForm})
        else:
            productForm = ProductForm(initial={
                "name": product.name,
                "description": product.description,
                "price": product.price
            })
            return render(
                    request, "firstapp/updateUser.html", {"form": productForm})
    except Product.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Продукт {id} не найден</h2>")


@isTokenValid
# Удаление продукта
def delete(request, id):
    if not request.user.is_authenticated:
        return HttpResponse("<h2>Необходимо войти в\
                аккаунт для удаления товара</h2>")
    try:
        product = Product.objects.get(id=id)
        # Проверка владельца товара
        if request.user.id != product.user_id:
            return HttpResponse("<h2>Вы не можете удалить не свой товар</h2>")

        product.delete()
        return HttpResponseRedirect("/product/")
    except Product.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Продукт {id} не найден</h2>")
