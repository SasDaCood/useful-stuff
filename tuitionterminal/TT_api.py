import requests
from re import compile as comp,DOTALL
from configparser import ConfigParser
import random				# just for random colour
from time import sleep
import discord_send

# todo: change the point at which "job_htm_txt[:job_htm_txt.index("col-md-4 my-2 lg_d_none sm_d_block")]" cuts

class InfoField:
	'''for defining all the info markers. inelegant regex to locate data, along with indices to splice out data from found string'''
	def __init__(self,regex,start,end):
		self.regex = comp(regex,flags=DOTALL)
		self.start, self.end = start, end
		self.list = []							# stores the actual info data for an entire page (or for a single job in the case of INFO2)

	def search(self,text):
		self.list = [x[self.start:self.end] for x in self.regex.findall(text)]				# for INFO, returns list of 10 matches of corresponding data, e.g. 10 job_ids. for INFO2, returns just 1 match per data type
		if not self.list: self.list = ["N/A"]

class InfoPackage:
	# for storing and formatting each job. just wanted to use classes
	def __init__(self, info_index, info, info2, color=None):
		self.id, self.time, self.loc, self.grade, self.subs, self.sal = info["job_id"].list[info_index], info["rel_time"].list[info_index], info["location"].list[info_index], info["grade"].list[info_index], info["subjects"].list[info_index], info["salary"].list[info_index]
		self.cat, self.days, self.dur, self.method, self.gender, self.req, self.apps = info2["category"].list[0], info2["days"].list[0], info2["duration"].list[0], info2["method"].list[0], info2["gender"].list[0], info2["req"].list[0], info2["apps"].list[0]
		if not color:
			random.seed(self.id)															# seed with job_id so that same jobs get the same colour
			self.color = "%06x"%random.randrange(16**6)

	def send(self):
		discord_send.sendEmbed(self.id, self.time, self.loc, self.grade, self.subs, self.sal, self.color, self.cat, self.days, self.dur, self.method, self.gender, self.req, self.apps)


def writeToFile(value, element="last_job_id"):
    cfg["DEFAULT"][element] = f"{value}"
    with open("config.ini","w") as configfile:
        cfg.write(configfile)



cfg = ConfigParser()
cfg.read("config.ini")
JOB_DELAY = 5
LONG_DELAY = 60*5
LAST_JOB_ID = int(cfg["DEFAULT"]["last_job_id"])
API_URL = "https://tuitionterminal.com.bd/search/job-offer/ajax?page="		# +page number to iterate over
INFO = {
	"job_id"  : InfoField('Job Id: [0-9]+?\<',            8,  -1),
	"rel_time": InfoField('mr-1"></i>.*? ago',            10,None),
	"location": InfoField('; margin-right:15px;"\>.*?\<', 22, -1),
	"grade"   : InfoField('Course</span>.*?\</',          18, -2),
	"subjects": InfoField('Subjects</span>.*?\</',        21, -2),
	"salary"  : InfoField('BDT [0-9]*? Tk',               4,  -3)
}
INFO2 = {																	# for the job_htm site; each InfoField.list in INFO2 will have only 1 element but that's alright
	"category": InfoField('Category</span>.*?\</',      20, -2),
	"days"    : InfoField('. Day',                      0, 1),
	"duration": InfoField('Duration</span>.*? Hour\</', 20, -2),
	"method"  : InfoField('Method</span>.*?\</',        18, -2),		# need to replace &#039; with '
	"gender"  : InfoField('Tutor Gender</span>.*?\</',  24, -2),
	"req"     : InfoField('Requirement</span>.*?\</',   23, -2),
	"apps"    : InfoField('TOTAL APPLICATIONS- .*?\<',  20, -1)
}


while 1:				# keep on indefinitely executing
	try:
		current_page = 1
		reached_end = False
		temp_last_job_id = LAST_JOB_ID
		while not reached_end:
			htm_txt = requests.get(f"{API_URL}{current_page}").text		# returns a whole ass webpage in text
			if "Please wait while your request is being verified" in htm_txt: break			# sleep and retry in a while

			for info_field in INFO: INFO[info_field].search(htm_txt)	# save current page's job infos in InfoFields

			job_ids = [int(x) for x in INFO["job_id"].list]
			for index in range(len(job_ids)):
				if job_ids[index] <= LAST_JOB_ID:						# if currently inspected ID is older (lesser ID) or same as last logged ID, skip remaining IDs
					reached_end = True
					break
				else:
					sleep(JOB_DELAY)									# hopefully curb rate-limiting? since 2 requests made in quick succession
					job_htm_txt = requests.get(f"{discord_send.JOB_URL}{job_ids[index]}").text			# get the html for the specific job to get more info like gender. not putting in InfoFields since this takes time; best to only visit job_htm when needed
					job_htm_txt = job_htm_txt[:job_htm_txt.index("col-md-4 my-2 lg_d_none sm_d_block")] # shorten to necessary region
					for info_field in INFO2: INFO2[info_field].search(job_htm_txt)						# save current job's infos

					new_info = InfoPackage(index,INFO,INFO2)
					new_info.send()

			if current_page==1 and job_ids[0] > LAST_JOB_ID: temp_last_job_id = job_ids[0]		# store the first page's first ID (earliest ID) to update LAST_JOB_ID with after all the pages
			current_page += 1
	except Exception as e:
		print(e)

	writeToFile(temp_last_job_id)
	LAST_JOB_ID = temp_last_job_id						# bruh i forgot this
	sleep(LONG_DELAY)