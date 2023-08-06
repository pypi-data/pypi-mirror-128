import pytest

from anyforce import logging


@pytest.mark.asyncio
def test_logging():
    logger = logging.getLogger("test")
    logger.with_field(k="v").debug("debug")
    logger.with_field(k="v").info("info")
    logger.with_field(k="v").warning("warning")
    logger.with_field(k="v").success("success")
    logger.with_field(k="v").log(logging.INFO, "info")


@pytest.mark.asyncio
async def test_async_logging():
    logger = logging.getAsyncLogger("test")
    logger.with_field(k="v").debug("debug")
    logger.with_field(k="v").info("info")
    logger.with_field(k="v").warning("warning")
    logger.with_field(k="v").success("success")
    logger.with_field(k="v").log(logging.INFO, "info")
    try:
        1 / 0
    except Exception as e:
        logger.with_field(k="v").error("error", exc_info=e)
