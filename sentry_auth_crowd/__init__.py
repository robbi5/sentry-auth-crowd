# -*- coding: utf-8 -*-
from __future__ import absolute_import

from sentry.auth import register
from .provider import CrowdProvider

register('crowd', CrowdProvider)
