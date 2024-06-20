import streamlit as st
from back import detect_emotion, map_emotion_to_query, get_youtube_recommendations

st.title('Emotion-based YouTube Music Recommendations')
with st.sidebar:
    st.markdown("<h1 style='text-align:center;font-family:Georgia;font-size:26px;'>Emo-Music Recommendation Chat</h1>", unsafe_allow_html=True)
    st.markdown("<h7 style='text-align: justify;font-size:20px;'>A place where you can play songs based on your mood. Perfect for times when you’re unsure of what to listen to..</h7>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;font-family:Georgia;font-size:20px;'>Features</h2>", unsafe_allow_html=True)
    
    # Choices for features
    st.markdown("- Users can select preferred language for music recommendations.")
    st.markdown("- Text input is enough to analyze your mood.")
    st.markdown("- Can find recommendations based on views, relevance, and date.")
    st.markdown("---")

    if st.button('Refresh'):
        st.session_state['video_urls'] = []
        st.session_state['recommendations'] = []
        st.session_state['selected_video'] = None
        st.session_state['user_input'] = None
        st.session_state['language'] = None

    sort_order = st.selectbox('Sort songs by:', ['Relevance', 'View count', 'Rating', 'Date'])

user_input = st.text_input('How are you feeling today?', value=st.session_state.get('user_input', ''))
language = st.text_input('Choose a language for the song recommendations (optional)', 'I am feeling lucky')

if 'video_urls' not in st.session_state:
    st.session_state['video_urls'] = []

if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = []

if 'selected_video' not in st.session_state:
    st.session_state['selected_video'] = None

if st.button('Get Recommendations'):
    if user_input:
        emotion = detect_emotion(user_input)
        st.write(f'Detected Emotion: {emotion}')
        if emotion in ['sadness', 'disappointment', 'grief', 'remorse', 'embarrassment', 'nervousness', 'fear', 'confusion']:
            choice = st.selectbox('You are feeling sad. Select recommendations for:', ('Sad songs', 'Joyful/uplifting songs'))
            if choice == 'Sad songs':
                query = 'sad songs'
            else:
                query = 'happy songs'
        else:
            query = map_emotion_to_query(emotion)
            st.write(f'Search Query: {query}')
        order = {
            'Relevance': 'relevance',
            'View count': 'viewCount',
            'Rating': 'rating',
            'Date': 'date'
        }[sort_order]
        recommendations = get_youtube_recommendations(query, language, order)
        st.session_state['recommendations'] = recommendations
        st.session_state['video_urls'] = [item.split('(')[-1].split(')')[0] for item in recommendations if '(' in item]

if st.session_state['recommendations']:
    st.write('Top 5 YouTube Recommendations:')
    for i, video in enumerate(st.session_state['recommendations'], 1):
        try:
            video_title = video.split(' (')[0]
            video_url = st.session_state['video_urls'][i-1] if i <= len(st.session_state['video_urls']) else None
            if video_url:
                st.write(f"{i}. [{video_title}]({video_url})")
            else:
                st.write(f"{i}. {video_title}")
        except IndexError:
            st.write(f"Error displaying recommendation: {video}")

if st.session_state['video_urls']:
    selected_video = st.selectbox('Select a video to play', st.session_state['video_urls'], format_func=lambda x: st.session_state['recommendations'][st.session_state['video_urls'].index(x)].split(' (')[0])
    st.session_state['selected_video'] = selected_video

if st.session_state['selected_video']:
    st.write(f"Playing video: {st.session_state['selected_video']}")
    st.video(st.session_state['selected_video'])
# # Title of the Streamlit app
# st.title('Emotion-based YouTube Music Recommendations')

# # Sidebar content
# with st.sidebar:
#     st.markdown("<h1 style='text-align:center;font-family:Georgia;font-size:26px;'>Emo-Music Recommendation Chat</h1>", unsafe_allow_html=True)
#     st.markdown("<h7 style='text-align: justify;font-size:20px;'>This app detects your mood based on the text you enter and recommends music accordingly.</h7>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown("<h2 style='text-align:center;font-family:Georgia;font-size:20px;'>Features</h2>", unsafe_allow_html=True)
#     st.markdown("- Users can enter their feelings or describe their day.")
#     st.markdown("- Users can choose their preferred language for music recommendations.")
#     st.markdown("---")

#     # Refresh button to reset recommendations and state
#     if st.button('Refresh'):
#         st.session_state.clear()  # Clear all session state

# # Input text box for user input
# user_input = st.text_input('How are you feeling today?', value=st.session_state.get('user_input', ''))

# # Language selection
# language = st.text_input('Choose a language for the song recommendations (optional)', value=st.session_state.get('language', 'I am feeling lucky'))

# # Initialize session state variables if they don't exist
# if 'video_urls' not in st.session_state:
#     st.session_state['video_urls'] = []
# if 'recommendations' not in st.session_state:
#     st.session_state['recommendations'] = []
# if 'selected_video' not in st.session_state:
#     st.session_state['selected_video'] = None
# if 'emotion' not in st.session_state:
#     st.session_state['emotion'] = None
# if 'choice' not in st.session_state:
#     st.session_state['choice'] = None

# # Detect emotion from user input if provided
# if user_input:
#     st.session_state['user_input'] = user_input
#     emotion = detect_emotion(user_input)
#     st.session_state['emotion'] = emotion
#     st.write(f'Detected Emotion: {emotion}')

# # Determine query based on emotion and user choice
# if st.session_state['emotion']:
#     emotion = st.session_state['emotion']
    
#     if emotion in ['sadness', 'disappointment', 'grief', 'remorse', 'embarrassment', 'nervousness', 'fear', 'confusion']:
#         st.session_state['choice'] = st.selectbox('You are feeling sad. Select recommendations for:', 
#                                                  ('Sad songs', 'Joyful/uplifting songs'), 
#                                                  key='emotion_selection')
#         if st.session_state['choice'] == 'Sad songs':
#             query = 'sad songs'
#         else:
#             query = 'happy songs'
#     else:
#         query = map_emotion_to_query(emotion)
#         st.write(f'Search Query: {query}')
# else:
#     query = None

# # Button to get recommendations
# if st.button('Get Recommendations') and query:
#     # Get YouTube recommendations based on the query and language
#     recommendations = get_youtube_recommendations(query, language)
    
#     # Store recommendations and video URLs in session state
#     st.session_state['recommendations'] = recommendations
#     st.session_state['video_urls'] = [item.split('(')[-1].split(')')[0] for item in recommendations if '(' in item]

# # Display the recommendations as clickable links
# if st.session_state['recommendations']:
#     st.write('Top 5 YouTube Recommendations:')
#     for i, video in enumerate(st.session_state['recommendations'], 1):
#         st.write(f"{i}. {video}")

# # Dropdown to select a video to play
# if st.session_state['video_urls']:
#     selected_video = st.selectbox('Select a video to play', st.session_state['video_urls'], 
#                                   format_func=lambda x: st.session_state['recommendations'][st.session_state['video_urls'].index(x)].split(' (')[0])
    
#     # Update selected video in session state
#     st.session_state['selected_video'] = selected_video

# # Embed the selected video
# if st.session_state['selected_video']:
#     st.write(f"Playing video: {st.session_state['selected_video']}")  # Debugging: Print the video URL being played
#     st.video(st.session_state['selected_video'])