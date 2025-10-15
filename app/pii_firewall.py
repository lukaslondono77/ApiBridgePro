"""
PII Firewall - Per-field redaction, tokenization, and encryption
"""
import base64
import hashlib
import os
import re
from enum import Enum
from typing import Any, Optional

from cryptography.fernet import Fernet


class PIIAction(str, Enum):
    REDACT = "redact"
    TOKENIZE = "tokenize"
    ENCRYPT = "encrypt"
    HASH = "hash"

class PIIFirewall:
    def __init__(self, encryption_key: Optional[str] = None):
        # Use provided key or generate one
        key_bytes = encryption_key.encode() if encryption_key else Fernet.generate_key()
        if len(key_bytes) != 44:  # Fernet key must be 44 bytes base64-encoded
            # Derive proper key from provided string
            key_bytes = base64.urlsafe_b64encode(hashlib.sha256(key_bytes).digest())
        self.cipher = Fernet(key_bytes)

        # Common PII patterns
        self.patterns = {
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),
            "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "ip_address": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
        }

    def redact(self, value: str, redaction_char: str = "*") -> str:
        """Replace the value with redaction characters"""
        if not value:
            return value
        # Keep first and last char for context
        if len(value) <= 2:
            return redaction_char * len(value)
        return value[0] + redaction_char * (len(value) - 2) + value[-1]

    def tokenize(self, value: str) -> str:
        """Create a consistent hash token for the value"""
        if not value:
            return value
        # Create deterministic token
        token = hashlib.sha256(value.encode()).hexdigest()[:16]
        return f"TOK_{token}"

    def encrypt(self, value: str) -> str:
        """Encrypt the value (reversible)"""
        if not value:
            return value
        encrypted = self.cipher.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt an encrypted value"""
        if not encrypted_value:
            return encrypted_value
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception:
            return encrypted_value  # Return as-is if decryption fails

    def hash_value(self, value: str) -> str:
        """One-way hash of the value"""
        if not value:
            return value
        hashed = hashlib.sha256(value.encode()).hexdigest()
        return f"HASH_{hashed[:16]}"

    def apply_action(self, value: Any, action: PIIAction) -> Any:
        """Apply PII action to a value"""
        if not isinstance(value, str):
            return value

        if action == PIIAction.REDACT:
            return self.redact(value)
        elif action == PIIAction.TOKENIZE:
            return self.tokenize(value)
        elif action == PIIAction.ENCRYPT:
            return self.encrypt(value)
        elif action == PIIAction.HASH:
            return self.hash_value(value)
        return value

    def scan_and_protect_patterns(self, text: str, action: PIIAction = PIIAction.REDACT) -> str:
        """Scan text for common PII patterns and protect them"""
        if not isinstance(text, str):
            return text

        result = text
        for pattern_name, pattern in self.patterns.items():
            matches = pattern.finditer(result)
            for match in matches:
                original = match.group(0)
                protected = self.apply_action(original, action)
                result = result.replace(original, protected, 1)
        return result

    def process_dict(self, data: dict[str, Any], field_rules: dict[str, PIIAction]) -> dict[str, Any]:
        """
        Process a dictionary applying PII rules to specific fields

        Args:
            data: Dictionary to process
            field_rules: Mapping of field paths to PII actions
                        e.g., {"user.email": PIIAction.ENCRYPT, "ssn": PIIAction.REDACT}
        """
        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            # Check if this field has a rule
            if key in field_rules:
                result[key] = self.apply_action(value, field_rules[key])
            elif isinstance(value, dict):
                # Recursively process nested dicts
                nested_rules = {
                    k.split('.', 1)[1]: v
                    for k, v in field_rules.items()
                    if k.startswith(f"{key}.") and '.' in k
                }
                result[key] = self.process_dict(value, nested_rules)
            elif isinstance(value, list):
                result[key] = [
                    self.process_dict(item, field_rules) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value

        return result

    def auto_scan(self, data: Any, action: PIIAction = PIIAction.REDACT) -> Any:
        """
        Automatically scan and protect PII patterns in any data structure
        """
        if isinstance(data, str):
            return self.scan_and_protect_patterns(data, action)
        elif isinstance(data, dict):
            return {k: self.auto_scan(v, action) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.auto_scan(item, action) for item in data]
        return data


# Global instance (can be configured via environment)
_firewall: Optional[PIIFirewall] = None

def get_firewall() -> PIIFirewall:
    global _firewall
    if _firewall is None:
        encryption_key = os.getenv("PII_ENCRYPTION_KEY")
        _firewall = PIIFirewall(encryption_key)
    return _firewall


