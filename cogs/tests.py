import apscheduler
from numix_imports import *
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

class Tests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Tests" cog loaded')

	def myfunc(name):
		print(f"{name} printed")
		
	jobstores = {
		'mongo': MongoDBJobStore(),
		'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
	}
	executors = {
		'default': ThreadPoolExecutor(20),
		'processpool': ProcessPoolExecutor(5)
	}
	job_defaults = {
		'coalesce': False,
		'max_instances': 3
	}
	scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

	job = scheduler.add_job(myfunc, 'interval', minutes=2)
	job.remove()

def setup(bot):
	bot.add_cog(Tests(bot))