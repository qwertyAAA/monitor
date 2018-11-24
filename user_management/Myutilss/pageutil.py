class Page():
    def __init__(self,models,request,per_page=10,max_page=11):
        self.models=models
        self.request=request
        self.per_page=per_page
        self.max_page=max_page
    def Sum(self):

        #分页三要素：总条数 每页显示数量 当前页
        #通过get请求获取page_num当前页
        if self.request.method=='GET':
            page_num=self.request.GET.get('pn')
        else:
            page_num=self.request.POST.get('pagenum',None)
        #总页数
        total_count=self.models.count()#总数据量
        total_page,m=divmod(total_count,self.per_page)
        if m!=0:
            total_page+=1
        try:
            page_num = int(page_num)
            if page_num>total_page:
                page_num=total_page
            if page_num<1:
                page_num=1
        except:
            #当输入的页码不是数字的时候默认页为1
            page_num=1


        #每页的第一条数据
        data_start=(page_num-1)*self.per_page
        #每页最后一条数据
        data_end=(page_num)*self.per_page

        #定义页面上的页码总数
        if total_page<self.max_page:
            max_page=total_page

        half_page=self.max_page//2
        #页面上的第一页
        page_start=page_num-half_page
        #页面上最后一页
        page_end = page_num + half_page
        print(page_start)
        # if page_start<=0:
        #     page_start=1
        #     page_end=1
        if page_end<self.max_page:
            page_end=self.max_page
        if page_end>total_page:
            page_end=total_page
            page_start=total_page-self.max_page
        if page_start<1:
            page_start=1
        if page_num<1:
            page_num=1
        if page_start==1 and page_end==1:
            page_delete=page_num
            page_add=page_num
        else:
            page_add=page_num+1
            page_delete=page_num-1
            if page_delete<1:
                page_delete=1
            if page_add>page_end:
                page_add=page_end
        #all可以进行切片
        stu=self.models[data_start:data_end]#django分页就是切片

        #返回的html结构
        html_list=[]
        html_list.append('<li><a href="?pn=1">首页</a></li>')
        html_list.append('<li><a href="?pn={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(page_delete))

        for i in range(page_start,page_end+1):
            if i==page_num:
                html_list.append('<li class="active"><a href="?pn={}">{}</a></li>'.format(i,i))
            else:
                html_list.append('<li><a href="?pn={}">{}</a></li>'.format(i,i))

        html_list.append('<li><a href="?pn={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(page_add))
        html_list.append('<li><a href="?pn={}">未页</a></li>'.format(total_page))
        page_html=''.join(html_list)

        return stu,page_html