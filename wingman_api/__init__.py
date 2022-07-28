from .public import app

import wingman_api.controller.auth
wingman_api.controller.auth.init(app)

import wingman_api.controller.project
wingman_api.controller.project.init(app)

import wingman_api.controller.intent
wingman_api.controller.intent.init(app)

import wingman_api.controller.action
wingman_api.controller.action.init(app)

import wingman_api.controller.story
wingman_api.controller.story.init(app)