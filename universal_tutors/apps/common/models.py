from django.db import models
from apps.common.utils.abstract_models import TitleAndSlugModel, BaseModel

class FeedbackQuestion(TitleAndSlugModel):
    class Meta:
        ordering = ['position', 'id']

    optional_text_title = models.CharField(max_length=255, null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0, help_text='Question number position. NOTE: The system auto correct on front-end if some number is missing')

    def __unicode__(self):
        return self.title

class FeedbackQuestionOption(BaseModel):
    class Meta:
        ordering = ['position', 'id']

    title = models.CharField(max_length=255, null=True, blank=True)
    question = models.ForeignKey('FeedbackQuestion')
    position = models.PositiveSmallIntegerField(default=0, help_text='Answer ordering')

    def __unicode__(self):
        return self.title
    
class FeedbackAnswer(BaseModel):
    question = models.ForeignKey(FeedbackQuestion)
    option = models.ForeignKey(FeedbackQuestionOption)
    comment = models.CharField(max_length=255, null=True, blank=True)
    
    
#    def save(self, *args, **kwargs):
#        super(self.__class__, self).save(*args, **kwargs)
#
#        template = loader.get_template('common/emails/new_feedback.html')
#        context = Context({
#            'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
#            'feedback': self,
#        })
#        html = template.render(context)
#    
#        if settings.DEBUG:
#            to_email = 'vitor@rawjam.co.uk'
#        else:
#            to_email = settings.CONTACT_EMAIL
#        msg = EmailMessage(
#                           'New Feedback', 
#                           html, 
#                           settings.DEFAULT_FROM_EMAIL, 
#                           [to_email])
#        msg.content_subtype = 'html'
#        t = threading.Thread(target=msg.send, kwargs={'fail_silently': True})
#        t.setDaemon(True)
#        t.start()
    

#class Feedback(BaseModel):
#    question = models.ForeignKey(FeedbackQuestion)
#    question_answer = models.ForeignKey(FeedbackQuestionOption)
#    comment = models.CharField(max_length=255, null=True, blank=True)
    

#    QUESTION_CHOICES = (
#          (1, 'Not so hot'),
#          (2, "It'll do"),
#          (3, 'Not half-bad'),
#          (4, 'Top-notch'),
#          (5, 'Mind-blowing'),
#    )
#    
#    QUESTION_2_CHOICES = (
#          (1, "Couldn't be easier"),
#          (2, "Took no time"),
#          (3, 'Just fine'),
#          (4, 'A little tricky'),
#          (5, 'Far too hard'),
#    )
#    
#    question_1 = models.PositiveIntegerField('Question 1: How is your overall impression of Universal Tutors?', choices=QUESTION_CHOICES, )
#    question_1_comments = models.CharField('Are there any specific improvements you would like to see? (optional)', max_length=255, null=True, blank=True, )
#    question_2 = models.PositiveIntegerField('Question 2: How easy is it to find a great tutor?', choices=QUESTION_2_CHOICES, )
#    question_2_comments = models.CharField('How would you make finding a tutor easier? (optional)', max_length=255, null=True, blank=True, )
#    question_3 = models.PositiveIntegerField('Question 3: How is the classroom experience?', choices=QUESTION_CHOICES, )
#    question_3_comments = models.CharField('What would make the classroom experience even better? (optional)', max_length=255, null=True, blank=True, )
#    question_4 = models.PositiveIntegerField('Question 4: What do you think of the private dashboard area?', choices=QUESTION_CHOICES, )
#    question_4_comments = models.CharField('How can the dashboard area be improved? (optional)', max_length=255, null=True, blank=True, )
#    
#    class Meta:
#        verbose_name_plural = 'Feedback'
#        
    def __unicode__(self):
        return '%s - %s' % (self.question, self.option)
#    
#    def get_admin_url(self):
#        return 'http://%s/admin/common/feedback/%s/' % (settings.PROJECT_SITE_DOMAIN, self.id)
#    