# -*- coding: utf-8 -*-
# Copyright 2012-2013 Rooter Analysis S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tinymce.models import HTMLField

from moocng.courses.models import Course
from moocng.teacheradmin.managers import MassiveEmailManager
from moocng.teacheradmin.tasks import massmail_send_in_batches


class Invitation(models.Model):

    """
    Invitation data model.

    .. versionadded:: 0.1
    """
    host = models.ForeignKey(User, verbose_name=_(u'Host'), blank=False,
                             null=False)
    email = models.EmailField(verbose_name=_(u'Email'), blank=False,
                              null=False)
    course = models.ForeignKey(Course, verbose_name=_(u'Course'), blank=False,
                               null=False)
    datetime = models.DateTimeField(verbose_name=_(u'Date and time'),
                                    blank=False, null=False,
                                    auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')


class MassiveEmail(models.Model):

    """
    MassiveEmail data model.

    .. versionadded:: 0.1
    """
    course = models.ForeignKey(Course, verbose_name=_(u'Course'),
                               related_name='massive_emails', blank=False,
                               null=False)
    datetime = models.DateTimeField(verbose_name=_(u'Date and time'),
                                    blank=False, null=False,
                                    auto_now_add=True, editable=False)
    subject = models.CharField(verbose_name=_(u'Subject'), max_length=200,
                               blank=False, null=False)
    message = HTMLField(verbose_name=_(u'Content'))

    objects = MassiveEmailManager()

    class Meta:
        verbose_name = _(u'massive email')
        verbose_name_plural = _(u'massive emails')

    def send_in_batches(self, email_send_task):
        """
        Start the celery task that will start the batch assignment. Take in mind
        that we are sending the whole MassiveEmail object to the batches task.

        .. versionadded:: 0.1
        """
        massmail_send_in_batches.delay(self, email_send_task)
