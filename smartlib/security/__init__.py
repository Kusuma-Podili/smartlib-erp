"""Identity, Security, Access Control, and Privacy Package.

Implements TOTP 2FA (RFC 6238), SAML 2.0 Web SSO SP, OAuth2/OIDC token issuance,
Attribute-Based Access Control (ABAC) policy evaluation, and GDPR patron privacy retention.
"""
from .totp import TotpEngine, HotpEngine
from .saml import SamlServiceProvider, SamlAuthnRequest
from .oauth2 import OAuth2TokenIssuer, JwtPayload
from .abac import AbacPolicyEngine, AbacRequest, AbacDecision, Role
from .privacy import PatronPrivacyEngine, RetentionPolicy
