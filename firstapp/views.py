from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import UserForm, ProductForm
from .models import Person, Product


# получение данных из бд
def index(request):
    people = Person.objects.all()
    products = Product.objects.all()
    return render(request, "firstapp/index.html", {"people": people, "products": products})

def productsOfUser(request, userId):
    person = Person.objects.get(id = userId)
    products = person.product_set.all()
    # products = Person.objects.get(id = userId).product_set.all()
    return render(request, "firstapp/productsOfUser.html", {"products": products, "person": person})

# Создание нового пользователя
def createUser(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            person = Person()
            person.name = userForm.cleaned_data["name"]
            person.age = userForm.cleaned_data["age"]
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "firstapp/createUser.html", {"form": userForm})
    else:
        return render(request, "firstapp/createUser.html", {"form": UserForm()})


# Обновление пользователя
def updateUser(request, id):
    try:
        person = Person.objects.get(id=id)

        if request.method == "POST":
            userForm = UserForm(request.POST)
            if userForm.is_valid():
                person.name = userForm.cleaned_data["name"]
                person.age = userForm.cleaned_data["age"]
                person.save(update_fields=["name", "age"])
                return HttpResponseRedirect("/")
            else:
                return render(request, "firstapp/updateUser.html", {"form": userForm})
        else:
            userForm = UserForm(initial={
                "name": person.name,
                "age": person.age
            })
            return render(request, "firstapp/updateUser.html", {"form": userForm})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# Удаление пользователя
def deleteUser(request, id):
    try:
        Person.objects.filter(id=id).delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# Вывешивание товара на продажу
def createProduct(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            person = Person.objects.get(id=7) # От имени какого пользователя публиковать товар

            product = Product()
            product.person = person
            product.name = productForm.cleaned_data["name"]
            product.description = productForm.cleaned_data["description"]
            product.price = productForm.cleaned_data["price"]
            product.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "firstapp/createProduct.html", {"form": productForm})
    else:
        return render(request, "firstapp/createProduct.html", {"form": ProductForm()})

def updateProduct(request, id):
    try:
        product = Product.objects.get(id=id)

        if request.method == "POST":
            productForm = ProductForm(request.POST)
            if productForm.is_valid():
                product.name = productForm.cleaned_data["name"]
                product.description = productForm.cleaned_data["description"]
                product.price = productForm.cleaned_data["price"]
                product.save(update_fields=["name", "description", "price"])
                return HttpResponseRedirect("/")
            else:
                return render(request, "firstapp/updateUser.html", {"form": productForm})
        else:
            productForm = ProductForm(initial={
                "name": product.name,
                "description": product.description,
                "price": product.price
            })
            return render(request, "firstapp/updateUser.html", {"form": productForm})
    except Person.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Product {id} not found</h2>")


# Удаление продукта
def deleteProduct(request, id):
    try:
        Product.objects.filter(id=id).delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Product not found</h2>")