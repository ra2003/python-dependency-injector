"""Custom provider example."""

from dependency_injector import providers


class CustomFactory(providers.Provider):

    __slots__ = ('_factory',)

    def __init__(self, provides, *args, **kwargs):
        self._factory = providers.Factory(provides, *args, **kwargs)
        super().__init__()

    def __deepcopy__(self, memo):
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(
            self._factory.provides,
            *providers.deepcopy(self._factory.args, memo),
            **providers.deepcopy(self._factory.kwargs, memo),
        )
        self._copy_overridings(copied, memo)

        return copied

    def _provide(self, args, kwargs):
        return self._factory(*args, **kwargs)


factory = CustomFactory(object)


if __name__ == '__main__':
    object1 = factory()
    assert isinstance(object1, object)

    object2 = factory()
    assert isinstance(object1, object)

    assert object1 is not object2
