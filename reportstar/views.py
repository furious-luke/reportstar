from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from projects.database import query_project
from projects.models import Project
from questionnaire.models import RunInfo

def index(request, runid):
    run_info = get_object_or_404(RunInfo.objects(), random=runid)
    proj = get_object_or_404(Project.objects(), leader=run_info.subject)
    info = query_project(proj.account)
    ctx = {
        'account': proj.account,
        'name': info['project_name'],
        'code': info['project_code'],
        'leader': run_info.subject.full_name(),
        'institute': run_info.subject.institute(),
        'members': [[m['title'], m['firstname'], m['lastname'], '(%s)'%m['institution']].join(' ') for m in info['members']],
        'cpu': proj.usage,
        'runid': runid,
    }
    return render_to_response('index.html', ctx, context_instance=RequestContext(request))
