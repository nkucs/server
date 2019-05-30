from django.apps import AppConfig

# 用于解决登录时报错
class UserConfig(AppConfig):
    name = 'user'
    def ready(self):
        # 将更新最后一次登录时间的函数，与用户登录信号解绑
        super(UserConfig, self).ready()
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(dispatch_uid="update_last_login")
