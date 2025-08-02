# normal sec
import os
import sys
import json
import random
import bisect
from datetime import datetime
import time
import asyncio
import copy

# discord sec
import discord
from discord import (
    app_commands,
    Interaction,
    Guild,
    Member,
    Embed,
    Color,
    TextStyle,
    SelectOption
)
from discord.ext import (
    commands,
    tasks
)
from discord.ext.commands import Bot
from discord.ui import Modal, TextInput, Select

# static typing
from enum import Enum
import typing
from typing import (
    # type
    Any,
    Tuple,
    Dict,
    List,
    
    # func
    Callable,
    Coroutine,
    
    # etc
    Optional,
    Union,
    Literal,
    TypeGuard,
    TypedDict,
    cast
)

# my library
from library.SaveData import *
from library.utils.NormalUtil import *
from library.utils.SaveDataUtil import *
from library.Errors import *
from library.Achievement import *
from library.utils.AchievementUtil import *
from library.objects.BaseButt import *
from library.objects.AgreeButt import *
from library.BaseEnum import BaseEnum

T = typing.TypeVar('T')

def forEach(objs:List[Any], func:Callable[[Any], None]) -> None:

    NormalUtil.forEach(objs, func)
