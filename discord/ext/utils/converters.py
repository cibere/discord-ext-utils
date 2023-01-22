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
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Generic, TypeVar

from discord import Interaction, app_commands
from discord.ext import commands

ConverterReturn = TypeVar("ConverterReturn")

__all__ = ["CodeblockConverter", "Codeblock", "BaseConverter"]

RAW_LOWERCASE_CHARS = "qwertyuiopasdfghjklzxcvbnm"
CHARACTERS = list(RAW_LOWERCASE_CHARS)
CHARACTERS.extend(list(RAW_LOWERCASE_CHARS.upper()))
CODEBLOCK_FORMAT = "`" * 3


class BaseConverter(
    app_commands.Transformer, commands.Converter, Generic[ConverterReturn]
):
    """A base converter that can be used with slash and prefix commands.

    To use, override the `handle` method.
    It takes the following parameters

    ctx_or_interaction : commands.Context | Interaction
        the ctx or interaction the converter was invoked with
    arg : str
        the raw arg
    """

    async def handle(
        self, ctx_or_interaction: commands.Context | Interaction, arg: str
    ) -> ConverterReturn:
        raise NotImplementedError(
            "Subclass this base converter and override the handle coro"
        )

    async def convert(self, ctx: commands.Context, arg: str) -> ConverterReturn:
        return await self.handle(ctx, arg)

    async def transform(self, inter: Interaction, arg: str) -> ConverterReturn:
        return await self.handle(inter, arg)


@dataclass(slots=True)
class Codeblock:
    code: str
    language: str


class ActualCodeblockConverter(BaseConverter):
    """Removes the codeblock from the given arg.

    Parameters
    ----------
    ctx_or_interaction : commands.Context | discord.Interaction
        the ctx or interaction from the slash or prefix command
    arg : str
        the text that will be converted

    Returns
    ----------
    str
        your converted text
    """

    async def handle(
        self, ctx_or_interaction: commands.Context | Interaction, arg: str
    ) -> Codeblock:
        lang = ""
        if arg.startswith("`"):
            arg = arg.removeprefix(CODEBLOCK_FORMAT).removesuffix(CODEBLOCK_FORMAT)
            arg = arg.strip()

            lines = arg.splitlines()
            line1 = lines[0]
            if len(line1) < 10 and all(char in CHARACTERS for char in line1):
                lang = lines.pop(0)
                arg = "\n".join(lines)

        return Codeblock(code=arg, language=lang)


CodeblockConverter = Annotated[Codeblock, ActualCodeblockConverter]
