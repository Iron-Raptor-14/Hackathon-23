# Main program to run the API websever

import os
from flask import Flask, flash, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
from utility import Meeting_Master,Agile_Master,Retro_Master,Master_AI
from format import *
import json
from flask_cors import CORS, cross_origin


# UPLOAD_FOLDER = 'meetings'
ALLOWED_EXTENSIONS = {'txt','vtt','docx'}

# Flask Config settings
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'meetings/1'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.secret_key = 'super secret key'
app.json.sort_keys = False



# Each time it starts, determine the number of meetings saved and setup
# loca variable to keep track of meetings
# neccessary incase the server restarts and for object permience
folder_path = os.getcwd() + '/meetings' # Replace with the actual folder path

if os.path.exists(folder_path) and os.path.isdir(folder_path):
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    global meeting_counter
    meeting_counter = len(subfolders) + 1

# check upload is of valid file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# make a new folder for a new ID. Occurs after file upload
def make_folder(ID):
    # Get the current working directory
    current_directory = os.getcwd()

    # Specify the name of the new folder you want to create
    new_folder_name = "meetings/" + str(ID)

    # Combine the current directory and the new folder name to create the full path
    new_folder_path = os.path.join(current_directory, new_folder_name)

    # Check if the folder already exists
    if not os.path.exists(new_folder_path):
        # Create the new folder
        os.mkdir(new_folder_path)
        # print(f"Folder '{new_folder_name}' created in the current directory.")
    # else:
        # print(f"Folder '{new_folder_name}' already exists in the current directory.")

    return


# endpoint to return a JSON with AI Insight results for a given file ID
# Contains Meeting insights, Jira suggestions, Retro actions and Meeting Meta data
@app.route('/files/<id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_file(id):
    
    if(request.method == 'GET'): 

        file_name = "meetings/"+str(id)+"/master_output.json"

        try:

            with open(file_name,'r') as file:
                data = json.load(file)
  
            return jsonify({'data': data}) 
        except:
            return jsonify({'data': "File not found"})
        # return "Got em"

# Endpoint to upload a meeting transcript file via post request.
# Currently takes .vtt,.txt and .docx
# This function will return an acknowledgment or notifcation of failure
# also, uploading file triggers the AI insight generation process for the uplaoded file
@app.route('/uploadtranscript', methods=[ 'POST'])
@cross_origin() # allow all origins all methods
def upload_file():
    if request.method == 'POST':

        # convert incoming API call into a dict for easy access of contents
        file = dict(request.files)['files']

        # if a file is found
        if file.filename:

            # security of name to prevent injection attacks
            filename = secure_filename(file.filename)
            
            global meeting_counter
            old_meeting_counter = meeting_counter
            
            # make new folder, save file
            make_folder(meeting_counter)
            app.config['UPLOAD_FOLDER'] = 'meetings/' +str(meeting_counter)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Access form data of file metadata
            meta_type = request.form.get('meetingType')
            meta_name = request.form.get('name')

            # start the AI process for the files contents i.e. transcript
            # takes about a minute
            meta_dict = Master_AI(filename,meeting_counter,meta_name,meta_type)
        
            meeting_counter = meeting_counter + 1
            
            # return acknoeldegement that files is ready and its ID
            return jsonify({'ID': old_meeting_counter,'title':meta_dict['title'],'type':meta_dict['type'],'date':meta_dict['date'],'attendees':meta_dict['attendees']}) 

  
    return jsonify({'message':'Invalid file upload'})


# Endpoint to request the json master list of files.
@app.route('/masterlist', methods=['GET'])
@cross_origin() # allow all origins all methods.
def return_master_file():
    
    if(request.method == 'GET'): 

        file_name = "master_list.json"

        try:

            with open(file_name,'r') as file:
                data = json.load(file)
  
            return jsonify({'data': data}) 
        except:
            return jsonify({'data': "Master list not found"})

# The following endpoints are deprecated and should only be used to test a specifc function.
# Not for production use.

# # default endpoint. Allows manual file upload via form
# @app.route('/', methods=['GET', 'POST'])
# def home_page():
    
#     if request.method == 'POST':
        
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
        
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
        
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             Meeting_Master(filename)

#             return
#             return redirect(request.url)
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''


# Upload a file (transcript), and return just the meeting minute related AI tasks
# @app.route('/meetinghelp', methods=[ 'POST'])
# def meeting_route():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             # print('here 1')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             # print('here 2')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             to_return = Meeting_Master(filename)
#             # print('here 3')

#             out_file = open("processed/meeting.json", "w")  
    
#             json.dump(to_return, out_file, indent = 6)  
    
#             out_file.close()
  
#             return jsonify({'data': to_return}) 
#     return



# Upload a file (transcript), and return just the agile tickets related AI tasks
# @app.route('/agilehelp', methods=[ 'POST'])
# def agile_route():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             # print('here 1')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             # print('here 2')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             to_return = Agile_Master(filename)
#             # print('here 3')

#             out_file = open("processed/agile.json", "w")  
    
#             json.dump(to_return, out_file, indent = 6)  
    
#             out_file.close()
  
#             return jsonify({'data': to_return}) 
#     return

# Upload a file (transcript), and return just the retro related AI tasks
# @app.route('/retrohelp', methods=[ 'POST'])
# def retro_route():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             # print('here 1')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             # print('here 2')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             to_return = Retro_Master(filename)
#             # print('here 3')

#             out_file = open("processed/retro.json", "w")  
    
#             json.dump(to_return, out_file, indent = 6)  
    
#             out_file.close()
  
#             return jsonify({'data': to_return}) 
#     return

if __name__ == '__main__':
    app.run()