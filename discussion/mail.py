import copy
import settings
import traceback

from django.db.models import signals
from django.dispatch import dispatcher
from django.template import Context, loader, Template, TemplateDoesNotExist
from django.core.mail import mail_admins
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from discussion.models import CommentNode
from blog.models import Post


DEFAULT_COMMENT_SUBJECT = '''New comment for post "{{ post.name }}" by "{{ comment.user.first_name }}"'''
DEFAULT_COMMENT_BODY = '''Comment text:
{{ comment.body }}

Reply: {{site_url}}{{ comment.get_absolute_url }}'''


def get_users_to_send_email(post, comment):
    all_comments = CommentNode.objects.for_object(post)
    #XXX: django before rev. ~7026 doesn't have Model.__hash__ so equal instances
    #XXX: would not match if we constructed set from comment.user instances instead
    user_ids = set([int(c.user_id) for c in all_comments])
    user_ids.add(int(post.author.id))
    user_ids.discard(int(comment.user.id))
    return User.objects.filter(id__in=list(user_ids)).distinct()


def fetch_old_comment(comment):
    if not comment.id:
        return None
    else:
        return CommentNode._default_manager.get(id=comment.id)


# send mail on comment
def send_comment_by_mail(instance, created):
    if not created:
        return
    comment = instance
    if comment.content_type.model_class() != Post:
        return
    post = Post.objects.get(id__exact=comment.object_id)
    if post.is_draft:
        return
    # use templates for mail subject and body
    try:
        subject_tmp = loader.get_template("comment_subject.txt")
    except TemplateDoesNotExist:
        subject_tmp = Template(DEFAULT_COMMENT_SUBJECT)
    try:
        body_tmp = loader.get_template("comment_body.txt")
    except TemplateDoesNotExist:
        body_tmp = Template(DEFAULT_COMMENT_BODY)

    current_domain = Site.objects.get_current()
    site_url = '%s://%s' % (settings.SITE_PROTOCOL, current_domain)
    ctx = Context({'post': post, 'comment': comment, 'site_url': site_url})
    subject = subject_tmp.render(ctx).strip()
    body = body_tmp.render(ctx).strip()
    # send email to the user
    try:
        for user in get_users_to_send_email(post, comment):
	    if user.email:
        	user.email_user(subject, body)
    except UnicodeEncodeError:
        if not settings.DEBUG:
            mail_admins("Trouble while sending email", traceback.format_exc())
        else:
            raise


dispatcher.connect(send_comment_by_mail, sender=CommentNode, signal=signals.post_save)
