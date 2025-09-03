# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html?utm_source

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  
from .router import execute

from .models import RequestLog             
from .utils import file_to_base64          
from .models import Content
from django.views.generic.edit import CreateView,DeleteView,UpdateView


from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def plutonium(request):
    context = {}

    if request.method == "POST":
       
        # user inputs
        # اذا موجود بيسفه مو موجود بيكون
        # ""
        # او
        # None

        #.post: for text
        user_text = request.POST.get("user_input_request", "")
        #.FILES: for files 
        user_file = request.FILES.get("user_input_file", None)

        # 
        user_file_b64 = ""
        
        # اذا كان الملف موجود
        if user_file:
            #نمرره للدالة عشان تحوله ل base64
            user_file_b64 = file_to_base64(user_file)
            try:
                # نرجع ال cursor للبداية
                user_file.seek(0)
            except Exception:
                # اكسبشن في حال بعض الملفات ماتقبل
                pass

        # نسوي لوق جديد بالمدخلات الموحودة
        log = RequestLog.objects.create(
            # اليوزر الي بنربطه فيه
            user= request.user,
            user_input_request= user_text,
            user_input_file_base64= user_file_b64,
        )

        #execute للفنكشن الي في الراوتر
        result = execute(user_text=user_text, user_file=user_file)

        # الرسبونس الي من السيرفر يكون نل فاضي في البداية
        server_text = ""
        server_file_b64 = ""


        # execute: ترجع اكثر من شكل للاوتبوت ممكن سترنج و ممكن دكشيرني 
        # isinstance: تتاكد ان الناتج نفس التايب الي جطيناه
        # مثلا نبغا الناتج يكون دكشيرني
        if isinstance(result, dict):
            #  لانه دكشيرني فنشوف اذا الكي رجع شيء فمناه انه هذا هو النوع
            # .get: تاخذ المقتاح و ترجع الناتح
            if result.get("type") == "image":
                # assign server_file_b64 to response value
                # و اذا ماكان موجود نخليه ""
                server_file_b64 = result.get("value", "")
            # في حال التايب كتابة
            elif result.get("type") == "text":
                server_text = result.get("value", "")
        else:
            # الناتح على حطته
            server_text = str(result)


        # نحدث الفاريبول
        log.server_response_text = server_text
        log.server_response_file_base64 = server_file_b64
        # نحفظ التغيرات في الداتا بيس
        log.save()

        # context update
        # has username, result_text,result_file_b64, logs
        context.update({
            # اخر طلب
            "log": log,
            "result_text": server_text,
            "result_file_b64": server_file_b64,

            # كل الطلبات
            # نسوي اكسس حق اللوقس, بعجها فلتر لليوزر نفسه
            # order_by("id"): حق الترتيب تصاعدي
            "logs" : RequestLog.objects.filter(user=request.user).order_by("id"),
        })

    return render(request, "plutonium.html", context)




class ContentCreate(LoginRequiredMixin, CreateView):
    model = Content
    fields = ['title', 'content','language' ]

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ContentUpdate(LoginRequiredMixin,UpdateView):
    model=Content
    fields= ["title", "content", "language"]
    
    success_url= '/plutonium'

class ContentDelete(LoginRequiredMixin,DeleteView):
    model=Content
    success_url='/plutonium'


def content_list(request):
    contents = Content.objects.all()
    return render(request, "content_list.html", {"contents": contents})
    
def content_detail(request, content_id):
    content=Content.objects.get(id=content_id)
    return render(request, "content_detail.html", {"content": content})

@login_required
def profile(request):
    contents = Content.objects.filter(user=request.user)
    return render(request, "profile.html", {"contents": contents})

