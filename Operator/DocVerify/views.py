from django.forms import formset_factory
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.contrib import messages
from Login.models import *

from .forms import *
from .models import *
from Login.models import docvUser
from django.db import IntegrityError, transaction
# Create your views here.

def myauthd(func):
    def inner(request, *args, **kwargs):
        uid = ''
        if 'uid' in request.session:
            uid = request.session['uid']
            if docvUser.objects.get(pk = uid).user_type == 2:
                return func(request,*args,**kwargs)
            
        return redirect('/') 
    return inner

def myauthv(func):
    def inner(request, *args, **kwargs):
        uid = ''
        if 'uid' in request.session:
            uid = request.session['uid']
            if docvUser.objects.get(pk = uid).user_type == 1:
                # k = choice_verification_assistant.objects.filter(vuid_id = uid).first().pk
                return func(request,*args,**kwargs)
            
        return redirect('/') 
    return inner

def myauth(func):
    def inner(request, *args, **kwargs):
        uid = ''
        if 'uid' in request.session:
            uid = request.session['uid']
            print(uid)
            return func(request,*args,**kwargs)
            
        return redirect('/') 
    return inner

"""
render dashboard
"""
@myauth
def dashboard(request):
    uid = ''
    if 'uid' in request.session:
        uid = request.session['uid'] 

    duser = docvUser.objects.get(pk = uid)

    dt = datetime.now()


    return render(request, 'dashboard.html', {'duser':duser, 'datetime':dt})



"""
take details from user(dealing assistant) to save them in our db
"""
@myauthd
def verification_doc_recieved(request):
    form = VerificationDocumentDetailsForm()
    print('verify form')
    
    uid = ''
    if 'uid' in request.session:
        uid = request.session['uid']
    print(uid)
    duser = docvUser.objects.get(pk = uid)
    vdasnm = choice_dealing_assistant.objects.get(duid_id = uid).pk
    print(vdasnm)

    if request.method == 'POST':
        print('post')
        form = VerificationDocumentDetailsForm(request.POST)
        if form.is_valid():
            print('valid form')
            refno = form.cleaned_data['recieved_reference_no']
            recdt = form.cleaned_data['received_date']
            recdept = form.cleaned_data['received_dept']
            dcrecch = form.cleaned_data['doc_no_received_choice']
            docnrec = form.cleaned_data['doc_no_received']

            print('proceed to save')
            reg = VerificationDocumentDetails(recieved_reference_no=refno,
                                              received_date=recdt,
                                              received_dept=recdept,
                                              doc_no_received_choice=dcrecch,
                                              doc_no_received=docnrec,
                                              dealing_assistant_choice=choice_dealing_assistant.objects.get(duid_id = uid),)
                                              
            reg.save()

            vid = VerificationDocumentDetails.objects.filter(recieved_reference_no=refno).first().pk
            
            messages.success(request, 'Data Saved with Ref No {}'.format(refno))
            return redirect('addrn/{}'.format(vid))
        print('form noy valid')

    return render(request, 'docvrecieved.html', {'form': form, 'vdasnm':choice_dealing_assistant.objects.get(pk = vdasnm).dealing_assistant, 'duser':duser})

'''
func to handle enter roll numbers in bulk
'''

@myauthd
def addrn(request, vid):
    uid = ''
    if 'uid' in request.session:
        uid = request.session['uid']
    print(uid)
    duser = docvUser.objects.get(pk = uid)
    
    vobj = VerificationDocumentDetails.objects.get(pk=vid)
    showpvtb = VerificationPerformed.objects.filter(
        VerificationDocument_id_id=vobj.pk).all()
    print('1')
    FormSet = formset_factory(PerformVerificationForm, extra=vobj.doc_no_received,
                              min_num=vobj.doc_no_received, validate_min=True)
    print('FormSet')
    data = {
        'form-TOTAL_FORMS': vobj.doc_no_received,
        'form-INITIAL_FORMS': '1',
        
        'form-MAX_NUM_FORMS':vobj.doc_no_received,
        'form-MIN_NUM_FORMS':vobj.doc_no_received,
    }
    formset = FormSet(data)
    dform = PerformVerification1Form()
    print('formset')
   
    if request.method == 'POST':
        print('post')
        formset = FormSet(request.POST,data)
        print('formset post')
        dform = PerformVerification1Form(request.POST)


        if formset.is_valid() and dform.is_valid():
            print('valid')
            rn = []
            notrn = []
            with transaction.atomic():
                try:
                    for rn_form in formset:
                        print(dform.cleaned_data.get('documnet_type'), type(dform.cleaned_data.get('documnet_type')))
                        if dform.cleaned_data.get('documnet_type') == 1:
                            try:
                                rollnum = rn_form.cleaned_data.get('number')
                                rn.append(rollnum)
                            except:
                                messages.error(request, 'Something went wrong! for Number {}, Check DB'.format(rn_form.cleaned_data.get('number')))

                        elif dform.cleaned_data.get('documnet_type') == 2:
                            if not MarksheetVerification.objects.filter(marksheet_no=rn_form.cleaned_data.get('number')).exists():
                                messages.error(request,'Marksheet No. {},Not Available'.format(rn_form.cleaned_data.get('number')))
                                
                                notrn.append(rn_form.cleaned_data.get('number'))
                                continue
                            else:
                                try:
                                    rollnum = MarksheetVerification.objects.filter(marksheet_no=rn_form.cleaned_data.get('number')).first().roll_number
                                    rn.append(rollnum)
                                except:
                                    messages.error(request,'Marksheet No. {},Not Available'.format(rn_form.cleaned_data.get('number')))
                                    continue
                            
                        elif dform.cleaned_data.get('documnet_type') == 3:
                            if not CertificateVerification.objects.filter(certificate_no=rn_form.cleaned_data.get('number')).exists():
                                messages.error(request, 3,'Certificate No. {},Not Available'.format(rn_form.cleaned_data.get('number')))
                                notrn.append(rn_form.cleaned_data.get('number'))
                            else:    
                                try:
                                    rollnum = CertificateVerification.objects.filter(certificate_no=rn_form.cleaned_data.get('number')).first().roll_number
                                    rn.append(rollnum)
                                except:
                                    messages.error(request, 3,'Certificate No. {},Not Available'.format(rn_form.cleaned_data.get('number')))
                                    continue
                            
                        # messages.error(request, 'Something went wrong! for Number {}, Check DB'.format(rn_form.cleaned_data.get('number')))
                except IntegrityError:
                    return HttpResponse('ERROR from DB')

            print(rn)
            print('notrn',notrn)
            with transaction.atomic():
                try:
                    for j in range(len(notrn)):
                        if not VerificationPerformed.objects.filter(unpacked_rn=notrn[j],VerificationDocument_id_id=vobj.pk).exists():
                            if not VerificationPerformed.objects.filter(VerificationDocument_id_id=vobj.pk).count() == vobj.doc_no_received:
                               
                                for i in range(len(notrn)):
                                        obj = VerificationPerformed.objects.bulk_create(
                                            [
                                                VerificationPerformed(VerificationDocument_id_id=VerificationDocumentDetails.objects.filter(
                                                    recieved_reference_no=vobj.recieved_reference_no).first().pk, unpacked_rn=notrn[i], remark="(Auto) Data Not Found", status=False)
                                            ])
                                        messages.success(request, 'Data Not Available, No. {} with RefNo. {}, Marked Failed  '.format(notrn[i],vobj.recieved_reference_no))
                except IntegrityError:
                    return HttpResponse('ERROR from DB')

            with transaction.atomic():
                try:
                    for j in range(len(rn)):
                        if not VerificationPerformed.objects.filter(unpacked_rn=rn[j]).filter(VerificationDocument_id_id=vobj.pk).exists():
                            if not VerificationPerformed.objects.filter(VerificationDocument_id_id=vobj.pk).count() == vobj.doc_no_received:
                               
                                for i in range(len(rn)):
                                        obj = VerificationPerformed.objects.bulk_create(
                                            [
                                                VerificationPerformed(VerificationDocument_id_id=VerificationDocumentDetails.objects.filter(
                                                    recieved_reference_no=vobj.recieved_reference_no).first().pk, unpacked_rn=rn[i]),
                                            ])
                                        messages.success(request, 'Roll No. {} Added for RefNo. {}'.format(rn[i],vobj.recieved_reference_no))
                except IntegrityError:
                    return HttpResponse('ERROR from DB')

                    
            showpvtb = VerificationPerformed.objects.filter(
                VerificationDocument_id_id=vobj.pk).all()

            context = {
                'showdvtb': vobj, 'showpvtb': showpvtb, 'formset': formset, 'vobj': vobj, 'dform':dform,
            }
            return render(request, 'addrollnumb.html', context)
        else:
            print('error',formset.errors), print('non form error',formset.non_form_errors())

    context = {
        'formset': formset, 'vobj': vobj, 'showpvtb': showpvtb, 'dform':dform,
    }
    return render(request, 'addrollnumb.html', context)


class classallotment:
    rollnumb = 0
    verifer = 0

    def __init__(self, rollnumb, verifer) :
        self.rollnumb = rollnumb
        self.verifer = verifer

class classallotedverifier:
    verify_id = 0
    count = 0
    def __init__(self, verify_id, count) :
        self.verify_id = verify_id
        self.count = count


@myauthd
def revisit(request):
    uid = request.session['uid']
    vdasnm = choice_dealing_assistant.objects.get(duid_id = uid)
    print(vdasnm)
    form = RevisitForm()
    if request.method == 'POST':
        form = RevisitForm(request.POST)
        if form.is_valid:
            refno = form['reference_no'].value()

            if VerificationDocumentDetails.objects.filter(recieved_reference_no = refno,dealing_assistant_choice_id=vdasnm.pk ).exists():
                vobj = VerificationDocumentDetails.objects.filter(recieved_reference_no = refno).first()
                return render(request, 'revisit.html', {'form':form,'hi':vdasnm.dealing_assistant, 'vobj':vobj
                })

    return render(request, 'revisit.html', {'form':form,'hi':vdasnm})



@myauthd
def allotment(request, vid):
     # k = verificationdeatils id
    
    vdobj = VerificationDocumentDetails.objects.get(pk=vid)
    docnumb = VerificationDocumentDetails.objects.get(pk =vid).doc_no_received
    pvobj = VerificationPerformed.objects.filter(VerificationDocument_id_id = vid, status=False, remark__isnull=True)
    
    vaobj = choice_verification_assistant.objects.all()

    availpvobj = []

    for i in range(1, (vaobj.latest('pk').pk)+1 ):
        print(i)
        availpvobj.append(classallotedverifier(i, VerificationPerformed.objects.filter(status=False, verification_assistant_choice_id=i).count()) )
    
    for availva in availpvobj:
        print(availva.verify_id,choice_verification_assistant.objects.filter(pk = availva.verify_id).first().verification_assistant,'->' ,availva.count)
    
    availvaobj = VerificationPerformed.objects.filter()
    
    

    rnvalist = []
    if request.method == 'POST':
        for p in pvobj:
            if not request.POST.get('v-{}'.format(p.unpacked_rn)) == '':
                va = request.POST.get('v-{}'.format(p.unpacked_rn))
                if not VerificationPerformed.objects.filter(VerificationDocument_id_id=vid, status=False, unpacked_rn=int(p.unpacked_rn), verification_assistant_choice_id=int(va)).exists():
                    if type(VerificationPerformed(VerificationDocument_id_id=vid, status=False, unpacked_rn=int(p.unpacked_rn)).verification_assistant_choice_id) == type(None):
                
                        rnvalist.append(classallotment(rollnumb=p.unpacked_rn, verifer=va))
                        # print(p.unpacked_rn,"->" , request.POST.get('v-{}'.format(p.unpacked_rn)))
        
        
        # print(rnvalist)
        with transaction.atomic():
            for rv in rnvalist:
                
                try:
                    print(type(rv.rollnumb),rv.rollnumb,'->' ,type(rv.verifer),rv.verifer)
                    VerificationPerformed.objects.filter(VerificationDocument_id_id=vid, status=False, unpacked_rn=int(rv.rollnumb)).update(verification_assistant_choice_id=int(rv.verifer))
                    messages.success(request, 'Roll No. {} Assigned to verifier {}'.format(rv.rollnumb,rv.verifer))
                    
                except IntegrityError:
                    return HttpResponse('ERROR from DB')

    vdobj = VerificationDocumentDetails.objects.get(pk=vid)
    docnumb = VerificationDocumentDetails.objects.get(pk =vid).doc_no_received
    pvobj = VerificationPerformed.objects.filter(VerificationDocument_id_id = vid, status=False, remark__isnull=True)
    print('pvobj',pvobj.first())
    context = {
        'pvobj':pvobj.all(), 'vaobj':vaobj, 'availpvobj':availpvobj, 'vdobj':vdobj, 'docnumb':docnumb
    }
    return render(request, 'allotmentrn.html', context)
     

"""
funcn to only show which query needed operators attention i.e unverifed
"""

@myauthv
def verifytheselist(request):
     # vk = verification_assistant id
    uid = ''
    if 'uid' in request.session:
            uid = request.session['uid']
 
    vk = choice_verification_assistant.objects.get(vuid_id = docvUser.objects.get(pk = uid).pk).pk
    dvobj = VerificationPerformed.objects.all()
    # print(dvobj.filter(status=False, verification_assistant_choice_id=vk).order_by('is_created').values())
    # .filter(status = False).order_by('received_date').values()
    vdobj = VerificationDocumentDetails.objects.filter(status = False, dispatchstatus=False).all()

    for dv in dvobj:
        # print(dv)
        for vd in vdobj:
            # print(vd)
            print('vd',vd.pk, type(vd.pk))
            print('dv',dv.VerificationDocument_id, type(dv.VerificationDocument_id_id))
            if vd.pk == dv.VerificationDocument_id_id:
                print(vd.recieved_reference_no)

    context = {
        'dvobj': dvobj.filter(verification_assistant_choice_id=vk,status=False).filter(remark__isnull=True).exclude(remark__exact='').order_by('is_created').values(),
        'vdobj':vdobj
    }
    return render(request, 'verifytheselisting.html', context)


"""
func to perform verification,  fetch deatils and show them on our template
"""

@myauthv
def search_for_verification(request, k):
    #k = verification performed

    uid = ''
    if 'uid' in request.session:
            uid = request.session['uid']

    #vk verification assist
    vk = choice_verification_assistant.objects.get(vuid_id = docvUser.objects.get(pk = uid).pk).pk

    form = PerformVerification2Form()
    vdobj = VerificationDocumentDetails.objects.get(pk=k, dispatchstatus=False)

    unpkdrn = VerificationPerformed.objects.filter(
    VerificationDocument_id_id=vdobj.pk, status=False,verification_assistant_choice_id=vk, remark=None ).values('unpacked_rn')

    update_verification_status(k)

# # http://127.0.0.1:8000/dv/verifythese/verifythis/1
  
    if request.method == 'GET':
        rn = request.GET.get('roll_number')
        print(rn)
        # rn = 311111415011

        if not type(rn) == type(None):
            # remrk = form.cleaned_data['remark']
            print(rn, type(rn))
            reg = VerificationPerformed(
                unpacked_rn=rn, VerificationDocument_id_id=k)
            print('print')  #don't save

            # # search everything

            if CertificateVerification.objects.filter(roll_number=rn).exists() and MarksheetVerification.objects.filter(roll_number=rn).exists(): #and MigrationVerification.objects.filter(roll_number = rn).exists():
                try:
                    print('try')
                    certifct = CertificateVerification.objects.filter(roll_number=rn)
                    
                
                    markshit = MarksheetVerification.objects.filter(roll_number=rn)
                    
                
                    # migration = MigrationVerification.objects.filter(roll_number = rn) 
                    


                    rid = VerificationPerformed.objects.filter(unpacked_rn=rn, status=False).filter(remark__isnull=True).exclude(remark__exact='').filter(
                        VerificationDocument_id_id=k, verification_assistant_choice_id=vk).first().pk

                # img = mediaupload.objects.filter(roll_no=rn).first()

                    context = {
                        'unpkdrn': unpkdrn, 'vdobj': vdobj, 
                        'marksheetobj': markshit.all(), 
                        'certificateobj': certifct.first(),
                        # 'migobj':migration.latest('semester'),
                        'rid': rid,
                            'multiobj': VerificationDocumentDetails.objects.get(pk=k),
                        'searchrn': VerificationPerformed.objects.filter(VerificationDocument_id_id=k, verification_assistant_choice_id=vk).all(),
                        'form': form,
                        'verifyby': choice_verification_assistant.objects.get(pk=vk).verification_assistant
                    }
                    messages.success(
                        request, 'You Searched for Roll No. {}'.format(rn))
                    return render(request, 'searchforverify.html', context)
                except Warning:
                    print('warning')
                    messages.error(request, 'Data Not Available')
                    rid = VerificationPerformed.objects.filter(unpacked_rn=rn, status=False).filter(remark__isnull=True).exclude(remark__exact='').filter(
                        VerificationDocument_id_id=k, verification_assistant_choice_id=vk).first().pk
                    notavailable(request,rid)
            print('Data Not Available, #')
            messages.error(request, 'Data Not Available')
            rid = VerificationPerformed.objects.filter(unpacked_rn=rn, status=False).filter(remark__isnull=True).exclude(remark__exact='').filter(
                        VerificationDocument_id_id=k, verification_assistant_choice_id=vk).first().pk
            notavailable(request,rid)


    context = {

        'vdobj': vdobj,
        'unpkdrn': unpkdrn,
        'verifyby': choice_verification_assistant.objects.get(pk=vk).verification_assistant
    }
    return render(request, 'searchforverify.html', context)

'''
func to handle failed to verify if data not available
'''
@myauthv
def notavailable(request, k):
    uid = ''
    if 'uid' in request.session:
            uid = request.session['uid']
    # print(uid)

    #vk verification assist
    vk = choice_verification_assistant.objects.get(vuid_id = docvUser.objects.get(pk = uid).pk).pk

    remrk = '(Auto)Data Not Available in Database'
    print(remrk)
    print(k)
    if VerificationPerformed.objects.filter(pk=k, status=False).exists():
        check = VerificationPerformed.objects.filter(
            pk=k).update(remark=remrk)
        print(check)
        messages.success(request, 'We Marked Roll No. {} Not Verified, As Data Not Available'.format(VerificationPerformed.objects.get(pk=k).unpacked_rn))
'''
func to handle failed to verify
'''
@myauthv
def notverified(request, k):
    #k = verification performed
    uid = ''
    if 'uid' in request.session:
            uid = request.session['uid']
    # print(uid)

    #vk verification assist
    vk = choice_verification_assistant.objects.get(vuid_id = docvUser.objects.get(pk = uid).pk).pk

    if request.method == 'POST':
        form = PerformVerification2Form(request.POST)
        if form.is_valid():
            remrk = form.cleaned_data['remark']
            print(remrk)
            print(k)
            if VerificationPerformed.objects.filter(pk=k, status=False).exists():
                check = VerificationPerformed.objects.filter(
                    pk=k).update(remark=remrk)
                print(check)
                messages.success(request, 'You Marked Roll No. {} Not Verified'.format(VerificationPerformed.objects.get(pk=k).unpacked_rn))
                # vk = VerificationPerformed.objects.filter(pk=k).first(
                # ).VerificationDocument_id.verification_assistant_choice.pk
                return HttpResponseRedirect('/dv/verifythese')

"""
once deatils checked, here we can add them as verified..
"""

@myauthv
def addtoverified(request, k):
    # k is id of verfication perform tb
    print(k)
    uid = ''
    if 'uid' in request.session:
            uid = request.session['uid']
    # print(uid)

    #vk verification assist
    vk = choice_verification_assistant.objects.get(vuid_id = docvUser.objects.get(pk = uid).pk).pk
    check = VerificationPerformed.objects.filter(pk=k).update(status=True)
    
    kk = VerificationPerformed.objects.get(pk=k).VerificationDocument_id.pk
    update_verification_status(kk)
    if update_verification_status is True:
        messages.success(request, '{} is Verifed'.format(k))
        messages.success(request, 'You Marked Roll No. {} Verified'.format(VerificationPerformed.objects.get(pk=k).unpacked_rn))
    return HttpResponseRedirect('/dv/verifythese')


"""
funcn to update status of verified..
"""

def update_verification_status(k):
    vdobj = VerificationDocumentDetails.objects.get(pk=k)
    # nosearch = vdobj.doc_no_received
    cnt = VerificationPerformed.objects.filter(
        VerificationDocument_id_id=vdobj.pk).filter(status=True).count()
    print(cnt)
    if vdobj.doc_no_received == cnt:
        check = VerificationDocumentDetails.objects.filter(pk=k).update(
            status=VerificationPerformed.objects.filter(VerificationDocument_id_id=vdobj.pk).first().status)
        print(check)
        return True
    return False


"""
use this func to view comon listing..
"""

@myauth
def common_listing(request):
    uid = ''
    if 'uid' in request.session:
        uid = request.session['uid'] 

    duser = docvUser.objects.get(pk = uid)

    dvobj = VerificationDocumentDetails.objects.filter(dispatchstatus=False).all()
    dpobj = VerificationPerformed.objects.all()

    search_refno = dvobj.values('recieved_reference_no').distinct()
    search_recdept = dvobj.values('received_dept').distinct()
    # search_year = dvobj.dates('received_date', 'year')

    rnstatusonj = VerificationPerformed.objects.all()

    if request.method == 'GET':
        print('GET')
        org = request.GET.get('org')
        refno = request.GET.get('refno')
        year = request.GET.get('year')
        if not type(org)  == type(None) or not type(refno)== type(None):
            print(org, '/', refno, '/', year, type(org), type(None))

            ans = dvobj.filter(received_dept=org) | dvobj.filter(
                recieved_reference_no=refno)

            context = {
            'rnstatusonj': rnstatusonj,
            'ans': ans.distinct().order_by('received_date').values(),
            'search_refno': search_refno,
            'search_recdept': search_recdept,
            'dpobj':dpobj,
            'duser':duser,
            }

            return render(request, 'commonlisting.html', context)
    
    context = {
        'rnstatusonj': rnstatusonj,
        'dvobj': dvobj.order_by('-received_date').values(),
        'dpobj':dpobj,
        'search_refno': search_refno,
        'search_recdept': search_recdept,
        'duser':duser,
    }

    return render(request, 'commonlisting.html', context)


"""
use this func to search in comon listing..
"""

@myauth
def searchcomlist(request):
    dvobj = VerificationDocumentDetails.objects.filter(dispatchstatus=False).all()
    search_refno = dvobj.values('recieved_reference_no').distinct()
    search_recdept = dvobj.values('received_dept').distinct()
    # search_year = dvobj.dates('received_date','year')
    if request.method == 'GET':
        print('GET')
        org = request.GET.get('org')
        refno = request.GET.get('refno')
        year = request.GET.get('year')
        print(org, '/', refno, '/', year)

        ans = dvobj.filter(received_dept=org) | dvobj.filter(
            recieved_reference_no=refno)
        rnstatusonj = VerificationPerformed.objects.all()
        context = {
            'rnstatusonj': rnstatusonj,
            'ans': ans.distinct().order_by('received_date').values(),
            'search_refno': search_refno,
            'search_recdept': search_recdept,
            
        }

        return render(request, 'commonlisting.html', context)


"""
func to add deatils for dispatches...
"""

@myauthd
def send_dispatch(request, k):
    # k = verification details id
    uid = ''
    if 'uid' in request.session:
        uid = request.session['uid'] 

    duser = docvUser.objects.get(pk = uid)

    form = VerificationDispatchDetailsForm()
    
    print('dispatch form')
    if VerificationDocumentDetails.objects.filter(pk=k, status=True, dispatchstatus=False).exists() or VerificationPerformed.objects.filter(VerificationDocument_id_id=k).exclude(remark__isnull=True).exclude(remark__exact='').exclude(status=True).exists():
        verified_rn = VerificationPerformed.objects.filter(
            VerificationDocument_id_id=k, status=True).values()
        unverified_rn = VerificationPerformed.objects.filter(VerificationDocument_id_id=k, status=False).exclude(remark__isnull=True).exclude(remark__exact='').all()
        print(verified_rn)
        if request.method == 'POST':
            print('post')
            form = VerificationDispatchDetailsForm(request.POST)
            if form.is_valid():
                print('valid form')
                drefno = form.cleaned_data['dispatch_reference_no']
                ddt = form.cleaned_data['dispatch_date']
                ddept = form.cleaned_data['dispatch_dept']
                rmrk = form.cleaned_data['remark']
                
                
                reg = VerificationDispatchDetails(
                    dispatch_reference_no=drefno, dispatch_date=ddt, dispatch_dept=ddept, remark=rmrk,VerificationDocument_id_id = VerificationDocumentDetails.objects.get(pk=k).pk)


                print(' save')
                reg.save()
                reg1 = VerificationDocumentDetails.objects.filter(pk = k).update(dispatchstatus = True)
                # imp # VerificationDocumentDetails.objects.filter(pk = k).update(dispatchstatus = True)
                messages.success(
                    request, 'Data Added for Dispatch!, for {}!'.format(k))
                return HttpResponseRedirect('/dv/list')

        vdobj = VerificationDocumentDetails.objects.get(pk=k)
        context = {'updatern': vdobj.recieved_reference_no,
                    'updatestatus': vdobj.status, 'fm': form, 
                'verified_rn': verified_rn,'unverified_rn':unverified_rn
                ,'duser':duser,
                }
        return render(request, 'docdispatchdetails.html', context)
    else:
        messages.warning(
        request, "Not Verified!! Can't Dispatch ")
    return HttpResponseRedirect('/dv/list')


"""
func to show in btw dates report...
"""

@myauth
def reportdatewise(request):
    dvobj = VerificationDocumentDetails.objects.all()
    dpobj = VerificationPerformed.objects.filter(status=False).all()
    form = searchDateRange()
    if request.method == 'POST':
        form = searchDateRange(request.POST)
        if form.is_valid():
            fmDt = form.cleaned_data['fromDate']
            toDt = form.cleaned_data['toDate']
            print(fmDt, toDt)

            ans = dvobj.filter(received_date__gte=fmDt,
                            received_date__lte=toDt)
            if ans is not None:
                if VerificationPerformed.objects.filter(VerificationDocument_id_id=ans.first().pk).exists():
                    try:
                        rnstatusonj = VerificationPerformed.objects.all()

                        messages.success(request, 'Report!!')
                        context = {
                            'ans': ans.distinct().order_by('received_date').values(),
                            'form': form,
                            'rnstatusonj': rnstatusonj,
                            'dpobj':dpobj,
                        }

                        return render(request, 'reportdate.html', context)
                    except:
                        messages.warning(request, 'Report Not Available')

    context = {'form': form, }
    return render(request, 'reportdate.html', context)


"""
func to gen. report refno or dept wise...
"""

@myauth
def reportgenrefdept(request):
    dvobj = VerificationDocumentDetails.objects.all()
    dpobj = VerificationPerformed.objects.filter(status=False).all()
    
    deptobj = dvobj.values('received_dept').distinct()
    if request.method == 'POST':
        refno = request.POST.get('refno') 
        org =  request.POST.get('dept')
        print('refno',refno, org)

        if not (refno) == '' or not (org) == '':
            if not type(refno) == type(None) or not type(org) == type(None):

                ans = dvobj.filter(recieved_reference_no=refno) | dvobj.filter(
                    received_dept=org)

                if VerificationPerformed.objects.filter(VerificationDocument_id_id=ans.first().pk).exists():
                    try:
                        rnstatusonj = VerificationPerformed.objects.all()

                        messages.success(request, 'Report!!')
                        context = {
                            'ans': ans.distinct().order_by('received_date').values(),
                            
                            'rnstatusonj': rnstatusonj,
                            'dpobj':dpobj,
                            'deptobj':deptobj,
                            'dvobj': dvobj
                        }

                        return render(request, 'reportrefdept.html', context)
                    except:
                        messages.ERROR(request, 'Report Not Available')

    context = { 'deptobj':deptobj , 'dvobj': dvobj}
    return render(request, 'reportrefdept.html', context)

