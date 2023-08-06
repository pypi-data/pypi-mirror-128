from typing import Callable, List, Dict, Any, Tuple

from sqlalchemy.cimmutabledict import immutabledict
from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import Session
from sqlalchemy.util._collections import EMPTY_DICT

from constellate.database.sqlalchemy.sharding.shardoption import SetShardEngineOption
from constellate.database.sqlalchemy.sqlalchemydbconfigmanager import SQLAlchemyDbConfigManager


class _GetBindResolver:
    def _get_bind_resolve(self, mapper=None, clause=None, resolvers: List[Callable] = None):
        try:
            return resolvers[0](mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return resolvers[1](mapper=mapper, clause=clause)

    def _get_bind_build_resolvers_order(
        self, bind_priority: str = None, resolvers: List[Callable] = None
    ):
        return list(resolvers if bind_priority == "sqlalchemy" else reversed(resolvers))


class _ConfigManager:
    @property
    def config_manager(self):
        return self._config_manager


class _InjectDefaultExecutionOptions:
    def __inject_options(self, options: Dict = None, default_options: Dict = None):
        default_options = default_options or {}
        # Note: options is most of the time an immutabledict instance.
        options = dict(options)

        no_value = object()
        for key, value in default_options.items():
            current_value = options.get(key, no_value)
            if current_value == no_value:
                # Set default execution option value
                options.update({key: value})
            else:
                # Do not use default execution option value
                pass

        return options

    def _inject_default_bind_arguments(
        self, bind_arguments: Dict = EMPTY_DICT, kw: Dict = EMPTY_DICT
    ) -> Tuple[Dict, Dict]:
        if bind_arguments is not None:
            return (
                self.__inject_options(
                    options=bind_arguments,
                    default_options=self._default_bind_arguments,
                ),
                kw,
            )
        else:
            return bind_arguments, self.__inject_options(
                options=kw.get("bind_arguments", EMPTY_DICT),
                default_options=self._default_bind_arguments,
            )

    def _inject_default_execution_options(
        self, execution_options: Dict = EMPTY_DICT, kw: Dict = EMPTY_DICT
    ) -> Tuple[Dict, Dict]:
        if execution_options is not None:
            return (
                self.__inject_options(
                    options=execution_options,
                    default_options=self._default_execution_options,
                ),
                kw,
            )
        else:
            return execution_options, self.__inject_options(
                options=kw.get("execution_options", EMPTY_DICT),
                default_options=self._default_execution_options,
            )


def pop_param_when_available(kwargs: Dict = {}, key: Any = None, default_value: Any = None):
    return kwargs.pop(key) if key in kwargs else default_value


class MultiEngineSession(
    AsyncSession, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        has_custom_sync_session_class = "sync_session_class" in kwargs

        if has_custom_sync_session_class:
            execution_options = kwargs.get("execution_options", {})
            bind_arguments = kwargs.get("bind_arguments", {})
            kwargs.update({"owner": owner, "config_manager": config_manager})
        else:
            # Extracting execution_options/bind_arguments from kwargs because super.init is not
            # supporting said param
            execution_options = pop_param_when_available(
                kwargs=kwargs, key="execution_options", default_value={}
            )
            bind_arguments = pop_param_when_available(
                kwargs=kwargs, key="bind_arguments", default_value={}
            )

        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._default_bind_arguments = bind_arguments
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        # clause = SELECT * FROM ....
        # mapper = Class being used to access a table. Eg: TradeR
        raise UnboundExecutionError()

    async def execute(
        self, statement, params=None, execution_options=EMPTY_DICT, bind_arguments=None, **kw
    ):
        execution_options, kw = self._inject_default_execution_options(
            execution_options=execution_options, kw=kw
        )
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        return await super().execute(statement, params, execution_options, bind_arguments, **kw)

    async def connection(self, **kw):
        execution_options, kw = self._inject_default_execution_options(kw=kw)
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        return await super().connection(**kw)


class SyncMultiEngineSession(
    Session, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Extracting execution_options/bind_arguments from kwargs because
        # super.init is not supporting said param
        execution_options = pop_param_when_available(
            kwargs=kwargs, key="execution_options", default_value={}
        )
        bind_arguments = pop_param_when_available(
            kwargs=kwargs, key="bind_arguments", default_value={}
        )

        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._default_bind_arguments = bind_arguments
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()

    def execute(
        self,
        statement,
        params=None,
        execution_options=EMPTY_DICT,
        bind_arguments=None,
        _parent_execute_state=None,
        _add_event=None,
        **kw
    ):
        execution_options, kw = self._inject_default_execution_options(
            execution_options=execution_options, kw=kw
        )
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        return super().execute(
            statement,
            params,
            execution_options,
            bind_arguments,
            _parent_execute_state,
            _add_event,
            **kw
        )

    def connection(
        self, bind_arguments=None, close_with_result=False, execution_options=None, **kw
    ):
        execution_options, kw = self._inject_default_execution_options(
            execution_options=execution_options, kw=kw
        )
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        return super().connection(bind_arguments, close_with_result, execution_options, **kw)


class SyncMultiEngineShardSession(
    ShardedSession, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Unsupported params in parent class
        execution_options = pop_param_when_available(
            kwargs=kwargs, key="execution_options", default_value={}
        )
        bind_arguments = pop_param_when_available(
            kwargs=kwargs, key="bind_arguments", default_value={}
        )

        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._default_bind_arguments = bind_arguments
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, shard_id=None, instance=None, clause=None, **kw):
        if shard_id is not None:
            return self._ShardedSession__binds[shard_id]

        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()

    def execute(
        self,
        statement,
        params=None,
        execution_options=EMPTY_DICT,
        bind_arguments=None,
        _parent_execute_state=None,
        _add_event=None,
        **kw
    ):
        execution_options, kw = self._inject_default_execution_options(
            execution_options=execution_options, kw=kw
        )
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        # Hint super() to use the proper super class. Details: https://bugs.python.org/issue15753
        return super(SyncMultiEngineShardSession, self).execute(
            statement,
            params,
            execution_options,
            bind_arguments,
            _parent_execute_state,
            _add_event,
            **kw
        )

    def connection(
        self, bind_arguments=None, close_with_result=False, execution_options=None, **kw
    ):
        execution_options, kw = self._inject_default_execution_options(
            execution_options=execution_options, kw=kw
        )
        bind_arguments, kw = self._inject_default_bind_arguments(
            bind_arguments=bind_arguments, kw=kw
        )
        return super(SyncMultiEngineShardSession, self).connection(
            bind_arguments, close_with_result, execution_options, **kw
        )
