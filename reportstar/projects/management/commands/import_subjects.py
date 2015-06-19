from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from projects.moab import parse_proc_usage
from projects.database import query_users, query_projects, query_project_members
from projects.models import Project
from questionnaire.models import Subject

class Command(BaseCommand):
    help = 'Import project information from moab and databases.'

    def handle(self, *args, **kwargs):
        self.update_subjects()

    def update_subjects(self):
        rows = query_users()
        for row in rows:
            sub, created = Subject.objects.get_or_create(email=unicode(row['email_address']))
            sub.title = unicode(row['title'])
            sub.givenname = unicode(row['firstname'], 'latin-1')
            sub.surname = unicode(row['lastname'], 'latin-1')
            sub.institution = unicode(row['institution_name'])
            sub.state = 'inactive' # auto inactive, only admins should be active
            if created:
                sub.nextrun = datetime.now();
                self.stdout.write(u'Created new subject with email: %s'%row['email_address'])
            sub.save()
