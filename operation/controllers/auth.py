#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from operation.models.usermodels import User
#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='用户名:', max_length=100)
    password = forms.CharField(label='密__码:', widget=forms.PasswordInput())


#注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数
		username = uf.cleaned_data['username']
            	password = uf.cleaned_data['password']
            	#添加到数据库
            	User.objects.create(username= username,password=password)
            	return HttpResponse('regist success!!')
	        	
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf}, context_instance=RequestContext(req))

#登陆

def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

#登陆成功
def index(req):
	username = req.COOKIES.get('username','')
	li = {'userhome':'用户首页', 'hosts':'主机管理', 'monitors':'监控管理'}
	list = ['userhome', 'hosts', 'monitors']
	if False == req.COOKIES.has_key('username'):
		return HttpResponseRedirect('/login/')
	else:
		 return render_to_response('index.html' ,{'username':username, 'li':li, 'list':list,})
#退出
def logout(req):
    #response = HttpResponse('退出成功!!')
    response = HttpResponseRedirect('/login/')
    #清理cookie里保存username
    response.delete_cookie('username')
    response.write("<script>window.location='/login/'</script>")
    return response
