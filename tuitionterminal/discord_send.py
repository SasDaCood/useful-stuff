from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep


URLS = {
	"personal tutor": {
		"url":"https://discord.com/api/webhooks/973215604687392848/DtHqfhyAZ-UTyNWphgV0mhL238vgfqCXxnHp41poN4vikfV0OFBlaSzi4xAC8HZsdgem",
		"EXCLUDE_GENDER":("female",),
		"EXCLUDE_CAT":("Bangla Medium",),
		"EXCLUDE_SUBS":("Bangla",),
		"MIN_SALARY":6000
	}
}
JOB_URL  = "https://tuitionterminal.com.bd/job-board/job-details/"			# +job ID
YAY_URL  = "https://cdn.discordapp.com/emojis/650967789850460160.webp"
DELAY = 5

current_client ="personal tutor"
webhook  = DiscordWebhook(url=URLS[current_client]["url"],username="TuitionTerminal posts",rate_limit_retry=True)


def cleanMsg(msg):
	return msg.replace("&amp;","&").replace("&quot;",'"').replace("&#039;","'")

def sendEmbed(job_id, rel_time, location, grade, subjects, salary, color, category, days, duration, method, gender, req, apps):
	if gender in URLS[current_client]["EXCLUDE_GENDER"]  or  URLS[current_client]["MIN_SALARY"] > int(salary)  or  category in URLS[current_client]["EXCLUDE_CAT"]  or  subjects in URLS[current_client]["EXCLUDE_SUBS"]:
		#print(f"{job_id} filtered")
		return

	desc = f'**Requirement:** {req}'
	#print(job_id, rel_time, location, grade, subjects, salary, color, category, days, duration, method, gender, req, apps)
	embed = DiscordEmbed(title=grade, description=cleanMsg(desc) + (" @everyone" if category == "English Medium" else "."), color=color)
	embed.set_author(name=job_id, url=f'{JOB_URL}{job_id}', icon_url=YAY_URL)
	embed.set_footer(text=f'{rel_time}														{apps} current applications')
	embed.add_embed_field(name='Salary',       value=salary)
	embed.add_embed_field(name='Location',     value=location)
	embed.add_embed_field(name='Gender',       value=f"{gender}")
	embed.add_embed_field(name='Category',     value=category)
	embed.add_embed_field(name='Classes/week', value=days)
	embed.add_embed_field(name='Duration',     value=duration)
	embed.add_embed_field(name='Method',       value=cleanMsg(method))
	embed.add_embed_field(name='Subjects',     value=cleanMsg(subjects))

	webhook.add_embed(embed)
	response = webhook.execute()
	webhook.remove_embeds()
	sleep(DELAY)
