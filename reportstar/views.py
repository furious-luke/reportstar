from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from projects.models import Project
from questionnaire.models import RunInfo, Questionnaire, Subject
from questionnaire.emails import send_emails

def index(request, runid):
    run_info = get_object_or_404(RunInfo.objects, random=runid)
    sub = run_info.subject
    proj = run_info.project
    ctx = {
        'account': proj.account,
        'name': proj.name,
        'code': proj.code,
        'leader': sub,
        'institution': sub.institution,
        'members': proj.members.all(),
        'cpu': proj.cpu_usage,
        'runid': runid,
    }
    return render_to_response('index.html', ctx, context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def select_questionnaire(request):
    qs = Questionnaire.objects.all()
    return render_to_response('select_questionnaire.html', locals(), context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def select_subjects(request):
    qu = get_object_or_404(Questionnaire, pk=request.GET.get('q', None))
    subs = []
    qs = Project.objects.all()
    for proj in qs:
        if proj.leader:
            subs.append(proj.leader)
    return render_to_response('select_subjects.html', locals(), context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def email(request):
    qu = get_object_or_404(Questionnaire, pk=request.POST.get('questionnaire', None))
    subj_pks = request.POST.get('subjects', '').split(',')
    subjs = []
    for pk in subj_pks:
        if pk != '':
            subjs.append(get_object_or_404(Subject, pk=pk))
    qs = Subject.objects.all()
    for s in qs:
        if s in subjs:
            s.state = 'active'
            s.nextrun = datetime.now()
        else:
            s.state = 'inactive'
        s.save()
    return send_emails(request, qu.name)
