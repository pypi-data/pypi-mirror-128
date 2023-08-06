"""Declares :class:`RedisCache`."""
import aioredis

from .base import BaseCache


class RedisCache(BaseCache):

    @property
    def dsn(self):
        """Return the Data Source Name (DNS) for the Redis
        connection.
        """
        dsn = f'redis://{self.opts.host}:{self.opts.port}'
        if self.opts.get('database'):
            dsn = f'{dsn}/{self.opts.database}?'
        return dsn

    @BaseCache.needs_connection
    async def delete(self, name, version=None):
        """Delete a key from the cache."""
        return await self._impl.delete(self.abskey(name, version))

    @BaseCache.needs_connection
    async def get(self, name, version=None, decoder=None):
        """Get a key from the cache."""
        return await self._impl.get(self.abskey(name, version))

    @BaseCache.needs_connection
    async def set(self, name, value, version=None, expires=None):
        """Set a key in the cache."""
        await self._impl.set(
            self.abskey(name, version),
            value,
            px=expires
        )

    async def connect(self):
        """Connect to the Redis service."""
        assert self._impl is None # nosec
        self._pool = aioredis.ConnectionPool.from_url(
            self.dsn, decode_responses=False
        )
        self._impl = aioredis.Redis(connection_pool=self._pool)

    async def join(self):
        """Waits until the connection is closed."""
        await self._pool.disconnect()

    def close(self):
        """Closes the connection with the cache server."""
        pass
