import requests
import json
from datetime import date as dt
from datetime import datetime,timedelta
import PySimpleGUI as sg
import pprint
import json
base_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?'


def next_ten_days(pincode,date,how_many_days=7):
	if pincode and date:
		date1 = datetime.strptime(date, '%d-%m-%Y')
		rec_data = []
		for i in range(int(how_many_days)):
			map_str = ''
			date_str = str(date1 + timedelta(days =i)).split(" ")[0] 
			date_format_str = dt.strftime(datetime.strptime(date_str, '%Y-%m-%d'),'%d-%m-%Y')
			map_str = 'pincode='+ pincode + '&date=' + date_format_str
			url = base_url+ map_str
			res = requests.get(url)
			sessions_data = res.json().get('sessions')
			if sessions_data:
				rec_data += sessions_data
			if not rec_data:
				return "No slots available"
		return rec_data
			
	else:
		return "enter the required data"


# Define the window's contents
layout = [[sg.Text("Enter the Date slot?(DD-MM-YYYY)")],[sg.Input(key='-INPUT-')],
		  [sg.Text("Enter Area Pincode ? ")],[sg.Input(key='-INPUT1-')],
		  [sg.Text("How long Do you want checking? (No.of Days)")],[sg.Input(key='-INPUT2-')],
		  [sg.Text(size=(40,1), key='-OUTPUT-')],
		  [sg.Multiline(size=(150,28), key='-OUTPUT1-', autoscroll=True, reroute_stdout=True, write_only=True, reroute_cprint=True)],
		  [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Covid19 vaccine Checker', layout)

# Display and interact with the Window using an Event Loop
while True:
	event, values = window.read()
	# See if user wants to quit or window was closed
	if event == sg.WINDOW_CLOSED or event == 'Quit':
		break
	# Output a message to the window
	rec = next_ten_days(values['-INPUT1-'],values['-INPUT-'],values['-INPUT2-'])
	
	window['-OUTPUT-'].update('Deatails are:\n ')
	if rec:
		str1 = rec
		str1 = rec
		if isinstance(rec,list):
			str1 = ""
			for i in range(len(rec)):
				print (rec[i])
				str1 = str1 +"\n\n" + str(i+1)+": " + json.dumps(rec[i], indent=4)
	# else:
	# 	str1 = rec
	window['-OUTPUT1-'].update(str1)

# Finish up by removing from the screen
window.close()


