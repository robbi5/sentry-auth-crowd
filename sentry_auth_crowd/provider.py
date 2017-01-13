# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django import forms
from django.shortcuts import render
from sentry.auth import Provider, AuthView

import crowd

from .constants import CROWD_URL, CROWD_APP_NAME, CROWD_APP_PASSWORD
from .constants import CROWD_DEFAULT_TEAM_SLUGS

class CrowdLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    provider = forms.CharField(widget=forms.HiddenInput(), required=False, initial="crowd")
    op = forms.CharField(widget=forms.HiddenInput(), required=False)


class AskUserAndPassword(AuthView):
    def dispatch(self, request, helper):
        # provider is needed, else we get an form in
        # error state after the first click "login with crowd"
        if request.method == 'POST' and request.POST.get('provider') is not None:
            form = CrowdLoginForm(request.POST)

            if form.is_valid():
                helper.bind_state('username', form.cleaned_data['username'])
                # we don't save the password here
                return helper.next_step()

        else:
            form = CrowdLoginForm(initial=request.POST)

        return render(request, 'sentry_auth_crowd/login.html', {'form': form})

class AuthAtCrowd(AuthView):
    _crowd = None

    def __init__(self, *args, **kwargs):
        super(AuthAtCrowd, self).__init__(*args, **kwargs)
        self._crowd = crowd.CrowdServer(CROWD_URL, CROWD_APP_NAME, CROWD_APP_PASSWORD)

    def dispatch(self, request, helper):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return helper.error('username / password missing')

        success = self._crowd.auth_user(username, password)
        if not success:
            return helper.error('auth failed')

        helper.bind_state('name', success['name'])
        helper.bind_state('email', success['email'])

        return helper.next_step()


class CrowdProvider(Provider):
    name = 'Crowd'

    def get_auth_pipeline(self):
        return [
            AskUserAndPassword(),
            AuthAtCrowd()
        ]

    def build_identity(self, state):
        return {
            'name': state['name'],
            'id': state['username'],
            'email': state['email']
        }

    def refresh_identity(self, auth_identity):
        pass

    def build_config(self, state):
        return {}
