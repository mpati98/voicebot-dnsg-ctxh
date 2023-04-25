import json
from os.path import exists
def write_json(new_data, filename='ERROR_sample.json'):
    with open(filename,'r+', encoding='utf-8') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat_history"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, ensure_ascii=False)

username = "WLIN"
file_exists = exists(username + '_sample.json')
if file_exists:
    with open(username + '_sample.json', 'r') as openfile:

    # Reading from json file
        json_object = json.load(openfile)
        # print(json_object)
        recent_chat = json_object["chat_history"]
        print(len(recent_chat))
        print(recent_chat[0]["req"])


else:
    total_tag = ""
    total_resp = ""
    temp_resp = ""
    temp_tag = ""
text_input = "hello"
# data_dict = {"req": text_input, "resp": total_resp, "tag": total_tag, "temp_tag": temp_tag, "temp_resp": temp_resp}
# write_json(data_dict, filename=username + "_sample.json")