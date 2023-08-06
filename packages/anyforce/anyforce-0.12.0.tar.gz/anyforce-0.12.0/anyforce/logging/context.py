from __future__ import annotations

import logging
from asyncio import CancelledError, Task
from contextlib import suppress
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from aiologger.levels import LogLevel
from aiologger.loggers.json import JsonLogger

from .level import SUCCESS


class Context(object):
    def __init__(
        self,
        log: Callable[..., Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        super(Context, self).__init__()
        self._log = log
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
        return Context(log=self._log, context=context)

    def debug(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self._log(
            logging.DEBUG,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.INFO,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.WARNING,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.WARNING,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.ERROR,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.ERROR,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            logging.CRITICAL,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
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
        return self._log(
            SUCCESS,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
            stack_info=stack_info,
            *kwargs,
        )

    def log(
        self,
        level: int,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self._log(
            level,
            msg,
            args=args,
            exc_info=exc_info,
            extra=self.get_extras(extra),
            stack_info=stack_info,
            *kwargs,
        )


class ContextLogger(logging.Logger):
    def with_field(self, **kwargs: Any) -> Context:
        return Context(log=self._log, context=kwargs)


class AsyncContextLogger(JsonLogger):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tasks: List[Task[None]] = []

    def with_field(self, **kwargs: Any) -> Context:
        return Context(
            log=self.__log,
            context=kwargs,
        )

    async def shutdown(self, ignore_exception: bool = True) -> None:
        with suppress(CancelledError):
            for task in self.tasks:
                try:
                    await task
                except Exception as e:
                    if ignore_exception:
                        continue
                    raise e
        await super().shutdown()

    def remove_task(self, task: Task[None]):
        self.tasks.remove(task)

    def __log(
        self,
        level: Union[LogLevel, int],
        msg: str,
        args: Tuple[Any, ...],
        **kwargs: Any,
    ) -> Task[None]:
        task = super()._log(
            LogLevel.INFO if level == SUCCESS else level,
            msg,
            args=args,
            caller=self.find_caller(kwargs.get("stack_info", False)),
            **kwargs,
        )
        task.add_done_callback(self.remove_task)
        self.tasks.append(task)
        return task

    def debug(
        self,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self.__log(
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
        return self.__log(
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
        return self.__log(
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
        return self.__log(
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
        return self.__log(
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
        return self.__log(
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
        return self.__log(
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
        return self.__log(
            SUCCESS,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )

    def log(
        self,
        level: int,
        msg: str,
        *args: Any,
        exc_info: Optional[Exception] = None,
        extra: Optional[Dict[str, Any]] = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self.__log(
            level,
            msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            *kwargs,
        )
