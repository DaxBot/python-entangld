<a name="entangld"></a>
# entangld

python-entangld library

This module is a port of the node.js library `entangld`, which synchronizes key-value
stores with RPCs and pub/sub events.

<a name="entangld.entangld"></a>
# entangld.entangld

<a name="entangld.entangld.EntangldError"></a>
## EntangldError Objects

```python
class EntangldError(Exception)
```

Entangld exception

<a name="entangld.entangld.Entangld_Message"></a>
## Entangld\_Message Objects

```python
class Entangld_Message()
```

Entangld message object.

**Arguments**:

- `data` _dict_ - message data
- `data.type` _string_ - the type of entangld message
- `[data.path]` _string_ - the path against which the message is applied
- `[data.uuid]` _string_ - the uuid of the get/value or subscribe/event
- `[data.value]` _any|None_ - a data packet associated with the message

<a name="entangld.entangld.Entangld_Message.get"></a>
#### get

```python
 | @classmethod
 | get(cls, tree, get_params=None)
```

Construct a (remote) 'get' message

**Arguments**:

- `tree` _string_ - the path of the get relative to the remote datastore
- `[get_params=None]` _any|None_ - parameters to pass to a function 'get'
  

**Returns**:

- `Entangld_Message` - the 'get' message

<a name="entangld.entangld.Entangld_Message.value"></a>
#### value

```python
 | @classmethod
 | value(cls, get_msg, value)
```

Construct a (remote) 'value' message

**Arguments**:

- `get_msg` _Entangld_Message_ - the 'get' message to response to
- `value` _any|None_ - the data response to the 'get'
  

**Returns**:

- `Entangld_Message` - the 'value' message

<a name="entangld.entangld.Entangld_Message.setpush"></a>
#### setpush

```python
 | @classmethod
 | setpush(cls, obj)
```

Construct a (remote) 'set'/'push' message

**Arguments**:

- `obj` _dict_ - the parameter object
- `obj.type` _string_ - the type (must be 'set' or 'push')
- `obj.path` _string_ - the path against which the 'set'/'push' is applied
- `obj.value` _any|None_ - the value of the 'set'/'push'
  

**Returns**:

- `Entangld_Message` - the 'set'/'push' message

<a name="entangld.entangld.Entangld_Message.subscribe"></a>
#### subscribe

```python
 | @classmethod
 | subscribe(cls, tree, uuid)
```

Construct a (remote) 'subscribe' message

**Arguments**:

- `tree` _string_ - the path of the subscribe (relative to the remote store)
- `uuid` _sting_ - the uuid of the subscription
  

**Returns**:

- `Entangld_Message` - the 'subscribe' message

<a name="entangld.entangld.Entangld_Message.event"></a>
#### event

```python
 | @classmethod
 | event(cls, path, value, uuid)
```

Construct a (remote) 'event' message

**Arguments**:

- `path` _string_ - the path against which the event is occurring (relative to this datastore)
- `uuid` _string_ - the uuid of the subscription
  

**Returns**:

- `Entangld_Message` - the 'event' message

<a name="entangld.entangld.Entangld_Message.unsubscribe"></a>
#### unsubscribe

```python
 | @classmethod
 | unsubscribe(cls, uuid)
```

Construct a (remote) 'unsubscribe' message

**Arguments**:

- `uuid` _sting_ - the uuid of the subscription to unwatch
  

**Returns**:

- `Entangld_Message` - the 'unsubscribe' message

<a name="entangld.entangld.Subscription"></a>
## Subscription Objects

```python
class Subscription()
```

A datastore Subscription object

**Arguments**:

- `obj` _dict_ - the parameter object for construction
- `obj.path` _string_ - the path (relative to this store) of the subscription
- `obj.uuid` _string_ - the uuid of the subscription
- `obj.callback` _function_ - the callback function to be applied to matching
  event messages, signature 'callback(path, value)'
- `[obj.downstream]` _Entangld_ - the downstream datastore of the subscription
  (if applicable)
- `[obj.upstream]` _Entangld_ - the upstream datastore of the subscription
  (if applicable)

<a name="entangld.entangld.Subscription.callback"></a>
#### callback

```python
 | callback(path, value)
```

Make a subscription callback in the async loop

**Arguments**:

- `path` _string_ - the path of the event (relative to this datastore)
- `value` _any|None_ - the value returned by the event

<a name="entangld.entangld.Subscription.is_pass_through"></a>
#### is\_pass\_through

```python
 | @property
 | is_pass_through()
```

Is this subscription a 'pass through' type?

Pass throughs exist only to support daisy-chain subscriptions across
multiple datastores, and are not really relevant to the operation of
this particular datastore. Usually, the user shouldn't directly
interact with pass through subscriptions.

<a name="entangld.entangld.Subscription.has_downstream"></a>
#### has\_downstream

```python
 | @property
 | has_downstream()
```

Does this subscription have a downstream datastore?

This means that this subscription is not associated with the datastore
where the path points to, and so it will be listening for event messages
from other datastores.

<a name="entangld.entangld.Subscription.matches_message"></a>
#### matches\_message

```python
 | matches_message(msg)
```

Does this subscription match a provided 'event'/'unsubscribe' message?

**Arguments**:

- `msg` _Entangld_Message_ - the 'event'/'unsubscribe' message to check against
  

**Returns**:

- `bool` - True if the message matches this subscription

<a name="entangld.entangld.Subscription.matches_uuid"></a>
#### matches\_uuid

```python
 | matches_uuid(uuid)
```

Does this subscription match a provided subscription uuid?

**Arguments**:

- `uuid` _string_ - the uuid of the subscription to check against
  

**Returns**:

- `bool` - True if the message matches this uuid

<a name="entangld.entangld.Subscription.matches_path"></a>
#### matches\_path

```python
 | matches_path(path)
```

Does this subscription match a provided path?

**Arguments**:

- `path` _string_ - the path (relative to this datastore) to check against
  

**Returns**:

  bool - True if the message matches this path

<a name="entangld.entangld.Subscription.is_beneath"></a>
#### is\_beneath

```python
 | is_beneath(path)
```

Is this subscription beneath (or equal to) a provided path?

I.e. provided path is 'system.voltage' and subscription is on 'system.voltage.unit'
returns True.

**Arguments**:

- `path` _string_ - the path to check against
  

**Returns**:

- `bool` - True if the subscription is below the provided path

<a name="entangld.entangld.Subscription.is_above"></a>
#### is\_above

```python
 | is_above(path)
```

Is this subscription above (or equal to) a provided path?

I.e. provided path is 'system.voltage.unit' and subscription is on 'system.voltage'
returns True.

**Arguments**:

- `path` _string_ - the path to check against
  

**Returns**:

- `bool` - True if the subscription is above the provided path

<a name="entangld.entangld.Entangld"></a>
## Entangld Objects

```python
class Entangld()
```

Synchronized event store

<a name="entangld.entangld.Entangld.extract_from_path"></a>
#### extract\_from\_path

```python
 | @staticmethod
 | extract_from_path(data, path)
```

Given a dictionary, extracts a child object using a string path.

**Arguments**:

- `data` _dict_ - object to extract data from.
- `path` _string_ - path to find beneath data.
  

**Returns**:

  tuple - tuple containing (result, remaining_path)

<a name="entangld.entangld.Entangld.namespace"></a>
#### namespace

```python
 | namespace(obj)
```

Get namespace for a store.

**Arguments**:

- `obj` _dict_ - object to get namespace of.
  

**Returns**:

- `string` - namespace for the given context object.

<a name="entangld.entangld.Entangld.attach"></a>
#### attach

```python
 | attach(namespace, obj)
```

Attach a namespace and a store

**Arguments**:

- `namespace` _string_ - a namespace for this store.
- `obj` _dict_ - context object associated with store.
  

**Raises**:

- `ValueError` - namespace or obj is null/empty.
- `EntangldError` - tried to attach to a namespace twice.

<a name="entangld.entangld.Entangld.detach"></a>
#### detach

```python
 | detach(namespace, obj)
```

Detach a namespace/object pair

**Arguments**:

- `namespace` _string_ - the namespace
- `obj` _dict_ - the context object
  

**Raises**:

- `ValueError` - only one parameter was passed

<a name="entangld.entangld.Entangld.transmit"></a>
#### transmit

```python
 | transmit(func)
```

Attach a function to handle message transmission.

Specify a callback to be used when transmitting data to another
store. Callback will be passed (msg, obj) where msg is an object of
type Entangld_Message and obj is the context object that should receive() it.

**Arguments**:

- `func` _function_ - callback function.
  

**Raises**:

- `TypeError` - func is not callable.

<a name="entangld.entangld.Entangld.receive"></a>
#### receive

```python
 | async receive(msg, obj)
```

Call this function with data transmitted from a remote store.

**Arguments**:

- `msg` _Entangld_Message_ - the entangld message that was received.
- `obj` _dict_ - the store context object where the message originated.
  

**Raises**:

- `EntangldError` - unknown message type or invalid store

<a name="entangld.entangld.Entangld.receive_sync"></a>
#### receive\_sync

```python
 | receive_sync(msg, obj)
```

Synchronous version of .receive

<a name="entangld.entangld.Entangld.push"></a>
#### push

```python
 | async push(path, value)
```

Push an object into a list in the store.

**Arguments**:

- `path` _string_ - the path to set.
- `value` _any|None_ - the object to store at the path.
  

**Raises**:

- `EntangldError` - object at path cannot be pushed to.

<a name="entangld.entangld.Entangld.push_sync"></a>
#### push\_sync

```python
 | push_sync(path, value)
```

Synchronous version of .push

<a name="entangld.entangld.Entangld.set"></a>
#### set

```python
 | set(path, value, op='set')
```

Set an object into the store.

**Arguments**:

- `path` _string_ - the path to set.
- `value` _any|None_ - the object or function to store at path.
- `[op='set']` _string_ - type of operation. Defaults to 'set'.
  

**Raises**:

- `TypeError` - path is not a string.
- `EntangldError` - unable to set object.

<a name="entangld.entangld.Entangld.get"></a>
#### get

```python
 | async get(path='', params=None)
```

Get an object from the store.

**Arguments**:

- `[path='']` _string_ - the path to query.
- `[params=None]` _any|None_ - parameters to pass to fucntion 'get'
  

**Raises**:

- `TypeError` - if path is not a string
  

**Returns**:

- `any` - the value of the get

<a name="entangld.entangld.Entangld.get_sync"></a>
#### get\_sync

```python
 | get_sync(path='', params=None)
```

Synchrones version of .get

<a name="entangld.entangld.Entangld.subscribe"></a>
#### subscribe

```python
 | subscribe(path, func)
```

Subscribe to change events for a path.

If objects at or below this path change, you will get a callback.

Subscriptions to keys within attach()ed stores are remote subscriptions.
If several stores are attached in some kind of arrangement, a given key
may actually traverse multiple stores!  Since each store only knows its
immediate neighbors - and has no introspection into those neighbors - each
store is only able to keeps track of the neighbor on each side with
respect to a particular path and has no knowledge of the eventual
endpoints.  This means that subscribing across several datstores is accomplished
by daisy-chaining 2-way subscriptions across each datastore interface.

For example, let's suppose capital letters represent Entangld stores and
lowercase letters are actual objects.  Then  the path "A.B.c.d.E.F.g.h"
will represent a subscription that traverses four Entangld stores.
From the point of view of a store in the middle - say, E - the "upstream"
is B and the "downstream" is F.

Each store involved keeps track of any subscriptions with which it is
involved.  It tracks the upstream and downstream, and the uuid of the
subscription.  The uuid is the same across all stores for a given
subscription.  For a particular store, the upstream is null if it is the
original link in the chain (called the 'head'), and the downstream is
null if this store owns the endpoint value (called the 'tail'). Any
subscription which is not the head of a chain is called a 'pass through'
subscription, because it exist only to pass 'event' messages back up the
chain to the head (where the user-provided callback function exists).
subscriptions can be checked to see if they are 'pass through' type via
the getter 'sub.is_pass_through'.

**Arguments**:

- `path` _string_ - path to watch.
- `func` _function_ - callback function of the form (path, value)
  

**Returns**:

- `uuid` - the uuid of the subscription

<a name="entangld.entangld.Entangld.subscribed_to"></a>
#### subscribed\_to

```python
 | subscribed_to(path)
```

Check for existing subscriptions.

**Arguments**:

- `path` _string_ - the subscription to check for.
  

**Returns**:

- `int` - count of subscriptions matching path.

<a name="entangld.entangld.Entangld.owned_subscriptions"></a>
#### owned\_subscriptions

```python
 | owned_subscriptions(path="")
```

Get list of subscriptions (not included pass throughs)

Can also provide a 'path' for which this method will search below.

**Arguments**:

- `[path=""]` _string_ - a path to search below

<a name="entangld.entangld.Entangld.unsubscribe"></a>
#### unsubscribe

```python
 | unsubscribe(path_or_uuid)
```

Unsubscribe to change events for a given path.

**Arguments**:

- `path_or_uuid` _string_ - path or uuid to unwatch.
  

**Raises**:

- `EntangldError` - no match found.
  

**Returns**:

- `int` - number of subscriptions removed.

<a name="entangld.entangld.Entangld.unsubscribe_tree"></a>
#### unsubscribe\_tree

```python
 | unsubscribe_tree(path)
```

Remove any subscriptions beneath a path.

**Arguments**:

- `path` _string_ - path to unwatch.
  

**Raises**:

- `EntangldError` - subscription belongs to an attached store.

