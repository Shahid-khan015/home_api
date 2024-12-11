import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask , jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
application = app

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

@app.route('/<name>')
def home(name):



    def list_folders(folder_name):
        try:
        
            result = cloudinary.api.subfolders(folder_name)
            return result['folders']
        except cloudinary.exceptions.Error as e:
            print(f"An error occurred while fetching folders: {str(e)}")
            return []

    def get_videos_from_folder(folder_name):
        try:
            resources = cloudinary.api.resources(type='upload', prefix=folder_name, resource_type='video')
            return resources['resources']

        except cloudinary.exceptions.Error as e:    
            print(f"An error occurred while fetching videos: {str(e)}")
            return []


    def get_optimized_video_url(video_public_id):
        url = cloudinary.CloudinaryImage(video_public_id).build_url(resource_type='video', quality='auto', fetch_format='auto')
        return url

    folders = list_folders('વ્યંજન')


    video_url = {}
    
    for folder in folders:
        folder_name = folder['name']
        if folder_name == name:
            videos = get_videos_from_folder(folder_name)
            if videos:
                for video in videos:
                    video_url[folder_name] = get_optimized_video_url(video['secure_url'])
    
            else:
                print(f"No videos found in folder '{folder_name}'.")

    return jsonify({'consonant' : video_url , "count" : len(video_url)})
    


if __name__ == '__main__':
    app.run(debug=True)
