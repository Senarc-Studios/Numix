import os
import io
import re
import json
import time
import psutil
import base64
import asyncio
import discord
import inspect
import aiohttp
import datetime
import textwrap
import traceback
import contextlib
import pymongo

from pymongo import MongoClient
from random import choice
from datetime import datetime
from utils import default
from discord.utils import get
from contextlib import redirect_stdout
from discord.ext import commands, tasks
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext.commands import has_permissions, MissingPermissions, errors