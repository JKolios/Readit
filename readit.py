import reddit
import pickle
from time import gmtime,strftime
import codecs


def common_keys(dict1,dict2):
	common = []
	for k1 in dict1.keys():
		for k2 in dict2.keys():
			if k1 == k2 :
				common.append(k1)
	return common

def get_top_scorers(r,num):	
	
	top = r.get_subreddit('all').get_hot(limit=num)
	scores = {}
	for story in top:
		scores[str(story.id)] = (story.score,story.title)	
	return scores

def create_change_dict(top,old_top):

	common = common_keys(top,old_top)
	change_dict = {}
	for key in common:
		change_dict[key] = (top[key][0] - old_top[key][0],top[key][1])
	return change_dict	

def main():
	
	r = reddit.Reddit(user_agent='python_wrapper_test')
	top = get_top_scorers(r,50)
	try :
		top_file = open("previous.bin","rb")
	
	# Initial run
	except IOError:
		try :
			top_file = open("previous.bin","wb")
		except IOError:
			print "Cannot create output file."
			quit()
		pickle.dump(top,top_file)
		top_file.close()
		try :
		  report_file = codecs.open('reddit_trends', encoding='utf-8', mode='w')
		except IOError:
			print "Cannot create report file."
			quit()
		print('No previous data detected, assuming initial run')
		report_file.write('Initial run at: ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+'\n')
		report_file.close()
		quit()


	# Later runs
	top_file = open("previous.bin","rb")
	old_top = pickle.load(top_file)
	top_file.close()
	try :
		top_file = open("previous.bin","wb")
	except IOError:
		print "Cannot create output file."
		quit()
	pickle.dump(top,top_file)
	top_file.close()

	# Generate and sort trend list
	trend_dict = create_change_dict(top,old_top)
	trends = trend_dict.values()
	trends = sorted(trends, key = lambda a: -a[0])
	
	# Open and write trend report file
	try :
		report_file = codecs.open('reddit_trends', encoding='utf-8', mode='a+')
	except IOError:
		print "Cannot create report file."
		quit()

	report_file.write('\n' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+'\n\n')
		
	for topic in trends:
		report_file.write(str(topic[0]) + ' ' + topic[1] + '\n')
	report_file.write('\n\n')
	report_file.close()

if __name__ == '__main__':
  main()
