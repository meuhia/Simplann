# encoding: utf-8

import django
from django.conf import settings
import sys

from git.repo import Repo

def git_version(request):
    """Return the current git version.

    """
    try:
        repo = Repo(settings.SITE_ROOT)
        v = repo.head.commit.hexsha
        br = repo.active_branch.name
    
        return {
            'git_version': br+'-'+v[:5]
        }
    except:
        return {
            'git_version': None
        }
