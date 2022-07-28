from .public import app

import wingman_api.controller.auth
wingman_api.controller.auth.init(app)

import wingman_api.controller.projects
wingman_api.controller.projects.init(app)

import wingman_api.controller.intents
wingman_api.controller.intents.init(app)

import wingman_api.controller.actions
wingman_api.controller.actions.init(app)