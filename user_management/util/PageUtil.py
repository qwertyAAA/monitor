class Page():
    def __init__(self,page_num,total_count,url_prefix,params,per_page=10,max_page=11):
        '''
        :param page_num: 当前的页码数
        :param total_count:总的记录
        :param url_prefix:a标签的href的前缀
        :param per_page:每页显示的条数
        :param max_page:最大的页码数
        :return: html分页结构str
        params:表示为了携带查询条件的参数
        '''
        self.url_prefix=url_prefix
        self.max_page=max_page

        import copy
        self.params=copy.deepcopy(params)

        total_page, m = divmod(total_count, per_page)
        if m:
            total_page += 1
        self.total_page=total_page
        # 如果输入的页码数超过了最大的页码数，默认返回最后一页
        try:
            page_num = int(page_num)
            if page_num > total_page:
                page_num = total_page
        except Exception as e:
            # 当输入的页码不是数字的时候，默认返回第一页
            page_num = 1
        self.page_num=page_num
        # 数据是根据当前页查找数据的起点和重点
        data_start = (page_num - 1) * per_page
        data_end = (page_num) *per_page

        self.data_start=data_start
        self.data_end=data_end

        # 定义页面上的页码 11 个页码
        max_page = 11
        # 当我的最大页数小于页面中页码的个数的时候  当前最大的页数赋值给页码
        if total_page < max_page:
            max_page = total_page

        half_max_page = max_page // 2

        # 页码上的页码开始的索引=
        page_start = page_num - half_max_page

        page_end = page_num + half_max_page

        # 判断
        if page_start <= 1:
            page_start = 1
            page_end = max_page

        if page_end > total_page:
            page_end = total_page
            page_start = total_page - max_page + 1
        self.page_start=page_start
        self.page_end = page_end

    def page_html(self):
            # 自己拼接分页的HTML
            html_str_list = []
            html_str_list.append('<li><a href="/{}?pn=1" >首页</a></li>'.format(self.url_prefix))
            if self.page_num <= 1:
                html_str_list.append( '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
            else:
                html_str_list.append('<li><a href="/{}?pn={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix,self.page_num - 1))

            print(self.params.urlencode())

             # pn=1&isSchoolJob=1&city=全国


            for i in range(self.page_start, self.page_end + 1):
                self.params['pn']=i
                if i == self.page_num:
                    html_str_list.append('<li class="active"><a href="/{0}/?pn={1}">{1}</a></li>'.format(self.url_prefix,i))
                else:
                    html_str_list.append('<li><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix,self.params.urlencode(),i))





            if self.page_num >= self.total_page:
                html_str_list.append('<li style="display:none"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
            else:
                html_str_list.append( '<li><a href="/{}/?pn={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix ,self.page_num + 1))

            html_str_list.append('<li><a href="/{}/?pn={}" >尾页</a></li>'.format(self.url_prefix,self.total_page))

            page_html = "".join(html_str_list)

            return page_html

