import os
import requests
import bs4
import re
import csv
import PySimpleGUI as sg

sg.change_look_and_feel('DefaultNoMoreNagging')

#============================CONFIGURATION============================================

#------------------------------FOR BOTH--------------------------------

#Type out Y?N below if verification IS or IS NOT needed
required_verification = 'Y'

#name_of_series = 'Arrow'
#episode_per_season = 24   #Comment out either this or next line
total_episodes = 160

#---------------------FOR RETRIEVAL FROM INTERNET----------------------

#download_page = "https://en.wikipedia.org/wiki/List_of_Arrow_episodes"

#=====================================================================================

def ShowSelection():

	#Retrieving Show Database from CSV file to dictionary

	reader = csv.reader(open('TV Show Database.csv'))
	ShowDB = {}
	for row in reader:
	    key = row[0]
	    ShowDB[key] = row[1:]

	#Transferring Show names from CSV file to list box for user selection and fetching download page

	Show_names = (tuple(ShowDB.keys()))

	layout = [[sg.Text('Select the Show')],
	         [sg.Listbox(values=Show_names,select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(50,6), bind_return_key=True, auto_size_text=True)],
	         [sg.Submit(), sg.Cancel()]]
	window = sg.Window('TV Show Renamer 3.0', layout, keep_on_top=True,finalize=True, size = (400,200))
	event, values = window.read()
	window.close()

	if (event == 0 or event == 'Submit') and values[0][0] != '':
		name_of_series = values[0][0]
		download_page = ShowDB.get(name_of_series)[0]
		return name_of_series, download_page

	elif event == 'Cancel':
		print ('\nCancelled\n ==PROGRAM RESTARTED==\n')
		main()
	
	else:
		print ("Please select the show\n")
		ShowSelection()


def DirectoryFetching():

	layout = [[sg.Text('Select the Directory')],
            [sg.Input(), sg.FolderBrowse()],
            [sg.OK(), sg.Cancel()] ]

	window = sg.Window('TV Show Renamer 3.0', layout, keep_on_top=True)
	event, values = window.read()
	window.close()

	if event == 'OK' and values[0] != '':
		return values[0]

	elif event == 'Cancel':
		print ('\nCancelled\n ==PROGRAM RESTARTED==\n')
		main()
	
	else:
		print ("Please select the directory\n")
		DirectoryFetching()


def RetrievefromInternet():

	dest_directory = DirectoryFetching()
	name_of_series, download_page = ShowSelection()

	new_names_list_wiki = []
	new_names_list = []
	res = requests.get(download_page)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, "html.parser")

	#HTML Attributes

	episode_list = soup.select('tbody .vevent')

	#print("\nTo Check if Retrieval is Correct:\n")

	for episode in episode_list:
		episode_no = episode.find('th', attrs={'scope':'row'}).getText()
		episode_name = episode.find('td', attrs={'class':'summary'}).getText()
		formatted_name = episode_no + '. ' + episode_name[1:-1]
		new_names_list_wiki.append(formatted_name)
		
		#Uncomment below to check if retrieval from wiki page is correct and fucntioning
		#print(formatted_name,'\n')

	print ('\n')
	old_names_list = os.listdir(dest_directory)
	no_of_operations = len(old_names_list)
	no_of_operations_done = 0
	pattern = re.compile(r'\bS(\d\d)(|.)E(\d\d)\b', re.IGNORECASE)

	for old_name in old_names_list:

		extract = pattern.search(old_name)

		if extract == None:
			print("Filenames are not in the expected format\n")
			return

		season = extract.group(1)
		identifier = extract.group(3)

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

				new_name = name_of_series + ' - ' + 'S' + season + 'E' + identifier + ' - ' + epi_name_mod + '.' + file_format
				print(old_name,'\n', '-->', new_name)

				
				if required_verification == 'Y':
					verification = input ('Y/N: ')
				else:
					verification = 'Y'

				if verification.upper() == 'Y':
					old_path = os.path.join(dest_directory, old_name)
					new_path = os.path.join(dest_directory, new_name)
					os.rename(old_path,new_path)
					no_of_operations_done +=1
					print('Sucessfully Renamed\n')

	if no_of_operations == no_of_operations_done:
		print("All Files renamed successfully")
	else:
		print(no_of_operations - no_of_operations_done, "files were not renamed")


#==============================FOR XX.EPISODE_NAME FORMAT========================================

def ReformatNames():

	dest_directory = DirectoryFetching()
	season = eval(input("Season: "))
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
			print("\nEpisode Number changing to Negative")
			print("Please Check ReformatNames Conditions")
			return

		new_name = name_of_series + ' - ' + 'S' + str('%02d' % season) + 'E' + str('%02d' % (ep_no - subtract_episodes)) + ' - ' + epi_name

		print(old_name,'-->', new_name)

		if required_verification == 'Y':
			verification = input ('Y/N: ')
		else:
			verification = 'Y'

		if verification.upper() == 'Y':
			old_path = os.path.join(dest_directory, old_name)
			new_path = os.path.join(dest_directory, new_name)
			os.rename(old_path,new_path)
			no_of_operations_done +=1
			print()

	if no_of_operations == no_of_operations_done:
		print("All Files renamed successfully")
	else:
		print(no_of_operations - no_of_operations_done, "files were not renamed")


def ReformatNames2():

	dest_directory = DirectoryFetching()
	old_names_list = os.listdir(dest_directory)
	no_of_operations = len(old_names_list)
	no_of_operations_done = 0
	pattern = re.compile(r'\b(\d{1,2})\w(\d\d)\b')

	for old_name in old_names_list:

		extract = pattern.search(old_name)

		if extract == None:
			print("Filenames are not in the expected format\n")
			return

		season = str('%02d' % int(extract.group(1)))
		epi_no = str('%02d' % int(extract.group(2)))

		epi_name = old_name.split('-')[-1]

		new_name = name_of_series + ' - ' + 'S' + season + 'E' + epi_no + ' -' + epi_name

		print(old_name,'-->', new_name)

		if required_verification == 'Y':
			verification = input ('Y/N: ')
		else:
			verification = 'Y'

		if verification.upper() == 'Y':
			old_path = os.path.join(dest_directory, old_name)
			new_path = os.path.join(dest_directory, new_name)
			os.rename(old_path,new_path)
			no_of_operations_done +=1
			print()

	if no_of_operations == no_of_operations_done:
		print("All Files renamed successfully")
	else:
		print(no_of_operations - no_of_operations_done, "files were not renamed")


#====================================MAIN=============================================

def main():

	print("Which Algorithm do you want to use to rename ?")
	print("1. Retrieve from Internet - '-SXXEXX-'")
	print("2. Reformat Names - 'EPISODE_NO. EPISODE_NAME'")
	print("3. Reformat Names - 'SERIES - [SxEE] - EPISODE_NAME'")
	
	algo = eval(input ("1/2/3: "))

	if algo == 1:
		RetrievefromInternet()

	elif algo == 2:
		ReformatNames()

	elif algo == 3:
		ReformatNames2()

	else:
		print("Invalid Choice")

main()