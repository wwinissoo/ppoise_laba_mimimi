import hashlib
import hmac
import secrets
import string

from fitness.exceptions import WeakPasswordError
from fitness.validation import ensure_count


class PasswordPolicy:
    """Правила сложности пароля и хэширование с солью."""

    HASH_ITERATIONS = 100_000
    SALT_BYTES = 16
    SPECIAL_CHARACTERS = set(string.punctuation)

    def __init__(self, min_length=8, require_digit=True, require_uppercase=True, require_special=False):
        self._min_length = ensure_count(min_length, "минимальная длина", minimum=1)
        self._require_digit = bool(require_digit)
        self._require_uppercase = bool(require_uppercase)
        self._require_special = bool(require_special)

    @property
    def min_length(self):
        return self._min_length

    @property
    def require_digit(self):
        return self._require_digit

    @property
    def require_uppercase(self):
        return self._require_uppercase

    @property
    def require_special(self):
        return self._require_special

    def find_violations(self, raw_password):
        """Список нарушенных правил (пустой — пароль подходит)."""
        if not isinstance(raw_password, str):
            return ["пароль должен быть строкой"]
        rules = (
            (len(raw_password) >= self._min_length, f"длина не меньше {self._min_length}"),
            (not self._require_digit or any(c.isdigit() for c in raw_password), "хотя бы одна цифра"),
            (not self._require_uppercase or any(c.isupper() for c in raw_password), "хотя бы одна заглавная буква"),
            (not self._require_special or any(c in self.SPECIAL_CHARACTERS for c in raw_password), "спецсимвол"),
        )
        return [message for satisfied, message in rules if not satisfied]

    def validate(self, raw_password):
        violations = self.find_violations(raw_password)
        if violations:
            raise WeakPasswordError("Пароль слишком простой: " + "; ".join(violations))
        return raw_password

    def strength_score(self, raw_password):
        """Оценка надёжности от 0 до 5."""
        if not isinstance(raw_password, str) or not raw_password:
            return 0
        checks = (
            len(raw_password) >= self._min_length,
            len(raw_password) >= 2 * self._min_length,
            any(c.isdigit() for c in raw_password),
            any(c.isupper() for c in raw_password) and any(c.islower() for c in raw_password),
            any(c in self.SPECIAL_CHARACTERS for c in raw_password),
        )
        return sum(checks)

    @classmethod
    def generate_salt(cls):
        return secrets.token_hex(cls.SALT_BYTES)

    @classmethod
    def hash_password(cls, raw_password, salt):
        digest = hashlib.pbkdf2_hmac("sha256", raw_password.encode(), salt.encode(), cls.HASH_ITERATIONS)
        return digest.hex()

    @classmethod
    def matches(cls, raw_password, salt, expected_hash):
        if not isinstance(raw_password, str):
            return False
        return hmac.compare_digest(cls.hash_password(raw_password, salt), expected_hash)
