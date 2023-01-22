"""
MIT License

Copyright (c) 2023-present cibere

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
from pkgutil import iter_modules

from aiohttp import ClientSession
from discord.utils import MISSING

from discord.ext import commands

__all__ = ["Bot"]
LOGGER = logging.getLogger(__name__)


class Bot(commands.Bot):
    """A subclass of `commands.Bot` which has stuff like

    a pre-populated session attribute
    a `load_extensions` method which will either load all extensions in a given folder, or from a list of them"""

    session: ClientSession

    async def start(
        self, token: str, *, reconnect: bool = True, **aiohttp_session_kwargs
    ) -> None:
        async with ClientSession(**aiohttp_session_kwargs) as session:
            self.session = session
            await super().start(token, reconnect=reconnect)

    async def load_extensions(
        self, *, extensions: list[str] = MISSING, folder: str = MISSING
    ):
        """|coro|

        Loads all of your extensions for you.

        Parameters
        -----------
        extensions : Optional[list[str]]
            a list of extensions to be loaded
        folder : Optional[str]
            the folder your extensions reside in

        Raises
        -----------
        ValueError
            both extensions and folder has been filled or neither have been filled
        """

        if extensions is MISSING and folder is MISSING:
            raise ValueError(
                "You must either provide a list of extensions `extentions kwarg`, or a folder name which contains your extensions `folder` kwarg"
            )
        elif extensions is not MISSING and folder is not MISSING:
            raise ValueError("Both folder and extensions given.")

        if folder:
            extensions = [m.name for m in iter_modules([folder], prefix="cogs.")]

        if extensions:
            for ext in extensions:
                try:
                    await self.load_extension(ext)
                except Exception as e:
                    LOGGER.error("Failed to load extension %s", exc_info=e)
