from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from projects.moab import parse_proc_usage
from projects.database import query_users, query_projects, query_project_members
from projects.models import Project
from questionnaire.models import Subject

class Command(BaseCommand):
    args = '<moab_file>'
    help = 'Import project information from moab and databases.'

    def handle(self, *args, **kwargs):

        # Must have been given a moab file.
        if len(args) < 1:
            raise CommandError('Must supply a moab stats filename.')

        self.update_subjects()
        self.update_projects()
        self.update_project_members()
        self.update_cpu_usage(args[0])

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

    def update_projects(self):
        rows = query_projects()
        for row in rows:
            try:
                lead = Subject.objects.get(email=unicode(row['email_address']))
            except Subject.DoesNotExist:
                self.stdout.write(u'WARNING: Could not proces "%s", user "%s" does not exist.'%(row['project_code'], row['email_address']))
                continue
            proj, created = Project.objects.get_or_create(account=unicode(row['project_code']))
            proj.leader = lead
            proj.name = unicode(row['project_name'])
            proj.code = unicode(row['project_research_code'])
            proj.description = unicode(row['project_description'], 'latin-1')
            proj.save()
            if created:
                self.stdout.write(u'Added new account to "%s": %s'%(row['email_address'], row['project_code']))

            # Update the leader to active.
            lead.state = 'active'
            lead.save()
            self.stdout.write(u'Set leader "%s" to active.'%lead.email)

    def update_project_members(self):
        rows = query_project_members()
        proj_mems = {}
        for row in rows:
            try:
                proj = Project.objects.get(account=unicode(row['project_code']))
            except Project.DoesNotExist:
                self.stdout.write(u'WARNING: Could not add member "%s" to project "%s", project does not exist.'%(row['email_address'], row['project_code']))
                continue
            try:
                user = Subject.objects.get(email=unicode(row['email_address']))
            except Subject.DoesNotExist:
                self.stdout.write(u'WARNING: Could not add member "%s" to project "%s", user does not exist.'%(row['email_address'], row['project_code']))
                continue
            proj_mems.setdefault(proj, []).append(user)
        for proj, mems in proj_mems.iteritems():
            proj.members = mems

    def update_cpu_usage(self, filename):

        # Try and parse the file.
        try:
            usage = parse_proc_usage(filename)
        except:
            raise CommandError('Error parsing moab stats file.')

        # Insert/update all information.
        for acc, ch in usage.iteritems():
            try:
                proj = Project.objects.get(account=acc)
            except Project.DoesNotExist:
                self.stdout.write(u'WARNING: No project associated with account: %s'%acc)
                continue
            if ch == None:
                ch = 0
            proj.cpu_usage = ch
            proj.save()
            self.stdout.write(u'Set usage for %s to: %g'%(acc, ch))
