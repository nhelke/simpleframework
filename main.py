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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import framework

class RestfulHandler(webapp.RequestHandler):
  def handle_exception(self, exception, debug_mode):
    """Better handles various exceptions and sets a more appropriate HTTP status."""
    if isinstance(exception, framework.Redirect):
      self.redirect(exception.url, exception.permanent)
    elif isinstance(exception, framework.HTTPError) and not debug_mode:
      self.error(exception.error_code)
    elif isinstance(exception, ImportError) and not debug_mode:
      self.error(404)
    else:
      super(RestfulHandler, self).handle_exception(exception, debug_mode)
  
  def render(self, controller_name, action_name, *args):
    """This method starts the controller with the right action and the renders the right
    template with a dict of the data values of the controller.
    If the action new and there is no new template, the edit template is rendered instead. This
    enables simple mapping of new and create to edit and update respectfully in the
    controller"""
    from google.appengine.ext.webapp import template
    controller_path = "controllers.%s" % controller_name.lower()
    __import__(controller_path)
    import sys
    self.controller = getattr(sys.modules[controller_path],
                              controller_name.title())(self.request)
    getattr(self.controller, action_name)(*args)
    # TODO Detect if the app is running in debug mode and render view in debug as well
    self.response.out.write( \
        template.render("../views/%s/%s.html" % (controller_name, action_name),
        self.controller.__dict__))

class CollectionHandler(RestfulHandler):
  def get(self, controller):
    if "new" in self.request.arguments():
      # For the purposes of bad web browsers ?new renders the edit form.
      self.render(controller, "new")
    else:
      self.render(controller, "index")
  def post(self, controller):
    """Create new object"""
    self.render(controller, "create")

class MemberHandler(RestfulHandler):
  def get(self, controller, keyname):
    """Read object"""
    self.render(controller, "show")
  def post(self, controller, keyname):
    """Legacy update to support HTML <5"""
    import re
    if "action" in self.request.arguments() and re.match("(update|destroy)$",
                                                                  self.request.get("action")):
      self.render(controller, self.request.get("action"))
    else:
      raise webapp.Error("Bad request, action parameter wrong/missing.")
  def put(self, controller, keyname):
    """Update object"""
    self.render(controller, "update")
  def delete(self, controller, keyname):
    """Destroy object"""
    self.render(controller, "destroy")

def main():
  import os
  debug = os.environ["SERVER_SOFTWARE"].startswith("Development")
  application = webapp.WSGIApplication([
                                        ('/(.+)/(.+)/?', MemberHandler),
                                        ('/(.+)/?', CollectionHandler),
                                       ],
                                       debug=debug)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
