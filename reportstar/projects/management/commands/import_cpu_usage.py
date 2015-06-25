import decimal
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from projects.moab import parse_proc_usage, parse_simple_proc_usage
from projects.database import query_users, query_projects, query_project_members
from projects.models import Project
from questionnaire.models import Subject

class Command(BaseCommand):
    help = 'Import project information from moab and databases.'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1)
        parser.add_argument('--type', choices=['simple', 'moab'], default='moab')

    def handle(self, *args, **options):

        # Try and parse the file.
        try:
            if options['type'] == 'simple':
                usage = parse_simple_proc_usage(options['filename'][0])
            else:
                usage = parse_proc_usage(options['filename'][0])
        except:
            raise CommandError('Error parsing stats file.')

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
            try:
                proj.save()
            except decimal.InvalidOperation:
                raise CommandError('Not enough digits in model, please increase.')
            self.stdout.write(u'Set usage for %s to: %g'%(acc, ch))
