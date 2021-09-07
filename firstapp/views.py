from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.contrib.auth.models import User


# получение данных из бд
def index(request):
    people = User.objects.all()
    products = Product.objects.all()
    return render(request, "firstapp/index.html", {"people": people, "products": products})\

# def productsOfUser(request, userId):
#     person = Person.objects.get(id = userId)
#     products = person.product_set.all()
#     # products = Person.objects.get(id = userId).product_set.all()
#     return render(request, "firstapp/productsOfUser.html", {"products": products, "person": person})

# Вывешивание товара на продажу
def create(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            product = Product()
            product.user = request.user
            product.name = productForm.cleaned_data["name"]
            product.description = productForm.cleaned_data["description"]
            product.price = productForm.cleaned_data["price"]
            product.save()
            return HttpResponseRedirect("/product/")
        else:
            return render(request, "firstapp/create.html", {"form": productForm})
    else:
        return render(request, "firstapp/create.html", {"form": ProductForm()})

# def updateProduct(request, id):
#     try:
#         product = Product.objects.get(id=id)

#         if request.method == "POST":
#             productForm = ProductForm(request.POST)
#             if productForm.is_valid():
#                 product.name = productForm.cleaned_data["name"]
#                 product.description = productForm.cleaned_data["description"]
#                 product.price = productForm.cleaned_data["price"]
#                 product.save(update_fields=["name", "description", "price"])
#                 return HttpResponseRedirect("/")
#             else:
#                 return render(request, "firstapp/updateUser.html", {"form": productForm})
#         else:
#             productForm = ProductForm(initial={
#                 "name": product.name,
#                 "description": product.description,
#                 "price": product.price
#             })
#             return render(request, "firstapp/updateUser.html", {"form": productForm})
#     except Person.DoesNotExist:
#         return HttpResponseNotFound(f"<h2>Product {id} not found</h2>")


# # Удаление продукта
# def deleteProduct(request, id):
#     try:
#         Product.objects.filter(id=id).delete()
#         return HttpResponseRedirect("/")
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Product not found</h2>")