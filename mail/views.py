from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def base(request):
    return render(request, 'base.html')


def pictures(request):
    return render(request, 'pictures.html')


def fhsms(request):
    return render(request, 'fhsms.html')


# 图片
def upload(request):
    obj = request.FILES.get('upload_img')
    print(obj.name)
    # media路径下的图片 回传到富文本 json数据格式   服务器上图片的路径  img的方式回传到
    # 构建服务器的图片的路径
    path = os.path.join(settings.MEDIA_ROOT, obj.name)
    with open(path, 'wb') as f:
        for line in obj:
            f.write(line)
    result = {
        "error": 0,
        "url": '/media/' + obj.name
    }
    return JsonResponse(result)
