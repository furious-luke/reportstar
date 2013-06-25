from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from projects.models import Project
from questionnaire.models import RunInfo

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
