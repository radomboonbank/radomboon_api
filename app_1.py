from flask import Flask , request
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def connect_google_sheet() :
	scope = ["https://www.googleapis.com/auth/spreadsheets"] 
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
	gc = gspread.authorize(credentials)
	# Google Sheet name = google_api_mobile_operator
	sheet1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1o9fPEjsk-D_c9j6WeYbwMQtmdsq-HTEbw3E7_rnuUSA/edit#gid=0')

	# # Google Sheet name = line_link_sheet
	# sheet1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XQXkBL_JDF26MMbm2MxRe68nVJsh3TYj9Uss8cET2Fo/edit#gid=0')
	worksheet = sheet1.get_worksheet(0) # sheet index in spreadsheets
	global list_data_sheet
	list_data_sheet = worksheet.get_all_values()

app = Flask(__name__)
line_access_token = 'apiNXSRhFfgIJ+ueODzpaYbWloo8mtcVvhp7n6fZAN4/yZ4DWbQChvwxOULpt0c3iUbw1gfvu8HotYNTmvwaCiWVZiGuMoq7mcLQezNZ9J9vlvcDt/1QJXmL1elGMqRX8xOvdSGYjzdeKmQnsMLP2gdB04t89/1O/w1cDnyilFU='

@app.route('/')

@app.route("/webhook", methods=["POST","GET"])
def webhook() :
	from reply_new import ReplyMessage  # ดึง Function จาก File ชื่อ reply_new.py
	if request.method == "GET" :
		return "Your = GET method from ngrok"
	elif request.method == "POST" : # Check Method ถ้าเป็น POST คือเราที่เราส่งข้อความไปในไลน์
		data = request.get_json()   # รับข้อมูลแบบ json
		connect_google_sheet()
		print(data)

		text_from_line = data["events"][0]["message"]["text"]
		reply_token = data["events"][0]["replyToken"]
		print("ข้อความที่ได้รับ คือ : " + text_from_line)
		print("Token ของคนส่ง คือ : " + reply_token)

		for ii in range(len(list_data_sheet)) :
			# print(text_from_line)
			# print(list_data_sheet[ii][0])
			if text_from_line in list_data_sheet[ii][0] :
				reply_msg = str(list_data_sheet[ii][0]) + ' : ' + str(list_data_sheet[ii][1])
				print(reply_msg)
				ReplyMessage(Reply_token=reply_token, TextMessage=reply_msg,Line_Access_Token=line_access_token)
		# if "ก1" in text_from_line :
		# 	reply_msg = "ก.ไก่ ตัวที่ 1"
		# else :
		# 	reply_msg = "ก.ไก่ ตัว ?????"

		
		# ReplyMessage(Reply_token=reply_token, TextMessage=reply_msg,Line_Access_Token=line_access_token)

		return "OK"

if __name__ == "__main__" :
	app.run(port = 200)