from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from functools import partial, reduce
from itertools import chain, product
import time
import typing
from typing import TYPE_CHECKING, Any, TypeVar

from loguru import logger
from pydantic import BaseModel, Field, validator
from typing_extensions import Literal, Protocol, TypeAlias, TypedDict
from yarl import URL

from . import manager
from .config import BaseConfig, Flavour
from .utils import bucketise, chain_dict, gather
from .utils import run_in_thread as t
from .utils import shasum

# ``NotRequired`` is provisional and does not exist at runtime
if TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import NotRequired as N


_TAuras = TypeVar('_TAuras', bound='BaseAuras')
_Slug = str
_ImportString = str
_AuraGroup: TypeAlias = 'Sequence[tuple[Sequence[WeakAura], WagoApiResponse, _ImportString]]'

IMPORT_API_URL = URL('https://data.wago.io/api/raw/encoded')


class BuilderConfig(BaseConfig):
    wago_api_key: typing.Optional[str] = None


class BaseAuras(
    BaseModel,
    arbitrary_types_allowed=True,
    json_encoders={URL: str},
):
    class Meta(Protocol):
        api_url: URL
        filename: str

    @classmethod
    def from_lua_table(cls: type[_TAuras], lua_table: Any) -> _TAuras:
        raise NotImplementedError


def _merge_auras(auras: Iterable[_TAuras]) -> dict[type, _TAuras]:
    "Merge auras of the same type."
    return {
        t: t(__root__=reduce(lambda a, b: {**a, **b}, (i.__root__ for i in a)))
        for t, a in bucketise(auras, key=type).items()
    }


class WeakAura(
    BaseModel,
    allow_population_by_field_name=True,
    arbitrary_types_allowed=True,
):
    id: str
    uid: str
    parent: typing.Optional[str]
    url: URL
    version: int

    @classmethod
    def from_lua_table(cls, lua_table: Any) -> WeakAura | None:
        url_string = lua_table.get('url')
        if url_string is not None:
            url = URL(url_string)
            if url.host == 'wago.io':
                return cls.parse_obj({**lua_table, 'url': url})

    @validator('url', pre=True)
    def _url_to_URL(cls, value: str | URL) -> URL:
        if not isinstance(value, URL):
            value = URL(value)
        return value


class WeakAuras(BaseAuras):
    class Meta:
        api_url = URL('https://data.wago.io/api/check/weakauras')
        filename = 'WeakAuras.lua'

    __root__: typing.Dict[_Slug, typing.List[WeakAura]]

    @classmethod
    def from_lua_table(cls, lua_table: Any) -> WeakAuras:
        auras = (
            a for t in lua_table['displays'].values() for a in (WeakAura.from_lua_table(t),) if a
        )
        sorted_auras = sorted(auras, key=lambda a: a.id)
        return cls(__root__=bucketise(sorted_auras, key=lambda a: a.url.parts[1]))


class Plateroo(WeakAura):
    id: str = Field(alias='Name')
    uid = ''


class Plateroos(BaseAuras):
    class Meta:
        api_url = URL('https://data.wago.io/api/check/plater')
        filename = 'Plater.lua'

    __root__: typing.Dict[_Slug, typing.List[Plateroo]]

    @classmethod
    def from_lua_table(cls, lua_table: Any) -> Plateroos:
        auras = (
            a
            for n, p in lua_table['profiles'].items()
            for t in chain(
                ({**p, 'Name': f'__profile_{n}__'},),
                p.get('script_data') or (),
                p.get('hook_data') or (),
            )
            for a in (Plateroo.from_lua_table(t),)
            if a
        )
        sorted_auras = sorted(auras, key=lambda a: a.id)
        return cls(__root__={a.url.parts[1]: [a] for a in sorted_auras})


class WagoApiResponse(TypedDict):
    _id: str  # +   # Alphanumeric ID
    name: str  # +  # User-facing name
    slug: str  # +  # Slug if it has one; otherwise same as ``_id``
    url: str
    created: str  # ISO datetime
    modified: str  # ISO datetime
    game: str  # "classic" or xpac, e.g. "bfa"
    username: N[str]  # +  # Author username
    version: int  # +   # Version counter, incremented with every update
    # Semver auto-generated from ``version`` - for presentation only
    versionString: str
    changelog: WagoApiResponse_Changelog  # +
    forkOf: N[str]  # Only present on forks
    regionType: N[str]  # Only present on WAs


class WagoApiResponse_Changelog(TypedDict):
    format: N[Literal['bbcode', 'markdown']]
    text: N[str]


class WaCompanionBuilder:
    """A WeakAuras Companion port for shellfolk."""

    def __init__(self, manager: manager.Manager, builder_config: BuilderConfig) -> None:
        self.manager = manager
        self.builder_config = builder_config

        output_folder = self.manager.config.plugin_dir / __name__
        self.addon_zip_path = output_folder / 'WeakAurasCompanion.zip'
        self.changelog_path = output_folder / 'CHANGELOG.md'
        self.checksum_txt_path = output_folder / 'checksum.txt'

    @staticmethod
    def extract_auras(model: type[_TAuras], source: str) -> _TAuras:
        from ._custom_slpp import SLPP

        source_after_assignment = source[source.find('=') + 1 :]
        lua_table = SLPP(source_after_assignment).decode()
        return model.from_lua_table(lua_table)

    def extract_installed_auras(self) -> Iterator[WeakAuras | Plateroos]:
        flavour_root = self.manager.config.addon_dir.parents[1]
        saved_vars_of_every_account = flavour_root.glob('WTF/Account/*/SavedVariables')
        for saved_vars, model in product(
            saved_vars_of_every_account,
            [WeakAuras, Plateroos],
        ):
            file = saved_vars / model.Meta.filename
            if not file.exists():
                logger.info(f'{file} not found')
            else:
                content = file.read_text(encoding='utf-8-sig', errors='replace')
                aura_group_cache = self.manager.config.cache_dir / shasum(content)
                if aura_group_cache.exists():
                    logger.info(f'loading {file} from cache at {aura_group_cache}')
                    aura_groups = model.parse_file(aura_group_cache)
                else:
                    start = time.perf_counter()
                    aura_groups = self.extract_auras(model, content)
                    logger.debug(f'{model.__name__} extracted in {time.perf_counter() - start}s')
                    aura_group_cache.write_text(aura_groups.json(), encoding='utf-8')
                yield aura_groups

    async def _fetch_wago_metadata(
        self, api_url: URL, aura_ids: Iterable[str]
    ) -> list[WagoApiResponse]:
        from aiohttp import ClientResponseError

        try:
            return sorted(
                await manager.cache_response(
                    self.manager,
                    api_url.with_query(ids=','.join(aura_ids)),
                    {'minutes': 30},
                    label='Fetching aura metadata',
                    request_extra={'headers': {'api-key': self.builder_config.wago_api_key or ''}},
                ),
                key=lambda r: r['slug'],
            )
        except ClientResponseError as error:
            if error.status != 404:
                raise
            return []

    async def _fetch_wago_import_string(self, aura: WagoApiResponse) -> str:
        return await manager.cache_response(
            self.manager,
            IMPORT_API_URL.with_query(id=aura['_id']).with_fragment(str(aura['version'])),
            {'days': 30},
            label=f"Fetching aura '{aura['slug']}'",
            is_json=False,
            request_extra={'headers': {'api-key': self.builder_config.wago_api_key or ''}},
        )

    async def get_remote_auras(self, auras: BaseAuras) -> _AuraGroup:
        if not auras.__root__:
            return []

        metadata = await self._fetch_wago_metadata(auras.Meta.api_url, auras.__root__)
        import_strings = await gather(self._fetch_wago_import_string(r) for r in metadata)
        return [(auras.__root__[r['slug']], r, i) for r, i in zip(metadata, import_strings)]

    def _checksum(self) -> str:
        from hashlib import sha256

        return sha256(self.addon_zip_path.read_bytes()).hexdigest()

    async def get_checksum(self) -> str:
        return await t(self.checksum_txt_path.read_text)(encoding='utf-8')

    def _get_toc_number(self) -> str:
        game_flavour: Flavour = self.manager.config.game_flavour
        if game_flavour is Flavour.retail:
            return '90100'
        elif game_flavour is Flavour.vanilla_classic:
            return '11400'
        elif game_flavour is Flavour.burning_crusade_classic:
            return '20502'

    def _generate_addon(
        self, auras: Iterable[tuple[type[WeakAuras | Plateroos], _AuraGroup]]
    ) -> None:
        from importlib.resources import read_text
        from zipfile import ZipFile, ZipInfo

        from jinja2 import Environment, FunctionLoader

        from . import wa_templates

        jinja_env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=FunctionLoader(partial(read_text, wa_templates)),
        )
        aura_dict = chain_dict((WeakAuras, Plateroos), (), auras)

        self.addon_zip_path.parent.mkdir(exist_ok=True)
        with ZipFile(self.addon_zip_path, 'w') as file:

            def write_tpl(filename: str, ctx: dict[str, Any]):
                # Not using a plain string as the first argument to ``writestr``
                # 'cause the timestamp would be set to the current time
                # which would render the build unreproducible
                zip_info = ZipInfo(filename=f'WeakAurasCompanion/{filename}')
                file.writestr(zip_info, jinja_env.get_template(filename).render(ctx))

            write_tpl(
                'data.lua',
                {
                    'weakauras': [
                        (
                            metadata['slug'],
                            {
                                'name': metadata['name'],
                                'author': metadata.get('username', '__unknown__'),
                                'encoded': import_string,
                                'wagoVersion': metadata['version'],
                                # ``wagoSemver`` is supposed to be the ``versionString``
                                # from Wago but there is a bug where the ``version``
                                # is sometimes not appended to the semver.
                                # The Companion add-on's version is derived from its checksum
                                # so if ``wagoSemver`` were to change between requests
                                # we'd be triggering spurious updates in instawow.
                                'wagoSemver': metadata['version'],
                                'versionNote': metadata['changelog'].get('text', ''),
                            },
                        )
                        for _, metadata, import_string in aura_dict[WeakAuras]
                    ],
                    # Maps internal UIDs of top-level auras to IDs or slugs on Wago
                    'weakaura_uids': [
                        (a.uid, a.url.parts[1])
                        for existing_auras, _, _ in aura_dict[WeakAuras]
                        for a in (
                            next((i for i in existing_auras if not i.parent), existing_auras[0]),
                        )
                    ],
                    # Maps local names to IDs or slugs on Wago
                    'weakaura_ids': [
                        (a.id, a.url.parts[1])
                        for existing_auras, _, _ in aura_dict[WeakAuras]
                        for a in existing_auras
                    ],
                    'plateroos': [
                        (
                            metadata['slug'],
                            {
                                'name': metadata['name'],
                                'author': metadata.get('username', '__unknown__'),
                                'encoded': import_string,
                                'wagoVersion': metadata['version'],
                                'wagoSemver': metadata['version'],
                                'versionNote': metadata['changelog'].get('text', ''),
                            },
                        )
                        for _, metadata, import_string in aura_dict[Plateroos]
                    ],
                    'plater_ids': [
                        (a.id, a.url.parts[1])
                        for existing_auras, _, _ in aura_dict[Plateroos]
                        for a in existing_auras
                    ],
                },
            )
            write_tpl('init.lua', {})
            write_tpl(
                'WeakAurasCompanion.toc',
                {'interface': self._get_toc_number()},
            )

        self.changelog_path.write_text(
            jinja_env.get_template(self.changelog_path.name).render(
                {
                    'changelog_entries': [
                        (
                            a.id,
                            a.url.parent,
                            metadata['version'],
                            metadata['changelog'].get('text') or 'n/a',
                        )
                        for v in aura_dict.values()
                        for existing_auras, metadata, _ in v
                        for a in (
                            next((i for i in existing_auras if not i.parent), existing_auras[0]),
                        )
                        if a.version != metadata['version']
                    ]
                }
            )
            or 'n/a',
            encoding='utf-8',
        )

        self.checksum_txt_path.write_text(
            self._checksum(),
            encoding='utf-8',
        )

    async def build(self) -> None:
        installed_auras = await t(list)(self.extract_installed_auras())
        installed_auras_by_type = _merge_auras(installed_auras)
        aura_groups = await gather(map(self.get_remote_auras, installed_auras_by_type.values()))
        await t(self._generate_addon)(zip(installed_auras_by_type, aura_groups))
