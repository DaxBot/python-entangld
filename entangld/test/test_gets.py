import unittest
import asyncio

from .helpers import block_until

from .. import entangld


class LocalGetExamples(unittest.TestCase):

    def setUp(self):
        self.store = entangld.Entangld()
        self.store.set("some_data",0.0)

        async def get_later():
            await asyncio.sleep(0.01)
            return 1
        async def get_async():
            return 1
        def get_now():
            return 1
        self.store.set("later",get_later)
        self.store.set("async",get_async)
        self.store.set("now",get_now)

    def tearDown(self):
        self.store.subscriptions = []
        del self.store

    def test_simple_get(self):
        """Get data locally
        """
        self.assertEqual(0.0,block_until(self.store.get("some_data")))

    def test_get_function(self):
        """Get data from a function
        """
        self.assertEqual(1,block_until(self.store.get("now")))

    def test_get_async_function(self):
        """Get data from an async function
        """
        self.assertEqual(1,block_until(self.store.get("async")))

    def test_get_async_function_delay(self):
        """Get data from a delaying async function
        """
        self.assertEqual(1,block_until(self.store.get("later")))


class LocalSynchronousGetExamples(unittest.TestCase):

    def setUp(self):
        self.store = entangld.Entangld()
        self.store.set("some_data",0.0)

        async def get_later():
            await asyncio.sleep(0.01)
            return 1
        async def get_async():
            return 1
        def get_now():
            return 1
        self.store.set("later",get_later)
        self.store.set("async",get_async)
        self.store.set("now",get_now)

    def tearDown(self):
        self.store.subscriptions = []
        del self.store

    def test_simple_get(self):
        """Get data locally
        """
        self.assertEqual(0.0,self.store.get_sync("some_data"))

    def test_get_function(self):
        """Get data from a function
        """
        self.assertEqual(1,self.store.get_sync("now"))

    def test_get_async_function(self):
        """Get data from an async function
        """
        self.assertEqual(1,self.store.get_sync("async"))

    def test_get_async_function_delay(self):
        """Get data from a delaying async function
        """
        self.assertEqual(1,self.store.get_sync("later"))

class LocalGetExamples(unittest.TestCase):

    def setUp(self):
        self.store = entangld.Entangld()
        self.store.set("some_data",0.0)

        async def get_later():
            await asyncio.sleep(0.01)
            return 1
        async def get_async():
            return 1
        def get_now():
            return 1
        self.store.set("later",get_later)
        self.store.set("async",get_async)
        self.store.set("now",get_now)

    def tearDown(self):
        self.store.subscriptions = []
        del self.store

    def test_simple_get(self):
        """Get data locally
        """
        self.assertEqual(0.0,block_until(self.store.get("some_data")))

    def test_get_function(self):
        """Get data from a function
        """
        self.assertEqual(1,block_until(self.store.get("now")))

    def test_get_async_function(self):
        """Get data from an async function
        """
        self.assertEqual(1,block_until(self.store.get("async")))

    def test_get_async_function_delay(self):
        """Get data from a delaying async function
        """
        self.assertEqual(1,block_until(self.store.get("later")))


class RemoteGetExamples(unittest.TestCase):

    def setUp(self):
        self.store = entangld.Entangld()
        self.remote = entangld.Entangld()

        self.store.transmit(lambda msg, obj: obj.receive_sync(msg,self.store))
        self.remote.transmit(lambda msg, obj: obj.receive_sync(msg,self.remote))

        self.store.attach("other",self.remote)

        self.remote.set("some_data",0.0)

        async def get_later():
            await asyncio.sleep(0.01)
            return 1
        async def get_async():
            return 1
        def get_now():
            return 1
        self.remote.set("later",get_later)
        self.remote.set("async",get_async)
        self.remote.set("now",get_now)

    def tearDown(self):
        self.store.subscriptions = []
        self.remote.subscriptions = []
        del self.store
        del self.remote

    def test_simple_get(self):
        """Get data remote
        """
        self.assertEqual(0.0,block_until(self.store.get("other.some_data")))

    def test_get_function(self):
        """Get remote data from a function
        """
        self.assertEqual(1,block_until(self.store.get("other.now")))

    def test_get_async_function(self):
        """Get remote data from an async function
        """
        self.assertEqual(1,block_until(self.store.get("other.async")))

    def test_get_async_function_delay(self):
        """Get remote data from a delaying async function
        """
        self.assertEqual(1,block_until(self.store.get("other.later")))

if __name__ == "__main__":
    unittest.main()
