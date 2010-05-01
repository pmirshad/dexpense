#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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

import cgi
import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from datetime import datetime
from ExpenseModel import ExpenseModel

class MainHandler(webapp.RequestHandler):

  def get(self):
    logging.info('MainHandler.get()')

    user = users.get_current_user()

    if user:
      template_values = {
      'title': user.nickname(),
      }
      path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
      self.response.out.write(template.render(path, template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))

class AddExpense(webapp.RequestHandler):

  def post(self):
        user = users.get_current_user()

        if user:
          expName = cgi.escape(self.request.get('expName'))
          expType = cgi.escape(self.request.get('expType'))
          expDate = datetime.strptime(self.request.get('expDate'), '%d-%m-%Y')
          expOwner = users.get_current_user()

          logging.info('expName: ' + expName)
          logging.info('expType: ' + expType)
          logging.info('expDate: ' + expDate.strftime("%d/%m/%Y"))
          logging.info('expOwner: ' + expOwner.nickname())

          expense = ExpenseModel( name = expName
                                , type = expType
                                , date = expDate
                                , owner = expOwner )
          expense.put()


          template_values = {
              'title': 'Home',
          }
          path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
          self.response.out.write(template.render(path, template_values))
        else:
          self.redirect(users.create_login_url(self.request.uri))


def main():
  logging.getLogger().setLevel(logging.DEBUG)

  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/addexpense', AddExpense)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
