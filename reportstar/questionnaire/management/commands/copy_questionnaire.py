from django.core.management.base import BaseCommand, CommandError
from questionnaire.models import Questionnaire, QuestionSet, Question, Choice

class Command(BaseCommand):
    help = 'Copy a questionnaire'

    def add_arguments(self, parser):
        parser.add_argument('questionnaire', metavar='Q', nargs=1, help='the questionnaire to copy')
        parser.add_argument('new_name', metavar='N', nargs=1, help='new name for questionnaire')

    def handle(self, *args, **options):

        # Duplicate the questionnaire.
        try:
            qsnr = Questionnaire.objects.get(name=options['questionnaire'][0])
        except Questionnaire.DoesNotExist:
            raise CommandError('Questionnaire does not exist.')
        new_qsnr = Questionnaire(name=options['new_name'][0], redirect_url=qsnr.redirect_url)
        new_qsnr.save()

        # Duplicate each questionset.
        for qset in QuestionSet.objects.filter(questionnaire=qsnr):
            qset_pk = qset.pk
            qset.pk = None
            qset.questionnaire = new_qsnr
            qset.save()

            # Duplicate questions in questionset.
            for qu in Question.objects.filter(questionset=qset_pk):
                qu_pk = qu.pk
                qu.pk = None
                qu.questionset = qset
                qu.save()

            # Duplicate choices in each question.
            for ch in Choice.objects.filter(question=qu_pk):
                ch.pk = None
                ch.question = qu
                ch.save()
