# cdk8s-redis

> Redis constructs for cdk8s

Basic implementation of a Redis construct for cdk8s. Contributions are welcome!

## Usage

The following will define a Redis cluster with a primary and 2 replicas:

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk8s_redis import Redis

# inside your chart:
redis = Redis(self, "my-redis")
```

DNS names can be obtained from `redis.primaryHost` and `redis.replicaHost`.

You can specify how many replicas to define:

```python
# Example automatically generated from non-compiling source. May contain errors.
Redis(self, "my-redis",
    replicas=4
)
```

Or, you can specify no replicas:

```python
# Example automatically generated from non-compiling source. May contain errors.
Redis(self, "my-redis",
    replicas=0
)
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
