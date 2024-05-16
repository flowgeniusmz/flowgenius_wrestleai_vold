import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
from googleapiclient.discovery import build
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from openai import OpenAI
import base64
from tempfile import NamedTemporaryFile, mktemp
import pandas as pd
import cv2
import io
import time

class VideoTranscript():
    def __init__(self):
        self.youtube_client = build('youtube', 'v3', developerKey=st.secrets.googleconfig.google_api_key)
        self.max_results = 10
        self.videos = []
        
    def get_youtube_search(self, query):
        self.query = query
        self.search_request = self.youtube_client.search().list(q=query, part='snippet', maxResults=self.max_results, type='video')
        self.search_response = self.search_request.execute()
        self.get_youtube_videos()
        self.get_video_data()
        self.create_search_result_file()
        
    def get_youtube_videos(self):
        self.video_ids = [item['id']['videoId'] for item in self.search_response.get('items', [])]
        self.videos_request = self.youtube_client.videos().list(id=','.join(self.video_ids), part='id, snippet, contentDetails, statistics')
        self.videos_response = self.videos_request.execute()
        
    def get_video_data(self):
        for item in self.videos_response.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel': item['snippet']['channelTitle'],
                'publish_date': item['snippet']['publishedAt'],
                'duration': item['contentDetails']['duration'],
                'view_count': item['statistics']['viewCount'],
                'like_count': item['statistics'].get('likeCount'),
                'dislike_count': item['statistics'].get('dislikeCount'),
                'comment_count': item['statistics'].get('commentCount'),
                'tags': item['snippet'].get('tags', []),
                'video_id': item['id'],
                'transcript': self.get_video_transcript(video_id=item['id'])
                }
            self.videos.append(video_data)
            
    def get_video_transcript(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id)
            #transcript = ' '.join([item['text'] for item in transcript_list])
            return transcript_list
        except TranscriptsDisabled:
            return "Transcript Unavailable"
        
    def create_search_result_file(self):
        self.video_search_dataframe = pd.DataFrame(self.videos)
        self.searchfiledirectory = st.secrets.pathconfig.ytsearch
        self.searchfilepath = f"{self.searchfiledirectory}{self.query}.csv"
        self.video_search_dataframe.to_csv(self.searchfilepath)
        
# a = VideoTranscript()
# a.get_youtube_search(query="Bo Bassett Wrestling")
# print(a.video_search_dataframe)

class VideoUpload():
    def __init__(self):
        self.video_file_buffer = None
        self.video_path = None
        self.cap = None
        self.total_frames = 0

    def get_frame(self, frame_number):
        """Seek to the specified frame number and return the frame."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        else:
            frame = None  # None indicates an invalid frame
        return frame

    def upload_video(self):
        self.video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
        if self.video_file_buffer is not None:
            tfile = NamedTemporaryFile(delete=False)
            tfile.write(self.video_file_buffer.read())
            self.video_path = tfile.name

            self.cap = cv2.VideoCapture(self.video_path)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def display_frame_range(self):
        if 'frame_range' not in st.session_state or not st.session_state.frame_range:
            st.session_state.frame_range = (0, min(10, self.total_frames - 1))

        frame_range = st.slider(
            'Select Frame Range',
            0, self.total_frames - 1,
            st.session_state.frame_range,
            key='_frame_range'
        )

        col1, col2, col3, col4 = st.columns(4)
        frames_to_display = [
            (frame_range[0] - 1, "Frame Before Start"),
            (frame_range[0], "Start Frame"),
            (frame_range[1], "End Frame"),
            (frame_range[1] + 1, "Frame After End")
        ]

        for i, (frame_index, label) in enumerate(frames_to_display):
            with [col1, col2, col3, col4][i]:
                if 0 <= frame_index < self.total_frames:
                    frame = self.get_frame(frame_index)
                    if frame is not None:
                        st.image(frame)
                        st.caption(f"{label} {frame_index}")
                    else:
                        st.write("No frame available")
                else:
                    st.write("No frame available")

    def download_video_segment(self, frame_range):
        if st.button("Download Video Segment"):
            # Setting up video writer
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])
            output_file_path = mktemp(suffix='.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_file_path, fourcc, out_fps, (frame_width, frame_height))

            for _ in range(frame_range[0], frame_range[1] + 1):
                ret, frame = self.cap.read()
                if ret:
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Writing frame to output file

            out.release()
            self.cap.release()

            # Download link
            with open(output_file_path, 'rb') as f:
                st.download_button('Confirm download', f, file_name='video_segment.mp4')

            os.remove(output_file_path)  # Clean up temporary file

    def run(self):
        st.title('Video Analysis')
        self.upload_video()
        if self.video_file_buffer is not None:
            self.display_frame_range()
            self.download_video_segment(st.session_state.frame_range)
        else:
            st.text("Please upload a video file to proceed.")
        
    
    
        