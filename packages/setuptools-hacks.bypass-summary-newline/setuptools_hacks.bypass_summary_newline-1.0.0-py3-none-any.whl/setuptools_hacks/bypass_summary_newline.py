import contextlib


def run(dist):
    with contextlib.suppress(AttributeError):
        (dist.metadata.description,) = dist.metadata.description.split('\n')[:1]
