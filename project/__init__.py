from .public import app

import project.controller.auth
project.controller.auth.init(app)

import project.controller.projects
project.controller.projects.init(app)

import project.controller.intents
project.controller.intents.init(app)

import project.controller.actions
project.controller.actions.init(app)