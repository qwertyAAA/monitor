from django.shortcuts import render, redirect, HttpResponse
from organization import models
from django.http import JsonResponse
from user_management import models as m2
from django.db.models import Q


# Create your views here.
def message(request):
    obj = models.Department.objects.all()
    obj1 = obj
    tid = request.GET.get("id", None)
    top = models.Department.objects.filter(id=tid).first()
    # print(top.name)
    if tid:
        obj = models.Department.objects.filter(top_department=top)
        # print(obj)
    return render(request, 'organization/message.html', {
        "obj1": obj1,
        'obj': obj,
        "top": top,
        "length": obj1.__len__()
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
    nid = request.POST.get("del_id")
    obj = models.Department.objects.filter(id=nid).first()
    obj.delete()
    return redirect("/organization/message/")


def search(request):
    obj = models.Department.objects.all()
    obj1 = obj
    text = request.POST.get("select_text")
    kind = request.POST.get("select_kind")
    top_id = request.POST.get("top", None)
    print("上级部门为：", top_id)
    q1 = Q()
    q1.connector = 'OR'
    q1.children.append(('code__contains', text))
    q1.children.append(('name__contains', text))
    q1.children.append(('en_name__contains', text))
    if kind == "全部":
        obj = models.Department.objects.filter(q1)
    elif kind == '本级':
        con = Q()
        con.add(q1, 'AND')
        q2 = Q()
        q2.connector = 'OR'
        if top_id:
            q2.children.append(('top_department', top_id))
        else:
            q2.children.append(('top_department', None))
        con.add(q2, 'AND')
        obj = models.Department.objects.filter(con)
    return render(request, 'organization/message.html', {
        "obj": obj,
        "msg": "1",
        "obj1": obj1,
        "length": obj1.__len__()
    })
