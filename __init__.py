#!/usr/bin/env python
#
# Copyright 2010 Nicholas Helke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

class HTTPError(Exception):
  """This is the base class for Exceptions that are caught by the RestfulHandler and
  converted to appropriate HTTP errors."""
  def __init__(self, code, *args):
    super(HTTPError, self).__init__(*args)
    self.error_code = code

class Redirect(Exception):
  """Raising this exception from a controller with the correct argument(s) performs
   a HTTP 302/303 redirect."""
  def __init__(self, url, permanent=False):
    super(Redirect, self).__init__()
    self.url = url
    self.permanent = permanent

class Controller(object):
  """This is the Controller class that all controller should inherit from."""
  def __init__(self, request):
    super(Controller, self).__init__()
    self._request = request

  def index(self):
    pass
  def show(self):
    pass
  def new(self):
    pass
  def create(self):
    pass
  def edit(self):
    pass
  def update(self):
    pass
  def destory(self):
    pass

  def authorize(self, authorized_emails, logout_url="/"):
    from google.appengine.api import users
    current_user = users.get_current_user()
    if current_user:
      if users.is_current_user_admin() or current_user.email() in authorized_emails:
        self.logout_url = users.create_logout_url(logout_url)
        return True
      else:
        raise HTTPError(403, current_user.email())
    else:
      raise Redirect(users.create_login_url(self._request.url))
