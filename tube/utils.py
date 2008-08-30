# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: utils.py 2 2008-03-07 20:33:17Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007 Guilherme Mesquita Gondim
#
#  This file is part of django-tube.
#
#  django-tube is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""django-tube utilities."""

import tube
import commands
import os
import sys
from django.conf import settings

def get_svn_revision():
    """
    Returns the SVN revision in the form SVN-XXX, where XXX is the
    revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.
    """
    try:
        from django.utils import version
        rev = version.get_svn_revision(tube.__path__[0])
    except ImportError:
        rev = u'SVN-unknown'
    return rev

def convertvideo (video):
    if video is None:
        return "Kein Video im Upload gefunden"
    filename = video.videoupload
    print "Konvertiere Quelldatei: %s" + filename
    if filename is None:
        return "Video mit unbekanntem Dateinamen"
    sourcefile = "%s%s" % (settings.MEDIA_ROOT,filename)
    flvfilename = "%s.flv" % video.id
    thumbnailfilename = "%svideos/flv/%s.png" % (settings.MEDIA_ROOT, video.id)
    targetfile = "%svideos/flv/%s" % (settings.MEDIA_ROOT, flvfilename)
    ffmpeg = "ffmpeg -i %s -acodec mp3 -ar 22050 -ab 32 -f flv -s 320x240 %s" % (sourcefile,  targetfile)
    grabimage = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320x240 %s " % (sourcefile, thumbnailfilename)
    flvtool = "flvtool2 -U %s" % targetfile
    print ("Source : %s" % sourcefile)
    print ("Target : %s" % targetfile)
    print ("FFMPEG: %s" % ffmpeg)
    print ("FLVTOOL: %s" % flvtool)
    try:
        ffmpegresult = commands.getoutput(ffmpeg)
        print "-------------------- FFMPEG ------------------"
        print ffmpegresult
        # Check if file exists and is > 0 Bytes
        try:
            s = os.stat(targetfile)
            print s
            fsize = s.st_size
            if (fsize == 0):
                print "File is 0 Bytes gross"
                os.remove(targetfile)
                return ffmpegresult
            print "Dateigroesse ist %i" % fsize
        except:
            print sys.exc_info()
            print "File %s scheint nicht zu existieren" % targetfile
            return ffmpegresult
        flvresult = commands.getoutput(flvtool)
        print "-------------------- FLVTOOL ------------------"
        print flvresult
        grab = commands.getoutput(grabimage)
        print "-------------------- GRAB IMAGE ------------------"
        print grab
    except:
        print sys.exc_info()
        return sys.exc_info[1]
    video.flvfilename = flvfilename
    video.save()
    return None
