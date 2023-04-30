from django.contrib.auth import authenticate
from django.shortcuts import redirect, render, HttpResponsePermanentRedirect, HttpResponseRedirect
from .forms import *
from DocVerify.models import *
from django.contrib import messages
from django.contrib.auth.hashers import *

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            em = form.cleaned_data['email']
            nm = form.cleaned_data['name']
            pswrd = form.cleaned_data['password']
            utype = form.cleaned_data['user_type']

            
            reg = docvUser.create_user(email=em , name=nm.lower(), user_type = utype, password=pswrd)
            reg.save()
            messages.success(request, 'You can login now')
            if utype == 1:
                print('hehe')
                regv = choice_verification_assistant(verification_assistant= nm.lower(), vuid_id = docvUser.objects.get(email = em).pk )
                regv.save()
                return redirect('/')
            elif utype == 2:
                regd = choice_dealing_assistant(dealing_assistant= nm.lower(), duid_id = docvUser.objects.get(email = em).pk )
                print('heeh')
                regd.save()
                return redirect('/')
            print(em,nm,pswrd, utype)
            # return redirect('/')

    return render(request, 'signup.html', {'form':form})



def login(request):
    form = LoginForm()
    print('login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print('login post')

        print(form['email'].value())
        print(form['password'].value())
        if form.is_valid():
            print('form valid')
            em = form.cleaned_data['email']
            pswrd = form.cleaned_data['password']

            print(em, pswrd)
            duobj = docvUser.objects.filter(email = em)
            # user = authenticate(email=em, password=pswrd)
            print('here')
            
            print(form.errors)
            if check_password(pswrd,duobj.first().password):
                if duobj.exists():
                    print('exists')
                    request.session['uid'] = duobj.first().pk
                    if duobj.first().user_type == 1:
                        print('urtyp 1')
                        return HttpResponsePermanentRedirect('/dv/verifythese') #{}'.format(choice_verification_assistant.objects.filter(vuid_id = duobj.first().pk).first().pk)
                    elif duobj.first().user_type == 2:
                        return HttpResponsePermanentRedirect('/dv/documentvrecieved/', )
                    else:
                        return redirect('/dv/list/')
                
            # else:
            #     messages.warning(request, 'Check Credentails')

    return render(request, 'login.html', {'form':form})


from django.views.decorators.cache import cache_control
from django.core.cache import cache

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    
    # docvUser.objects.filter(pk = request.session['uid']).update(is_active=False)  use this only to permanentaly disable account
    request.session.flush()
    cache.clear()
    
    return HttpResponseRedirect('/')
