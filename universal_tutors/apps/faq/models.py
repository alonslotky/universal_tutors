from django.db import models

class FAQSection(models.Model):
    """
    A FAQ Section
    """
    class Meta:
        verbose_name = 'FAQ Section'
        ordering = ['position']
    
    section = models.CharField(max_length=150)
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return self.section


class FAQItem(models.Model):
    """
    A FAQ Section
    """
    class Meta:
        verbose_name = 'FAQ Item'
        ordering = ['section__position', 'position']
    
    section = models.ForeignKey(FAQSection, related_name='items', null=True, blank=True)
    question = models.CharField(max_length=255)
    answers = models.TextField(verbose_name='Answer')
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return self.question
