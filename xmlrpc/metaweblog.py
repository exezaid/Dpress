#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright  2008 Alberto Paro <alberto@ingparo.it>

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from datetime import datetime
from time import strptime, mktime
import re
import os

from blog.models import Post
from django.conf import settings
from xmlrpclib import *
import urlparse
from utils import signature
from tagging.models import Tag

def full_url(url):
    return urlparse.urljoin(settings.SITE_URL, url)


def auth_user(username, password):
    try:
        u = User.objects.get(username = username)
        return u.check_password(password)        
    except User.DoesNotExist:
        return False
            
def datetime_from_iso(isostring):
    return datetime.datetime.fromtimestamp(mktime(strptime(isostring, '%Y%m%dT%H:%M:%SZ')))
    
def blogentry_to_mtentry(post, username):
    return {'userid': username,
            'dateCreated': DateTime(post.date.isoformat()),
            'postid': str(post.id),
            'description': post.text,
            'title': post.name,
            'link': post.get_absolute_url(),
            'permalink': post.get_absolute_url(),
            'mt_allow_comments': int(post.enable_comments),
            'mt_keywords': post.tags.split()}

###
### Blogger API
###

@signature(list, str, str, str)
def blogger_getUsersBlogs(request, appkey, username, password):
    """
    Get all user blogs.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * appkey string (application key)
    * utente string (user name)
    * password string (user password)
    
    Return value
    ~~~~~~~~~~~~
    * an array of <struct>'s containing the ID (blogid), name (blogName), and URL (url) of each blog.
    """
    if not auth_user(username, password):
        raise Fault(-1, "Authentication Failure")
    site = Site.objects.get_current()
    return [{'url': 'http://%s/' % site.domain,
             'blogid': settings.BLOG_NAME,#settings.SITE_ID
             'blogName': settings.BLOG_NAME},]

@signature(bool, str, str, str, int, bool)
def blogger_deletePost(request, appkey, postid, username, password, publish):
    """
    Delete a post.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * appkey string (application key)
    * postid integer (id of post)
    * username string (user name)
    * password string (user password)
    * publish bool (user password)
    
    Return value
    ~~~~~~~~~~~~
    * a boolean.
    """
    if not auth_user(username, password):
        raise Fault(-1, "Authentication Failure")
    
    try:
        b = Post.objects.get(pk = postid)
        b.is_draft = True
        b.save()
        return Boolean(True)
    except Post.DoesNotExist:
        raise Fault(-2, "Post does not exist")
    except Exception, e:
        raise Fault(-255, "Failed to create new post: %s" % str(e))


@signature(list, str, str, str)
def metaWeblog_getCategories(request, username, password, blogid):
    """
    The struct returned contains one struct for each category, containing 
    the following elements: description, htmlUrl and rssUrl.
    This entry-point allows editing tools to offer category-routing as a feature.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * username string (user name)
    * password string (user password)
    * blogid string (id of blof)
    
    Return value
    ~~~~~~~~~~~~
    * a list.
    """
    tags = Tag.objects.all()
    return [tag.name for tag in tags]

# example... this is what wordpress returns:
# {'permaLink': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'description': 'Welcome to <a href="http://wordpress.com/">Wordpress.com</a>. This is your first post. Edit or delete it and start blogging!',
#  'title': 'Hello world!',
#  'mt_excerpt': '',
#  'userid': '217209',
#  'dateCreated': <DateTime u'20060509T16:24:39' at 2c7580>,
#  'link': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'mt_text_more': '',
#  'mt_allow_comments': 1,
#  'postid': '1',
#  'categories': ['Uncategorized'],
#  'mt_allow_pings': 1}

def format_date(d):
    if not d: return None
    return DateTime(d.isoformat())

def post_struct(post):
    link = full_url(post.get_absolute_url())
    #TO improve tagging
    categories = post.tags.split()
    struct = {
        'postid': post.id,
        'title': post.name,
        'link': link,
        'permaLink': link,
        'description': post.text,
        'categories': categories,
        'userid': post.author.id,
        # 'mt_excerpt': '',
        # 'mt_text_more': '',
        # 'mt_allow_comments': 1,
        # 'mt_allow_pings': 1}
        }
    if post.date:
        struct['dateCreated'] = format_date(post.date)
    return struct

def setTags(post, struct):
    tags = struct.get('categories', None)
    if tags is None:
        post.tags = []
    else:
        post.tags = [Tag.objects.get(name__iexact=name) for name in tags]
    
###
### MetaWeblog API
###

@signature(string, str, str, int, dict, bool)
def metaWeblog_newPost(request, blogid, username, password, content, publish):
    """
    Creating a new post.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * username string (user name)
    * password string (user password)
    * blogid string (id of blog)
    * content dict (content of blog)
    * publish boolean (publish this post?)
    
    Return value
    ~~~~~~~~~~~~
    * a struct.
    """

    if not auth_user(username, password):
        return Fault(-1, "Authentication Failure")
        
    try:
        u = User.objects.get(username = username)
        post = Post(name = content['title'],
                      text = content['description'],
                      date = content['dateCreated'],
                      author = u,
                      is_draft = not bool(publish))
                      
        if content.has_key('mt_allow_comments'):
            post.enable_comments = bool(content['mt_allow_comments'])
        if content.has_key('mt_pingable'):
            pass # TODO
        if content.has_key('mt_convert_breaks'):
            pass # TODO
        if content.has_key('mt_keywords'):
            post.tags = content['mt_keywords']
    except User.DoesNotExist:
        raise Fault(-1, "Authentication Failure")
    except Exception, e:
        import traceback
        traceback.print_exc()
        raise Fault(-255, 'Unknown Error: %s' % str(e))
    
    try:
        post.save()
        return str(post.id)
    except Exception, e:
        raise Fault(-255, "Failed to create new post: %s" % str(e))

    
@signature(string, int, str, str, dict, bool)
def metaWeblog_editPost(request, postid, username, password, content, publish):
    """
    Edit a new post.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid integer (id of post)
    * username string (user name)
    * password string (user password)
    * content dict (content of blog)
    * publish boolean (publish this post?)
    
    Return value
    ~~~~~~~~~~~~
    * a string id of a post.
    """
    if not auth_user(username, password):
        raise Fault(-1, "Authentication Failure")
    
    try:
        post = Post.objects.get(id=postid)
        post.name = content['title']
        post.text = content['description']
        post.date = datetime_from_iso(str(content['dateCreated']))
        post.is_draft = not bool(publish)
        if content.has_key('mt_allow_comments'):
            post.enable_comments = bool(content['mt_allow_comments'])
        if content.has_key('mt_pingable'):
            pass # TODO
        if content.has_key('mt_keywords'):
            post.tags = content['mt_keywords']
        post.save()
        return str(post.id)                    
    except Post.DoesNotExist:
        raise Fault(-2, "Post does not exist")
    except Exception, e:
        raise Fault(-255, "Failed to create new post: %s" % str(e))
                
@signature(dict, int, str, int)
def metaWeblog_getPost(request, postid, username, password):
    """
    Get a post.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid integer (id of post)
    * username string (user name)
    * password string (user password)
    
    Return value
    ~~~~~~~~~~~~
    * a struct.
    """
    if not auth_user(username, password):
        return Fault(-1, "Authentication Failure")
    
    try:
        post = Post.objects.get(pk = int(postid))
        return blogentry_to_mtentry(post, username)
    except Post.DoesNotExist:
        raise Fault(-2, "Post does not exist")
    except Exception, e:
        import traceback
        traceback.print_exc()
        raise Fault(-255, 'Unknown Exception: %s' % str(e))
    
@signature(list, str, str, str, int)
def metaWeblog_getRecentPosts(request, blogid, username, password, numberOfPosts):
    """
    Get a lot of recent posts.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * blogid string (id of blog)
    * username string (user name)
    * password string (user password)
    * numberOfPosts integer (number of post)
    
    Return value
    ~~~~~~~~~~~~
    * a list of structs.
    """
    if not auth_user:
        return Fault(-1, "Authentication Failure")
        
    try:
        posts = Post.objects.order_by('-date')[:numberOfPosts]
        return [blogentry_to_mtentry(p, username) for p in posts]
    except Exception, e:
        raise Fault(-255, 'Unknown Exception: %s' % str(e))

@signature(dict, str, str, str, dict)
def metaWeblog_newMediaObject(request, blogid, username, password, fileObject):
    """
    Create a new media object.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * blogid string (id of blog)
    * username string (user name)
    * password string (user password)
    * fileObject struct (fileobject)
    
    Return value
    ~~~~~~~~~~~~
    * a string.
    """
    # The input struct must contain at least three elements, name,
    # type and bits. returns struct, which must contain at least one
    # element, url
    if not auth_user:
        raise Fault(-1, "Authentication Failure")

    file_data = str(fileObject['bits'])
    file_name = str(fileObject['name'])
    dated_path = datetime.datetime.now().strftime('%Y_%m_%d_') + os.path.basename(file_name)
    relative_path = os.path.join('upload', dated_path)
    target_path = os.path.abspath(os.path.join(settings.STATIC_ROOT, relative_path))
    target_url = os.path.abspath(settings.STATIC_ROOT, relative_path)
    open(target_path, 'w').write(file_data)
    return target_url
    
###
### MovableTypeAPI 
###

@signature(list, str, str, str, int)
def mt_getRecentPostTitles(request, blogid, username, password, numberOfPosts):
    """
    Get list of recent titles.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * blogid string (id of blof)
    * username string (user name)
    * password string (user password)
    * numberOfPosts integer (number of post)
    
    Return value
    ~~~~~~~~~~~~
    * a list of struct.
    """
    if not auth_user:
        raise Fault(-1, "Authentication Failure")
        
    try:
        posts = Post.objects.order_by('-date')[:numberOfPosts]
        return [p.name for p in posts]
    except Exception, e:
        raise Fault(-255, 'Unknown Exception: %s' % str(e))
    
@signature(list, str, str, str)
def mt_getCategoryList(request, blogid, username, password):
    """
    Get list of categories.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * blogid string (id of blof)
    * username string (user name)
    * password string (user password)
    
    Return value
    ~~~~~~~~~~~~
    * a list of struct.
    """
    if not auth_user(username, password):
        raise Fault(-1, 'Authentication Failure')
        
    return [{'categoryId':t.name, 'categoryName':t.name} \
                for t in Tag.objects.all()]
    
@signature(list, str, str, str)
def mt_getPostCategories(request, postid, username, password):
    """
    Get list of recent titles.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid int (id of post)
    * username string (user name)
    * password string (user password)
    
    Return value
    ~~~~~~~~~~~~
    * a list of struct.
    """
    if not auth_user(username, password):
        raise Fault(-1, 'Authentication Failure')

    try:
        post = Post.objects.get(pk = postid)
        return [{'categoryId':t, 'categoryName':t} \
                    for t in post.tags.split()]
    except Exception, e:
        raise Fault(-255, 'Unknown Exception: %s' % str(e))
        
@signature(bool, str, str, str, list)
def mt_setPostCategories(request, postid, username, password, categories):
    """
    Set the post categories.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid int (id of post)
    * username string (user name)
    * password string (user password)
    * categories list (list of categories)
    
    Return value
    ~~~~~~~~~~~~
    * a boolean.
    """
    if not auth_user(username, password):
        raise Fault(-1, 'Authentication Failure')
    
    return Boolean(True)
    #return Fault(-3, 'Not Implemented')
    
@signature(list)
def mt_supportedMethods(request):
    """
    Supported methods.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    
    Return value
    ~~~~~~~~~~~~
    * a list.
    """
    return []

@signature(list)
def mt_supportedTextFilters(request):
    """
    Supported TextFilters.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    
    Return value
    ~~~~~~~~~~~~
    * a list.
    """
    return []
        
@signature(list)
def mt_getTrackbackPings(request, postid):
    """
    Get TrackbackPings.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid int (id of post)
    
    Return value
    ~~~~~~~~~~~~
    * a list.
    """
    return []
        
@signature(list, str, str, str)
def mt_publishPost(request, postid, username, password):
    """
    Publish a post.
    
    Arguments
    ~~~~~~~~~
    * request object (request)
    * postid int (id of post)
    * username string (user name)
    * password string (user password)
    
    Return value
    ~~~~~~~~~~~~
    * a boolean.
    """
    if not auth_user(username, password):
        raise Fault(-1, 'Authentication Failure')
        
    try:
        b = Post.objects.get(pk = postid)
        b.is_draft = False
        b.save()
        return Boolean(True)
    except Post.DoesNotExist:
        raise Fault(-2, 'Blog entry not found')
    except Exception, e:
        raise Fault(-255, 'Unknown Error: %s' % str(s))
        
