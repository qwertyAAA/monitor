from django.shortcuts import render, redirect, HttpResponse
from organization import models
from django.http import JsonResponse
from user_management import models as m2


# Create your views here.
def message(request):
    obj = models.Department.objects.all()
    tid = request.GET.get("id", None)
    if tid:
        obj = models.Department.objects.filter(top_department=tid)
    return render(request, 'organization/message.html', {
        'obj': obj
    })


def edit(request):
    nid = request.GET.get('id', None)
    if request.is_ajax():
        obj = models.Department.objects.filter(id=nid).first()
        top_dep = obj.top_department
        if top_dep:
            top_dep = obj.top_department.name
        else:
            top_dep = ""
        print(obj)
        return JsonResponse({
            "did": obj.id,
            "name": obj.name,
            "en_name": obj.en_name,
            "code": obj.code,
            "phone": obj.phone,
            "address": obj.address,
            "func": obj.func,
            "user": obj.user.username,
            "tips": obj.tips,
            "top_dep": top_dep
        })
    if request.method == "POST":
        did = request.POST.get("did", None)
        dname = request.POST.get("dname")
        den_name = request.POST.get("en_name", None)
        dtop_dep = request.POST.get("top_dep", None)
        dcode = request.POST.get("code", None)
        dphone = request.POST.get("phone", None)
        daddress = request.POST.get("address", None)
        dfunc = request.POST.get("func", None)
        duser = request.POST.get("user", None)
        dtips = request.POST.get("tips", None)
        obj = models.Department.objects.filter(name=dname).first()
        top_obj = models.Department.objects.filter(name=dtop_dep).first()
        user = m2.User.objects.filter(username=duser).first()
        if obj:
            obj.name = dname
            obj.en_name = den_name
            obj.top_department = top_obj
            obj.code = dcode
            obj.phone = dphone
            obj.address = daddress
            obj.func = dfunc
            obj.user = user
            obj.tips = dtips
            obj.save()
        else:
            new_obj = models.Department.objects.create(
                name=dname,
                en_name=den_name,
                top_department=top_obj,
                code=dcode,
                phone=dphone,
                address=daddress,
                func=dfunc,
                tips=dtips,
                user=user,
                create_by=request.user.id
            )
        return redirect("/organization/message/")


def delete(request):
    pass
