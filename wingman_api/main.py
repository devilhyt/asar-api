from .public import app
import wingman_api.controller.auth
import wingman_api.controller.project
import wingman_api.controller.intent
import wingman_api.controller.action
import wingman_api.controller.story

wingman_api.controller.auth.init(app)
wingman_api.controller.project.init(app)
wingman_api.controller.intent.init(app)
wingman_api.controller.action.init(app)
wingman_api.controller.story.init(app)
