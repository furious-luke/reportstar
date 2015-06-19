from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from projects.quota import parse_quota
from projects.database import query_users, query_projects, query_project_members
from projects.models import Project
from questionnaire.models import Subject

class Command(BaseCommand):
    args = '<quota_file>'
    help = 'Import project disk quotas.'

    def handle(self, *args, **kwargs):

        # Must have been given a moab file.
        if len(args) < 1:
            raise CommandError('Must supply a disk quota filename.')

        self.update_quota(args[0])

    def update_quota(self, filename):

        # Try and parse the file.
        try:
            quota = parse_quota(filename)
        except:
            raise CommandError('Error parsing quota file.')

        # Insert/update all information.
        for acc, vals in quota.iteritems():
            try:
                proj = Project.objects.get(account=acc)
            except Project.DoesNotExist:
                self.stdout.write(u'WARNING: No project associated with account: %s'%acc)
                continue
            proj.disk_quota = vals['quota']
            proj.disk_usage = vals['usage']
            proj.save()
            self.stdout.write(u'Updated disk quota for %s.'%acc)
