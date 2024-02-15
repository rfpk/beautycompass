from django.core import signing
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.safestring import mark_safe


class CustomTokenGenerator(PasswordResetTokenGenerator):
    namespace = "token"

    def __init__(self, record=None):
        super(CustomTokenGenerator, self).__init__()
        self.record = record
        self.sign_key, self.secret = self.get_keys()

    @classmethod
    def get_keys(cls):
        key = settings.EMAIL_SECRET_KEY
        key_len = len(key)
        str1 = key[: key_len // 2]
        str2 = key[key_len // 2 :]
        return str1, str2

    def create_url(self, url, sign, token):
        return mark_safe(f"{settings.HOST}{url}?sign={sign}&token={token}")

    def dump_data(self, identifier, user):
        sign = signing.dumps({"id": identifier}, salt=self.namespace, key=self.sign_key)
        token = self.make_token(user)
        return sign, token

    def check_sign(self, sign):
        try:
            sign_data = signing.loads(
                sign,
                key=self.sign_key,
                salt=self.namespace,
                max_age=settings.EMAIL_TIMEOUT,
            )
            return sign_data
        except signing.BadSignature:
            return False


class RegistrationTokenGenerator(CustomTokenGenerator):
    namespace = "registration"

    def _make_hash_value(self, user, timestamp):
        return f"{self.record.pk}{timestamp}{self.record.count}{self.record.is_used}"


class PasswordResetTokenGenerator(CustomTokenGenerator):
    namespace = "password-reset"

    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return f"{self.record.pk}{user.password}{login_timestamp}{timestamp}{self.record.count}{self.record.is_used}"
