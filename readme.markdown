Simple Framework
================

This is a small framework I am working on to aid me in developing applications that run on the Google App Engine.

Unlike Django or web2py this framework was designed from the start specifically for the Google App Engine. No SQL abstraction layer, just `db.Model`. No users table, just `users.get_current_user()`

Setup
-----

1. Create a new GAE app
2. Add this project as a submodule
3. Point to this framework's main handler in your `app.yaml` file
4. Create controllers that subclass the Controller class in the framework's main handler
5. Place the controllers in a controllers directory in your project's base directory
6. The main handler will call restful actions (like Rails) on your controller and render them using Django templates in views in view/controller-name/action-name.html
7. The controller's instance variables are available to the view

The plan
--------
* Write generator script to help creating controllers and views
* Better authorization (@authorize)
* Add search support (Bill Katz?)
* Django 1.0 templates, perhaps also view helpers
