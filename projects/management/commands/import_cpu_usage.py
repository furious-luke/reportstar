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

        self.update_cpu_usage(args[0])

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
