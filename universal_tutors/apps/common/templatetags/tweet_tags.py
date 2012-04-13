import twitter
from django.core.cache import cache
from django.conf import settings
from django.template import Library, Node, Variable, TemplateSyntaxError

register = Library()
class TwitterLattestMsgNode(Node):
    def __init__(self, user, limit, tweets):
        self.tweets = tweets
        self.user = user
        self.limit = int(limit)

    def render(self, context):
        cache_key = "latest_tweets_%s_%d" % (self.user, self.limit)
        cached_elems = cache.get(cache_key, None)
        if cached_elems:
            context[self.tweets] = cached_elems
        else:
            try:
                api = twitter.Api()
                status_obj = api.GetUserTimeline(self.user)
                most_recent_messages = [{"text":s.text, "time":s.relative_created_at, "url": "http://twitter.com/%s/statuses/%s" % (self.user, s.id),} for s in status_obj][:self.limit]
                context[self.tweets] = most_recent_messages
                cache.set(cache_key, most_recent_messages, settings.TWITTER_TIMEOUT)
            except:
                context[self.tweets] = None
        return ''

@register.tag(name='get_twitter_messages')
def twitter_status(parser, token):
	"""
	Call this tag with: 
		get_twitter_messages bendell 10 as tweet
	"""
	bits = token.split_contents()

	if len(bits) != 5:
	    raise TemplateSyntaxError, "%s takes 7 arguments" % bits[0]	
	
	return TwitterLattestMsgNode(bits[1], bits[2], bits[4])