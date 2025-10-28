"""
OAuth2 Client Credentials Manager - Auto-refresh tokens
"""
import asyncio
import logging
import time
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

@dataclass
class OAuth2Token:
    access_token: str
    expires_at: float  # Unix timestamp
    token_type: str = "Bearer"
    scope: str | None = None

class OAuth2Manager:
    def __init__(self):
        self.tokens: dict[str, OAuth2Token] = {}
        self.locks: dict[str, asyncio.Lock] = {}
        self.client = httpx.AsyncClient()

    async def close(self):
        await self.client.aclose()

    async def get_token(
        self,
        provider_key: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: str | None = None,
        extra_params: dict | None = None
    ) -> str:
        """
        Get valid access token, refreshing if necessary

        Args:
            provider_key: Unique identifier for this OAuth2 provider
            token_url: Token endpoint URL
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            scope: Optional scope string
            extra_params: Additional parameters for token request
        """
        # Get or create lock for this provider
        if provider_key not in self.locks:
            self.locks[provider_key] = asyncio.Lock()

        async with self.locks[provider_key]:
            # Check if we have a valid token
            if provider_key in self.tokens:
                token = self.tokens[provider_key]
                # Add 60s buffer before expiration
                if time.time() < (token.expires_at - 60):
                    return token.access_token

            # Need to fetch new token
            logger.info(f"Fetching new OAuth2 token for {provider_key}")
            token = await self._fetch_token(
                token_url, client_id, client_secret, scope, extra_params
            )
            self.tokens[provider_key] = token
            return token.access_token

    async def _fetch_token(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: str | None = None,
        extra_params: dict | None = None
    ) -> OAuth2Token:
        """Fetch new access token from provider"""
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if scope:
            data["scope"] = scope
        if extra_params:
            data.update(extra_params)

        try:
            resp = await self.client.post(token_url, data=data)
            resp.raise_for_status()
            token_data = resp.json()

            # Calculate expiration time
            expires_in = token_data.get("expires_in", 3600)
            expires_at = time.time() + expires_in

            return OAuth2Token(
                access_token=token_data["access_token"],
                expires_at=expires_at,
                token_type=token_data.get("token_type", "Bearer"),
                scope=token_data.get("scope")
            )
        except Exception as e:
            logger.error(f"Failed to fetch OAuth2 token: {e}")
            raise

    def invalidate_token(self, provider_key: str):
        """Force token refresh on next request"""
        self.tokens.pop(provider_key, None)

# Global manager instance
_oauth2_manager: OAuth2Manager | None = None

def get_oauth2_manager() -> OAuth2Manager:
    global _oauth2_manager
    if _oauth2_manager is None:
        _oauth2_manager = OAuth2Manager()
    return _oauth2_manager

async def close_oauth2_manager():
    global _oauth2_manager
    if _oauth2_manager:
        await _oauth2_manager.close()


