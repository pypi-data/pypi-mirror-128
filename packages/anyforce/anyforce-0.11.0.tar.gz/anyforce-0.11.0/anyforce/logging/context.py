from __future__ import annotations

import logging
from asyncio import Task
from typing import Any, Callable, Dict, Optional, Tuple, Union

from aiologger.levels import LogLevel
from aiologger.loggers.json import JsonLogger

from .level import SUCCESS


class Context(object):
    def __init__(
        self,
        isEnabled: Callable[[int], bool],
        log: Callable[..., Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        super(Context, self).__init__()
        self.isEnabled = isEnabled
        self.log = log
        self.context: Dict[str, Any] = context or {}

    def get_extras(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = self.context.copy()
        if extra:
            context.update(extra)

        # 替换特殊关键词
        for keyword in ["name", "level", "msg", "args", "exc_info", "func"]:
            val = context.pop(keyword, None)
            if val:
                context[f"{keyword}_"] = val

        return context

    def with_field(self, **kwargs: Any) -> Context:
        context = self.context.copy()
        context.update(kwargs)
        return Context(isEnabled=self.isEnabled, log=self.log, context=context)

    def debug(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.DEBUG):
            return self

        return self.log(
            logging.DEBUG,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def info(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.INFO):
            return self

        self.log(
            logging.INFO,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def warning(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.WARNING):
            return self

        return self.log(
            logging.WARNING,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def warn(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.WARNING):
            return self

        return self.log(
            logging.WARNING,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def error(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.ERROR):
            return self

        return self.log(
            logging.ERROR,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def exception(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.ERROR):
            return self

        return self.log(
            logging.ERROR,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def critical(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(logging.CRITICAL):
            return self

        return self.log(
            logging.CRITICAL,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def success(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        if not self.isEnabled(SUCCESS):
            return self

        return self.log(
            SUCCESS,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )


class ContextLogger(logging.Logger):
    def with_field(self, **kwargs: Any) -> Context:
        return Context(isEnabled=self.isEnabledFor, log=self._log, context=kwargs)

    def success(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self._log(  # type: ignore
            SUCCESS,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            **kwargs,
        )


class AsyncContextLogger(JsonLogger):
    def with_field(self, **kwargs: Any) -> Context:
        return Context(isEnabled=self.is_enabled_for, log=self.__log, context=kwargs)

    def is_enabled_for(self, level: Union[int, LogLevel]) -> bool:
        return super().is_enabled_for(LogLevel.INFO if level == SUCCESS else level)

    def __log(
        self, level: LogLevel, msg: str, args: Tuple[Any, ...], **kwargs: Any
    ) -> Task[None]:
        return super()._log(
            LogLevel.INFO if level == SUCCESS else level, msg, args=args, **kwargs
        )

    def success(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Task[None]:
        return self._log(
            LogLevel.INFO,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            **kwargs,
        )
