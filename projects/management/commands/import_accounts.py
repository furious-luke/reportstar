from django.core.management.base import BaseCommand, CommandError
from projects.moab import parse_proc_usage
from projects.database import query_users, query_projects
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
        self.update_usage(args[0])

    def update_subjects(self):
        rows = query_users()
        for row in rows:
            sub, created = Subject.objects.get_or_create(email=row['email_address'])
            sub.title = row['title']
            sub.givenname = row['firstname']
            sub.surname = row['lastname']
            sub.institution = row['institution_name']
            sub.save()
            if created:
                self.stdout.write('Created new subject with email: %s'%row['email_address'])

    def update_projects(self):
        rows = query_projects()
        for row in rows:
            try:
                lead = Subject.objects().get(email=row['email'])
            except Subject.DoesNotExist:
                self.stdout.write('WARNING: Could not proces "%s", user "%s" does not exist.'%(row['project_id'], row['email']))
                continue
            proj, created = Project.objects.get_or_create(account=row['project_id'])
            proj.leader = lead
            proj.name = row['project_name']
            proj.code = row['project_code']
            proj.save()
            if created:
                self.stdout.write('Added new account to "%s": %s'%(row['email'], row['project_code']))

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
                self.stdout.write('WARNING: No project associated with account: %s'%acc)
                continue
            proj.cpu_usage = ch
            proj.save()
            self.stdout.write('Set usage for %s to: %g'%(acc, ch))
