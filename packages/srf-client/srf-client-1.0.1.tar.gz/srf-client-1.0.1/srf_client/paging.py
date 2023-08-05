from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, Sequence, TypeVar

import attr
import humps
from lazy_object_proxy import Proxy

T = TypeVar('T')


# https://github.com/python-attrs/attrs/issues/313
@attr.s(frozen=True, auto_attribs=True)
class Page(Generic[T]):
    """
    A page of results.

    :param items: Sequence of result items
    :param total: Total number of available items
    :param first: First page of results
    :param last: Last page of results
    :param next: Next page of results
    :param prev: Previous page of results
    """

    _client: 'PagingClient[T]'
    items: Sequence[T]
    total: int
    _first: str
    _last: str
    _next: Optional[str] = None
    _prev: Optional[str] = None

    @property
    def first(self) -> 'Page[T]':  # noqa: D102
        return self._client.get_page(self._first)

    @property
    def last(self) -> 'Page[T]':  # noqa: D102
        return self._client.get_page(self._last)

    @property
    def next(self) -> Optional['Page[T]']:  # noqa: D102
        if self._next:
            return self._client.get_page(self._next)
        else:
            return None

    @property
    def prev(self) -> Optional['Page[T]']:  # noqa: D102
        if self._prev:
            return self._client.get_page(self._prev)
        else:
            return None


class PagingClient(Generic[T], ABC):
    """
    Base class for paging support.

    :param page_size: the default page size
    """

    page_size = 100

    @staticmethod
    def _filter_params(**kwargs):
        """Remove reserved query params."""
        return {k: v for k, v in kwargs.items()
                if k not in ('includeItems', 'page', 'size')}

    def __init__(self, client, fragment):
        """
        Construct base class.

        :param client: root SRFData client
        :param fragment: URI path fragment
        """
        from . import SRFData
        self._client: SRFData = client
        self._fragment = fragment

    @abstractmethod
    def _parse_obj(self, data, uri) -> T:
        ...

    def _parse_item(self, data) -> T:
        try:
            return self._parse_obj(data['_item'], data['_location'])
        except KeyError:
            return Proxy(lambda: self.get(uri=data['_location']))

    def get(self, *, uri=None, obj_id=None) -> Optional[T]:
        """
        Get a single object by its URI or ID.

        In general IDs are not exposed to clients.
        The ``find_*`` methods should be used instead.
        """
        if bool(uri) == bool(obj_id):
            raise ValueError('Exactly one of uri or obj_id must be given')
        if obj_id:
            uri = f'/{self._fragment}/{obj_id}'

        response = self._client.get(uri)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return self._parse_obj(response.json(), response.url)

    def get_page(self, uri, params=None) -> Page[T]:
        """
        Get a page of objects.

        In general this method should not be used directly.
        Access is via ``find_*`` methods and attributes of ``Page``.
        """
        if params is None:
            params = {'size': self.page_size}
        elif 'size' not in params:
            params['size'] = self.page_size

        response = self._client.get(uri, params=humps.camelize(params))
        response.raise_for_status()
        data = response.json()
        return Page(
            client=self,
            items=tuple(self._parse_item(i) for i in data['_items']),
            total=data['_total'],
            first=data['_first'],
            last=data['_last'],
            next=data.get('_next'),
            prev=data.get('_prev')
        )


def paged_items(page: Page[T]) -> Iterable[T]:
    """
    Iterate over all items in all further pages.

    :param page: Page to start from
    """
    while page:
        for item in page.items:
            yield item
        page = page.next
