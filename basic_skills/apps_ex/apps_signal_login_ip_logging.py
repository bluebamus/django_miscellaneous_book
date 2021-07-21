from django.apps import AppConfig


class BasicSkillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basic_skills"

    def ready(self):
        import basic_skills.tasks.signal_login_ip_logging
