"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'djangogenericproject.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        site_name = get_admin_site_name(context)

#        # append an app list module for "Applications"
#        self.children.append(modules.Group(
#            _('Youcoca.com'),
#            collapsible=True,
#            column=1,
#            children = [
#                modules.ModelList(
#                    _('Offices'),
#                    css_classes=('collapse',),
#                    models=('apps.space.models.Space', 'apps.space.models.Amenity', 'apps.space.models.Feedback', ),
#                ),
#                modules.ModelList(
#                    _('Blog'),
#                    css_classes=('collapse',),
#                    models=('apps.blog.models.Post', 'apps.blog.models.Subscription', ),
#                ),
#            ]
#        ))

        # append an app list module for "Applications"
        self.children.append(modules.Group(
            _('Universal Tutors'),
            collapsible=True,
            column=1,
            children = [
                modules.ModelList(
                    _('Settings'),
                    css_classes=('collapse',),
                    models=('apps.core.models.*', ),
                ),
                modules.ModelList(
                    _('Classes'),
                    css_classes=('collapse',),
                    models=('apps.classes.models.*', ),
                ),
                modules.ModelList(
                    _('Users'),
                    css_classes=('collapse',),
                    models=('apps.profile.models.*', 'apps.common.models.*', ),
                    exclude=('apps.profile.models.TopUpItem', ),
                ),
                modules.ModelList(
                    _('Top Up & Withdraw'),
                    css_classes=('collapse',),
                    models=('paypal.*', 'apps.profile.models.TopUpItem', 'apps.profile.models.WithdrawItem', ),
                ),
                modules.ModelList(
                    _('FAQ'),
                    css_classes=('collapse',),
                    models=('apps.faq.models.*', ),
                ),
#                modules.ModelList(
#                    _('Blog'),
#                    css_classes=('collapse',),
#                    models=('apps.blog.models.Post', 'apps.blog.models.Subscription', ),
#                ),
            ]
        ))

        self.children.append(modules.AppList(
            _('Social Signups and Authentication'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('allauth.*','emailconfirmation.*',),
        ))

        self.children.append(modules.AppList(
            _('Site Administration'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('django.contrib.*', 'apps.profile.models.NewsletterSubscription', 'flatblocks.*', ),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('File Browser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Getting In Touch With Raw Jam'),
            column=2,
            children=[
                {
                    'title': _('Technical Support'),
                    'url': 'mailto:support@rawjam.co.uk',
                    'external': True,
                },
                {
                    'title': _('Sales'),
                    'url': 'mailto:sales@rawjam.co.uk',
                    'external': True,
                },
                {
                    'title': _('View our up-to-date portfolio'),
                    'url': 'http://www.rawjam.co.uk/our-work/',
                    'external': True,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Reports'),
            column=2,
            children=[
                {
                    'title': _('Students'),
                    'url': reverse('reports_students'),
                    'external': True,
                },
                {
                    'title': _('Tutors'),
                    'url': reverse('reports_tutors'),
                    'external': True,
                },
                {
                    'title': _('Classes'),
                    'url': reverse('reports_classes'),
                    'external': True,
                },
                {
                    'title': _('Financial'),
                    'url': reverse('reports_financial'),
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Raw Jam News'),
            column=2,
            feed_url='http://www.rawjam.co.uk/feeds/news/',
            limit=5
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
