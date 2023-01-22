# discord-ext-utils

a collection of utils I use with discord.py

## This repo includes

- [global view error handler global](#global-view-error-handler)
- [global modal error handler](#global-view-error-handler)
- [global view interaction_check](#global-view-interaction_check)
- [CodeblockConverter](#codeblockconverter)
- [BaseConverter](#baseconverter)
- [Custom bot subclass](#custom-bot-subclass)
- [send_message](#send_message)

# Guide/wiki/docs

## global view error handler

To use it, simply subclass our view class instead of `discord.ui.View`. (or if your using a modal, our modal class instead of `discord.ui.Modal`)
After that, our subclass will call `on_view_error` (or `on_modal_error`) then `view.on_error` (or `modal.on_error`) in the case of an errorrrr.

## global view interaction_check

To use it, simply subclass our view class instead of `discord.ui.View`.
Our subclass will call `bot.interaction_check` (if it exists) which acts like `view.interaction_check`. If it returns `True`, then it will check `view.interaction_check`.

## BaseConverter

We have a base converter class which allows you to easily make converters which work for slash, prefix, and hybrid cmds.
Example:

```py
class MyConverter(BaseConverter):
    async def handle(self, ctx_or_interaction, arg) -> str:
        # handle
        return ag
```

## CodeblockConverter

`CodeblockConverter` is actually an `typing.Annotated` statement, which returns `Codeblock` (a dataclass with `code` and `language`). For the actual converter, see `ActualCodeblockConverter`.

## Custom bot subclass

We have a custom bot subclass which you can subclass and use. It contains a re-populated session attribute, and a `bot.load_extensions` method which can either take a list of extensions or a folder which your extensions reside in. It will then load them, and if there is an error it will send it via logs. It also has a `setup_logging` method, which is auto-called when calling `bot.run/start`.

## send_message

this helper func lets you easily send a message. It takes a pos-only arg which is the destination. This could be a context object, interaction, channel, member, webhook, or a messageable. It also takes every kwarg any send method takes, and if a certain method does not support a kwarg it will drop it.
