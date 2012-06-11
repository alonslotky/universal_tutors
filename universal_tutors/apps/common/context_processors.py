from universal_tutors.apps.common.models import FeedbackQuestion


def feedback_questions(request):
    return {
        'questions': FeedbackQuestion.objects.all()
    }  