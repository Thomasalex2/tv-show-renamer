import os
import requests
import bs4
import re

verification = 'Y'

#============================CONFIGURATION============================================

#------------------------------FOR BOTH--------------------------------

dest_directory = 'D:\TV Shows\House MD\House MD Season 1\House.M.D.Season.1.S01.720p.WEBDL.x265.HEVCQmanUTR'
name_of_series = 'House'
#episode_per_season = 24   #Comment out either this or next line
total_episodes = 0

#---------------------FOR RETRIEVAL FROM INTERNET----------------------

download_page = "https://en.wikipedia.org/wiki/List_of_House_episodes"

#=====================================================================================


#==========================FOR SXXEXX FORMAT==========================

def RetrievefromInternet():

	new_names_list_wiki = []
	new_names_list = []
	res = requests.get(download_page)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, "html.parser")

	#HTML Attributes

	episode_list = soup.select('tbody .vevent')

	print "\nTo Check if Retrieval is Correct:\n"

	for episode in episode_list:
		episode_no = episode.find('th', attrs={'scope':'row'}).getText()
		episode_name = episode.find('td', attrs={'class':'summary'}).getText()
		formatted_name = episode_no + '. ' + episode_name[1:-1]
		new_names_list_wiki.append(formatted_name)
		print formatted_name

	print '\n\n'
	old_names_list = os.listdir(dest_directory)
	no_of_operations = len(old_names_list)
	no_of_operations_done = 0

	for old_name in old_names_list:

		try:
			index = re.search(r"\bS[0-9][0-9]E[0-9][0-9]\b", old_name, re.I).start()
		except AttributeError:
			print "Filenames are not in the expected format\n"
			return

		season = int(old_name[index+1:index+3])
		identifier = old_name[index+4:index+6]
		for match in new_names_list_wiki:
			dot_index = match.find('.')

			try:
				subtract_episodes = episode_per_season * (season - 1)
			except NameError:
				subtract_episodes = total_episodes

			if int(identifier) == (int(match[:dot_index]) - subtract_episodes):
				epi_name = match.split(' ',1)[1]
				epi_name_mod = ""

				for ch in epi_name:
					if ch in '<>:"\/|?*':
						epi_name_mod = epi_name_mod + ""
					else:
						epi_name_mod = epi_name_mod + ch

				file_format = old_name.split('.')[-1]
				season_no = old_name[index:index+6]
				new_name = name_of_series + ' - ' + season_no + ' - ' + epi_name_mod + '.' + file_format
				print old_name,'\n', '-->', new_name

				#verification = raw_input ('Y/N: ')
				if verification.upper() == 'Y':
					old_path = os.path.join(dest_directory, old_name)
					new_path = os.path.join(dest_directory, new_name)
					os.rename(old_path,new_path)
					no_of_operations_done +=1
					print 'Sucessfully Renamed\n'

	if no_of_operations == no_of_operations_done:
		print "All Files renamed successfully"
	else:
		print no_of_operations - no_of_operations_done, "files were not renamed"


#==============================FOR XX.EPISODE_NAME FORMAT========================================

def ReformatNames():

	season = input("Season: ")
	old_names_list = os.listdir(dest_directory)
	no_of_operations = len(old_names_list)
	no_of_operations_done = 0

	for old_name in old_names_list:

		try:
			ep_no = int(old_name.split('.',1)[0])
		except ValueError:
			continue

		epi_name = old_name.split(' ',1)[1]

		try:
			subtract_episodes = episode_per_season * (season - 1)
		except NameError:
			subtract_episodes = total_episodes

		if ep_no - subtract_episodes < 0:
			print "\nEpisode Number changing to Negative"
			print "Please Check ReformatNames Conditions"
			return

		new_name = name_of_series + ' - ' + 'S' + str('%02d' % season) + 'E' + str('%02d' % (ep_no - subtract_episodes)) + ' - ' + epi_name

		print old_name,'-->', new_name

		#verification = raw_input ('Y/N: ')

		if verification.upper() == 'Y':
			old_path = os.path.join(dest_directory, old_name)
			new_path = os.path.join(dest_directory, new_name)
			os.rename(old_path,new_path)
			no_of_operations_done +=1
			print

	if no_of_operations == no_of_operations_done:
		print "All Files renamed successfully"
	else:
		print no_of_operations - no_of_operations_done, "files were not renamed"


def ReformatNames2():

	old_names_list = os.listdir(dest_directory)
	no_of_operations = len(old_names_list)
	no_of_operations_done = 0

	for old_name in old_names_list:

		flag = 0

		for i in range(len(old_name)):
			if old_name[i] == '[':
				flag = 1
				season = str('%02d' % int(old_name[i+1]))
				epi_no = str(old_name[i+3]) + str(old_name[i+4])

		if flag == 0:
			continue

		epi_name = old_name.split('-')[-1]

		new_name = name_of_series + ' - ' + 'S' + season + 'E' + epi_no + ' -' + epi_name

		print old_name,'-->', new_name

		#verification = raw_input ('Y/N: ')

		if verification.upper() == 'Y':
			old_path = os.path.join(dest_directory, old_name)
			new_path = os.path.join(dest_directory, new_name)
			os.rename(old_path,new_path)
			no_of_operations_done +=1
			print

	if no_of_operations == no_of_operations_done:
		print "All Files renamed successfully"
	else:
		print no_of_operations - no_of_operations_done, "files were not renamed"


#====================================MAIN=============================================

def main():

	print "Which Algorithm do you want to use to rename ?"
	print "1. Retrieve from Internet"
	print "2. Reformat Names - 'XX.EPISODE_NAME'"
	print "3. Reformat Names - 'SERIES - [SxEE] - EPISODE_NAME'"
	
	algo = input ("1/2/3: ")

	if algo == 1:
		RetrievefromInternet()

	elif algo == 2:
		ReformatNames()

	elif algo == 3:
		ReformatNames2()

	else:
		print "Invalid Choice"

main()