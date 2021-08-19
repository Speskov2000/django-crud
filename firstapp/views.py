from django.http import HttpResponse


def products(request, productid=3):
    output = f"<h2>Product № {productid}</h2>"
    return HttpResponse(output)

def test(request):
    qwe = request.GET.get("qwe", "default?")

    output = f"qwe = {qwe}"
    return HttpResponse(output)

def users(request, id=1, name="bob", age=18):
    output = f"<h2>User</h2><h3>id: {id}  name: {name}, age: {age}</h3>"
    var = request.GET.get("name", "defalult")
    output += f" {var}"
    return HttpResponse(output)
