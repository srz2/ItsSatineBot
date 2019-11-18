import configparser

import time
from datetime import datetime, timedelta

import praw
import praw.exceptions


boo_SendReply = True

# subreddits_to_monitor = 'Test'
# subreddits_to_monitor = 'all'

bot_username = ''

def create_satine_reply_message():
	output = ''

	output += 'Hey, just want to let you know, '
	output += '[Its Satine Actually...](https://i.makeagif.com/media/10-27-2016/XqQlyU.gif)'
	output += '\n\n^You\'re ^welcome'

	return output

def satan_exists(content):
	lst_body = content.lower().split()
	if "satan" in content.lower():
		return True
	else:
		return False

def show_comment(comment):
	print 'From ' + str(comment.author)
	print 'ID:  ' + comment.id
	print 'Parent: ' + comment.parent_id
	print comment.body

def bot_exists_in_parent_comments(comment):
	# print 'Current ID:      ' + comment.id
	# print 'Checking Parent: ' + comment.parent_id
	# print 'Perma link       ' + comment.permalink
	if str(comment.author) == bot_username:
		return True

	if comment.parent_id[0:3] == 't3_':
		# print 'Is top comment, bailing...'
		return False

	# print 'Checking parent'
	parent = comment.parent()
	return bot_exists_in_parent_comments(parent)

def bot_exists_in_sibling_comments(comment):
	comment.refresh()
	replies = comment.replies
	# print replies
	# print 'Number of replies: ' + str(len(replies))
	for reply in replies:
		if str(reply.author) == bot_username:
			return True
	return False

def comment_reply_message(comment, message):
	print 'Posting reply to ' + str(comment.id)
	try:
		new_comment = comment.reply(message)
		print 'New Comment Posted: '  + str(new_comment)
		return new_comment
	except praw.exceptions.APIException as e:
		print e
		print 'Need to sleep: ' + str(reddit.auth.limits['remaining'])
		return None

config = configparser.ConfigParser()
config.read('bot.cfg')

client_id = config['DEFAULT']['CLIENT_ID']
client_secret = config['DEFAULT']['CLIENT_SECRET']
username = config['DEFAULT']['USERNAME']
password = config['DEFAULT']['PASSWORD']
user_agent = config['DEFAULT']['USER_AGENT']

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)

bot_username = str(reddit.user.me())
print('Running bot....' + bot_username)

subreddit = reddit.subreddit(subreddits_to_monitor)							# subscribe to /r/all
for comment in subreddit.stream.comments():									# Stream all comments
	if satan_exists(comment.body):									# Check if 'satan' exists in comment body
		if not bot_exists_in_parent_comments(comment):						# Check if this bot exists in any parent comments
			if not bot_exists_in_sibling_comments(comment):					# Check to make sure comment hasn't already been made
				# show_comment(comment)										# [DEBUG] Show comment
				if boo_SendReply:
					msg = create_satine_reply_message()
					if comment_reply_message(comment, msg) == None:			# Attempt to send message
						seconds = reddit.auth.limits['remaining']			# If it fails, wait for x amount of seconds
						now = datetime.now()
						expire = now + timedelta(seconds=seconds)
						print str(now.time()) + ' - Reddit Sending timeout. Sleeping for ' + str(seconds) + ' seconds. Sending at ' + str(expire.time())
						time.sleep(seconds)
						if comment_reply_message(comment, msg) == None:
							print 'Failed to send reply'
# 		# 		else:
# 		# 			print 'Sending replies is turned off'
# 			else:
# 				print 'Bot reply exists in sibling comment'
# 		else:
# 			print 'Bot reply exists in a parent comment'
# 	else:
# 		print 'A non-satan comment is here'
# 		show_comment(comment)
# 		Dont print anything here, otherwise all comments will be printed
