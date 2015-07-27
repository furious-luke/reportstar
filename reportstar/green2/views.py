from datetime import datetime
from collections import OrderedDict
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from projects.models import Project
from questionnaire.models import *
from questionnaire.emails import send_project_emails, send_subject_emails

def index(request, runid):
    run_info = get_object_or_404(RunInfo.objects, random=runid)
    sub = run_info.subject
    proj = run_info.project
    if proj:
        ctx = {
            'account': proj.account,
            'name': proj.name,
            'code': proj.code,
            'leader': sub,
            'institution': sub.institution,
            'members': proj.members.all(),
            'cpu': proj.cpu_usage,
            'storage': proj.disk_usage,
            'quota': proj.disk_quota,
            'runid': runid,
        }
    else:
        ctx = {
            'runid': runid,
        }
    return render_to_response('index.html', ctx, context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def select_questionnaire(request):
    qs = Questionnaire.objects.all()
    return render_to_response('select_questionnaire.html', locals(), context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def select_projects(request):
    qu = get_object_or_404(Questionnaire, pk=request.GET.get('q', None))
    projs = []
    for proj in Project.objects.all():
        if proj.leader:
            projs.append(proj)
    return render_to_response('select_projects.html', locals(), context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def select_subjects(request):
    qu = get_object_or_404(Questionnaire, pk=request.GET.get('q', None))
    subjs = Subject.objects.all()
    return render_to_response('select_subjects.html', locals(), context_instance=RequestContext(request))

@permission_required("questionnaire.management")
def email_projects(request):
    qu = get_object_or_404(Questionnaire, pk=request.POST.get('questionnaire', None))
    proj_pks = request.POST.get('projects', '').split(',')
    projs = []
    for pk in proj_pks:
        if pk != '':
            cur = get_object_or_404(Project, pk=pk)
            if cur not in projs:
                projs.append(cur)
    return send_project_emails(request, qu.name, projs)

@permission_required("questionnaire.management")
def email_subjects(request):
    qu = get_object_or_404(Questionnaire, pk=request.POST.get('questionnaire', None))
    subj_pks = request.POST.get('subjects', '').split(',')
    subjs = []
    for pk in subj_pks:
        if pk != '':
            cur = get_object_or_404(Subject, pk=pk)
            if cur not in subjs:
                subjs.append(cur)
    return send_subject_emails(request, qu.name, subjs)

@permission_required('questionnaire.management')
def document(request, proj_id, year):
    proj = get_object_or_404(Project, account=proj_id)
    ans = Answer.objects.filter(project=proj, runid=year)
    ctx = {'project': proj, 'year': year, 'answers': ans}
    return render_to_response('document.html', ctx, context_instance=RequestContext(request))

@permission_required('questionnaire.management')
def summary(request, year):
    questionnaire = get_object_or_404(Questionnaire, name='Users Survey')
    questions = Question.objects.filter(questionset__questionnaire=questionnaire)
    answers = []
    for qst in questions:
        if qst.type in ['open-textfield', 'open']:
            continue
        if qst.type == 'choice-yesno':
            choices = OrderedDict([('Yes', 0), ('No', 0)])
            val_to_choice = {'yes': 'Yes', 'no': 'No'}
        elif qst.type == 'choice-yesnodontknow':
            choices = OrderedDict([('Yes', 0), ('No', 0), ('Don\'t know', 0)])
            val_to_choice = {'yes': 'Yes', 'no': 'No', 'dontknow': 'Don\'t know'}
        else:
            choices = OrderedDict([(c, 0) for c in qst.choices()])
            val_to_choice = dict([(c.value, c) for c in qst.choices()])
        ans = Answer.objects.filter(question=qst, runid=year)
        # agg = 0
        # cnt = 0
        for a in ans:
            val = a.split_answer()
            if not val:
                continue
            ch = val_to_choice[val[0]]
            choices[ch] += 1
            # try:
            #     if qst.type in ['choice-yesno', 'choice-yesnodontknow']:
            #         if val[0] == 'yes':
            #             val = 1
            #         else:
            #             val = 0
            #     else:
            #         val = int(val[0])
            # except ValueError:
            #     continue
            # agg += val
            # cnt += 1
        # if cnt:
        #     agg = float(agg)/float(cnt)
        #     if qst.type in ['choice-yesno', 'choice-yesnodontknow']:
        #         agg = '%.02f%%'%(agg*100)
        #     else:
        #         agg = '%.02f'%agg
        cnt = sum(choices.values(), 0)
        for ch, val in choices.iteritems():
            if cnt:
                choices[ch] = '%.02f%%'%(100.0*choices[ch]/cnt)
            else:
                choices[ch] = '0.00%'
        answers.append((qst, choices))
    ctx = {'year': year, 'answers': answers}
    return render_to_response('summary.html', ctx, context_instance=RequestContext(request))

@permission_required('questionnaire.management')
def logos(request):
    projs = Project.objects.filter(~Q(logo__exact=''))
    ctx = {'projects': projs}
    return render_to_response('logos.html', ctx, context_instance=RequestContext(request))
