import unittest
import asyncio
import time

from .helpers import block_until


from .. import entangld


class LocalSubscriptionExamples(unittest.TestCase):

    def setUp(self):
        self.store = entangld.Entangld()


    def tearDown(self):
        self.store.subscriptions = []
        del self.store


    def test_subscribe_triggers_callback(self):
        """Subscriptions actually trigger callbacks
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        self.store.subscribe("some_data",inc)
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count,1)

    def test_subscribe_triggers_callback_multiple(self):
        """Subscriptions actually trigger callbacks for mutliple events
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        self.store.subscribe("some_data",inc)
        self.store.set("some_data", 0.0)
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count,2)

    def test_subscribe_triggers_async_callback(self):
        """Subscriptions actually trigger callbacks
        """
        self.count = 0
        async def inc(path, value):
            self.count += 1
        self.store.subscribe("some_data",inc)
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count,1)

    def test_unsubscribe(self):
        """Subscriptions actually cancelled
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        self.store.subscribe("some_data",inc)
        self.store.unsubscribe("some_data")
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count,0)


    def test_unsubscribe_all_from_path(self):
        """All subscriptions actually cancelled from paths
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("some_data",inc1)
        uuid2 = self.store.subscribe("some_data",inc2)
        self.store.unsubscribe("some_data")
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count1,0)
        self.assertEqual(self.count2,0)


    def test_unsubscribe_only_one(self):
        """Only the specific subscription gets cancelled
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("some_data",inc1)
        uuid2 = self.store.subscribe("some_data",inc2)
        self.store.unsubscribe(uuid1)
        self.store.set("some_data", 0.0)
        self.assertEqual(self.count1,0)
        self.assertEqual(self.count2,1)


class RemoteSubscriptionExamples(unittest.TestCase):

    def setUp(self):

        self.store = entangld.Entangld()
        self.remote1 = entangld.Entangld()
        self.remote2 = entangld.Entangld()

        self.store.transmit(lambda msg, obj: obj.receive_sync(msg,self.store))
        self.remote1.transmit(lambda msg, obj: obj.receive_sync(msg,self.remote1))
        self.remote2.transmit(lambda msg, obj: obj.receive_sync(msg,self.remote2))

        self.store.attach("other1",self.remote1)
        self.store.attach("other2",self.remote2)
        self.remote1.attach("other2",self.remote2)


    def tearDown(self):
        self.store.subscriptions = []
        self.remote1.subscriptions = []
        self.remote2.subscriptions = []
        del self.store
        del self.remote1
        del self.remote2


    def test_subscribe_triggers_callback(self):
        """Subscriptions actually trigger callbacks
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        uuid1 = self.store.subscribe("other2.some_data",inc)
        # self.assertEqual(len(self.store.subscriptions),1)
        # self.assertEqual(self.store.subscriptions[0].uuid,uuid1)
        # self.assertEqual(self.remote2.subscriptions[0].uuid,uuid1)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count,1)

    def test_subscribe_triggers_callback_multiple(self):
        """Subscriptions actually trigger callbacks for mutliple events
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        self.store.subscribe("other2.some_data",inc)
        self.remote2.set("some_data", 0.0)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count,2)

    def test_subscribes_multiple_stores_correct_callbacks(self):
        """Subscriptions from multiple stores to the same path get the correct
        number of callbacks
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("other2.some_data",inc1)
        uuid2 = self.remote1.subscribe("other2.some_data",inc2)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count1,1)
        self.assertEqual(self.count2,1)

    def test_subscribe_triggers_async_callback(self):
        """Subscriptions actually trigger callbacks (async)
        """
        self.count = 0
        async def inc(path, value):
            self.count += 1
        self.store.subscribe("other2.some_data",inc)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count,1)

    def test_subscribe_triggers_callback_across_multiple_stores(self):
        """Subscriptions actually trigger callbacks across multiple stores
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        uuid1 = self.store.subscribe("other1.other2.some_data",inc)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count,1)

    def test_unsubscribe(self):
        """Subscriptions actually cancelled
        """
        self.count = 0
        def inc(path, value):
            self.count += 1
        self.store.subscribe("other2.some_data",inc)
        self.store.unsubscribe("other2.some_data")
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count,0)


    def test_unsubscribe_all_from_path(self):
        """All subscriptions actually cancelled from paths
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("other2.some_data",inc1)
        uuid2 = self.store.subscribe("other2.some_data",inc2)
        self.store.unsubscribe("other2.some_data")
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count1,0)
        self.assertEqual(self.count2,0)


    def test_unsubscribe_only_one(self):
        """Only the specific subscription gets cancelled
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("other2.some_data",inc1)
        uuid2 = self.store.subscribe("other2.some_data",inc2)
        self.store.unsubscribe(uuid1)
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count1,0)
        self.assertEqual(self.count2,1)

    def test_unsubscribe_correct_store_from_path(self):
        """Only unsubscribe the correct store from a path
        """
        self.count1 = 0
        def inc1(path, value):
            self.count1 += 1
        self.count2 = 0
        def inc2(path, value):
            self.count2 += 1
        uuid1 = self.store.subscribe("other2.some_data",inc1)
        uuid2 = self.remote1.subscribe("other2.some_data",inc2)
        self.store.unsubscribe("other2.some_data")
        self.remote2.set("some_data", 0.0)
        self.assertEqual(self.count1,0)
        self.assertEqual(self.count2,1)

    def test_orphaned_subscriptions(self):
        """Orphaned subscriptions get cleaned
        """
        self.num_cancel = 0
        def trans_store(msg, obj):
            # print(msg)
            if msg.type == "unsubscribe":
                self.num_cancel += 1
            obj.receive_sync(msg, self.store)
        self.store.transmit(trans_store)

        self.num_events = 0
        def trans_remote2(msg, obj):
            if msg.type == "event":
                self.num_events += 1
            obj.receive_sync(msg, self.remote2)
        self.remote2.transmit(trans_remote2)

        uuid1 = self.store.subscribe("other2.some_data",lambda p,v: None)
        # orphase the pass through subscription on remote2
        self.store.subscriptions = []

        self.remote2.set("some_data", 0.0)

        self.assertEqual(self.num_cancel,1)
        self.assertEqual(self.num_events,1)

        self.remote2.set("some_data", 0.0)

        self.assertEqual(self.num_cancel,1)
        self.assertEqual(self.num_events,1)




if __name__ == "__main__":
    unittest.main()
