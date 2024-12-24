import random
import os
import base64
from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup
import streamlit as st
import time  # Import time for simulating delay

# Tarot deck with Tamil interpretations
tarot_deck = {
    "The Fool": [
        "உங்களுக்கு புதிய தொடக்கம் காத்திருக்கிறது! நண்பர்களுடன் ஜூம் அழைப்பில் சேர்ந்து வழக்கம் போல் கோவாவுக்கு சுற்றுலா செல்லும் திட்டத்தை பற்றி 140 வது முறையாக பேசுங்கள். இல்லையெனறால் இருக்கும் அலுவலகத்தில் பேப்பர் போட்டுவிட்டு புதிய வேலைக்கு டாகி போல் திரியுங்கள்."
    ],
    "The Magician": [
        "உங்கள் திறமைகளை முழுவீச்சில் பயன்படுத்துங்கள் – பாவக்காய் பச்சரிசி பாயசத்தை செய்ய சரியான நேரம் இது ! பழைய பொருட்களை புதிதாக மாற்றும் திறமை உங்களிடமிருக்கிறது, குட்டியாய் இருந்தபோது போட்டிருந்த ஜட்டியை, சமையல் கட்டில் உதவும் கரித்துணியாக கட் செய்யும் திறமையை உலகுக்கு சொல்லுங்கள். ஒரு புதிய முயற்சியை செய்ய வேண்டிய நேரம் இது. சீட்டில்லாத சைக்கிளில் இந்திய சுற்றுலா செல்ல சிந்தியுங்கள்."
    ],
    "The High Priestess": [
        "உள்ளுணர்வு உங்களுக்கு ஒரு சாவி! ஃப்ரிட்ஜில் ஒளித்து வைத்திருக்கும் கேக்கை யாராவது எடுக்க நினைத்தால் கூட போதும் அவர்கள் எடுப்பதை தடுக்கும் கில்லாடி நீங்கள். இன்று அமைதியுடன் உங்களை சுற்றி நடப்பதை கவனிக்க தொடங்குங்கள். மேனேஜர் ஆபிசில் இருக்கும் நேரத்தை விட கீழே டீக்கடையில் இருக்கும் நேரம் அதிகம் என்பது உங்களுக்கு தெரிய வரலாம். கேள்வி வரும் முன் பதிலை தயார் செய்யும் உங்கள் அறிவை இயக்கும் நாளாக இன்று இருக்காலாம். வேலை ஏன் முடியவில்லை? என்ற கேள்வி வரும் முன்னே ஏனென்றால் உடம்புக்கு முடியவில்லை ! என்ற பதிலை தயாரக வைத்துக் கொள்ளுங்கள்."
    ],
    "The Empress": [
        "அன்பும் பராமரிப்பும் உங்கள் நாளை அமைப்பதற்கு தயாராக இருக்கிறீர்கள் - உங்கள் நாயை குளிப்பாட்டும் நாள் நெருங்குகிறது. இன்று சமைப்பது மூலம் உங்கள் குடும்பத்திற்கு மகிழ்ச்சியை பகிரலாமா - உடனே அடுப்பை பற்ற வைத்து சுடுதண்ணி சமையுங்கள். சிறிய சேமிப்புகளில் பெரிய மாற்றங்களை உருவாக்கும் திறனைக் கொண்டுள்ளீர்களா - உண்டியலை உடையுங்கள்."
    ],
    "The Emperor": [
        "திட்டமிடும் திறனே உங்கள் சக்தி – நைட் பார்ட்டிக்கு செல்ல வீட்டில் சொல்ல வேண்டிய பொய்க்கு திட்டமிடுங்கள். இன்று உங்கள் வேலை நேரத்தை சமநிலையாகச் செய்ய வேண்டுமென்றால் ஆபீசில் தூங்கும் நேரத்தை குறைத்து விடுங்கள். புதிய வழிமுறைகளைக் கண்டறிந்து உங்கள் வாழ்க்கையை எளிதாக்க வேண்டுமானால் தலைகீழாக தன்ணி குடிப்பதை பற்றி சிந்தியுங்கள்."
    ],
    "The Hierophant": [
        "பழமையான நுணுக்கங்களை இந்த காலத்திற்கு ஏற்ப மாற்ற வேண்டுமென்று நினைத்தீர்களானால் லூடோவை ஆன்லைனில் விளையாடுங்கள். ஆன்மிக பயணத்தில் புதுப்பிக்க நேரம் இது. டிவியில் கந்தன் கருணை படம் பாருங்கள். பிறரின் ஆலோசனையை கேட்டு செயல்படடுங்கள். க்ரீம் 11 ஆப்பில் யாரை எடுத்தால் 10 ரூபாய் கிடைக்கும் என்று யாரயவது கேட்டு 10 ரூபாய் சம்பாதிக்க பாருங்கள்."
    ],
    "The Lovers": [
        "உறவுகளுக்கான நேரம் – உறவுக்காரர்கள் அனைவரையும் வீட்டிற்கு வர சொல்லிவிட்டு நீங்கள் வெளியே சென்று விடுங்கள். இன்று ஒரு புதிய உறவை ஆரம்பிக்க தயார் செய்யலாமா - டீக்கடையில் புதிய அக்கவுண்டை ஆரம்பிக்கலாம். உறவுகளில் இருந்து வரும் சந்தோஷத்தை அனுபவிக்கலாமா? - நீங்கள் கடும் கஷ்டத்தில் இருபதாக சொல்லுங்கள், அவர்கள் சந்தோஷப்படுவார்கள்."
    ],
    "The Chariot": [
        "உற்சாகமாக முன்னேறுங்கள் – இதுவரை ஒட்டடை அடித்துக்கொண்டிருந்த நீங்கள், இனி மாப் அடிக்குமளவு முன்னேற போகிறீர்கள். சிறிய வெற்றிகளையும் கொண்டாட வழி வந்து விட்டது - புக் கிரிக்கெட்டில் 20 ரன் அடித்ததை கொண்டாடுங்கள். ஒரு நீண்ட பயணத்தை நெருங்கி முன்னேற வேண்டும் என்று உணர்கிறீர்களா. பாண்டிச்சேரி பயணம் முடிக்கும் போது அந்த உணர்வு வரலாம்."
    ],
    "Strength": [
        "சிறு சவால்களை எதிர்கொண்டு வெற்றியடைய முயற்சிக்கலாமா? ஓசி டீக்காக ஒற்றைக்காலில் ஓட்டப்பந்தயம் ஓடி ஜெயிக்கலாம். தள்ளுபடி நாட்களுக்கக காத்திருந்து உங்கள் பொருளாதாரத்தைக் காக்கலாம் - 50 ரூபாய்க்கு 6 கர்ச்சீப் வாங்கும் காலம் வந்து விட்டது. முதலில் ஒரு சுவையான காபியுடன் உங்கள் நாளை தொடங்கலாமா? நீங்களே போட்டு குடியுங்கள்."
    ],
    "The Hermit": [
        "தனிமையில் உள்ள நேரத்தை அனுபவிக்க ஆசையா? நீங்கள் ஏற்கனவே தனியாகத்தான் இருக்கிறீர்கள். அமைதியுடன் உங்கள் வாழ்க்கையை சீரமைக்க நேரமா - அனிருத் பாடல்களை சத்தம் வைக்காமல் கேட்பது சிறந்தது. உங்கள் மன அழுத்தத்தை தணிக்க ஒரு புத்தகத்தை தேர்வு செய்யலாமென்று நினைத்தால் யாரையும் தொந்தரவு செய்யாமல் தாராளமாக தேர்வு செய்யுங்கள்."
    ],
    "Wheel of Fortune": [
        "இன்றைய பருவம் நீங்கள் எதிர்பார்க்காத மாற்றங்களை காணலாம். மேனஜர் உங்களை பார்த்து சிரிக்கலாம். இந்த நேரத்தில், வாழ்கையில் மாற்றங்களை ஏற்றுக் கொள்கின்றீர்கள் - இனி ஆபீசில் ஓசி காபி கிடைக்காது."
    ],
    "Justice": [
        "நீதி மற்றும் சமநிலை இப்போது உங்கள் வாழ்கையில் பிரதானமாக உள்ளது - பாத்திரம் விலக்குவதில் இது உங்களுடைய நாள். இந்த நேரத்தில், நேர்மையாக நடந்து கொள்ளுங்கள். அம்மாவிடம் கடனாக வாங்கிய காசை திருப்பி கொடுத்து விடுங்கள்."
    ],
    "The Hanged Man": [
        "இப்போது நீண்ட நேரம் யோசிக்கவும் எதை பற்றி யோசிக்கலாம் என்று. பழக்கமான பார்வையை மாற்ற வேண்டும் என்று இந்த நேரம் கூறுகிறது - எதிர் வீட்டு பெண்ணை விட்டுவிட்டு அடுத்த தெரு பெண்ணை உஷார் செய்யலாம்."
    ],
    "Death": [
        "இந்த நேரத்தில், முடிவுகளை ஏற்க வேண்டும். - சம்பளம் தாமதமாக வரலாம். பழைய பருவங்கள் முடிகின்றன மற்றும் புதிய ஆரம்பங்கள் ஆரம்பிக்கின்றன - மழை வரலாம், காயப்போட்ட துணியை எடுப்பது நல்லது."
    ],
    "Temperance": [
        "அழகான சமநிலை மற்றும் பொறுமையை நீங்கள் அனுபவிக்க வேண்டிய காலம். இந்த நேரத்தில், உங்கள் வாழ்க்கையில் உன்னத சமநிலையுடன் இருங்கள் - மதியம் டீம் லன்ச்சில் கிடைத்த ஓசி பிரியாணி போலவே இரவும் கிடைக்காது, பழைய சாதம் கூட கிடைக்கலாம்."
    ],
    "The Devil": [
        "நீங்கள் நம்பிக்கையுடன் கூடிய இழப்பை அனுபவிக்கின்றீர்கள். இந்த நேரத்தில், துன்பங்களிலிருந்து விடுபட உங்கள் திறனை கண்டறியுங்கள். இரண்டு நாள் லீவ் போட்டு மல்லாக்க படுத்து விட்டத்தை பார்த்தபடி தூங்கவும்."
    ],
    "The Tower": [
        "சமயோசிதமாக்கல் மற்றும் விபத்துகள் உங்கள் வாழ்க்கையில் நிகழலாம். இந்த நேரத்தில், நீங்கள் புதிய வழிகளை தேடி முடிவுகளை எடுக்க வேண்டும். வண்டியை ஒரு இரண்டு மாதம் அடகு வைத்து விட்டு ஷேர் ஆட்டோவில் செல்லலாம்."
    ],
    "The Star": [
        "நட்சத்திரங்களின் அழகு உங்கள் வாழ்க்கையை ஒளிரச் செய்யும். இந்த நேரத்தில், நீங்கள் புதிய நம்பிக்கையை கண்டுபிடிப்பீர்கள். அதற்காக நட்சத்திரம் நகர்கிறது திரைப்படத்தை பார்க்கலாமா என்று எகத்தாளம் பேச வேண்டாம்."
    ],
    "The Moon": [
        "உங்களுடைய பயங்கள் மற்றும் குறைகள் உங்களுக்கு வெளிப்படையானது. இந்த நேரத்தில், யாராவது குழப்பத்தை ஏற்படுத்தியுள்ளார்கள் - குழப்பமான இந்த நேரத்தில் குழம்பாமல், குழப்பமான குழப்ப மனநிலையை குழப்பமில்லாமல் கையாளுங்கள்."
    ],
    "The Sun": [
        "இந்த நேரத்தில் சந்தோஷம் மற்றும் வெற்றி நிச்சயமாக உங்களுக்குக் கிடைக்கும். நீங்கள் உற்சாகம் மற்றும் ஆரோக்கியத்தை அனுபவிக்க போகிறீர்கள் - ரேடியோ காண்டெஸ்டில் ஜெயித்த ப்ளூ டூத் ஸ்பீக்கரில் பாடல் கேட்டு குதுகலமாக இருங்கள்."
    ],
    "Judgement": [
        "இது உங்கள் மறுபிறவி. பதிவுகளை மறுபரிசீலனை செய்து புதிய உத்தி நெறி தொடங்குங்கள் - இந்த முறையாவது வீட்டில் சொன்ன சாமான்களை மளிகைக் கடையில் மறக்காமல் வாங்கி வாருங்கள்."
    ],
    "The World": [
        "உலகத்தை அரிதாக காணும்போது, நீங்கள் அனைத்து விஷயங்களையும் நிறைவு செய்துவிட்டீர்கள். ஃப்ரிட்ஜில் வாங்கி வைத்திருந்த ஸ்னாக்ஸ் அனைத்தும் காலையில் காணமல் போனதற்கான காரணாம் நீங்கள் என்று தெரிய வரலாம்."
    ]
}

# Correct path for images directory
IMAGE_DIR = "images"  # Update this path if your images are in a different directory

tarot_images = {
    "The Fool": os.path.join(IMAGE_DIR, "The Fool.jpg"),
    "The Magician": os.path.join(IMAGE_DIR, "The Magician.jpg"),
    "The High Priestess": os.path.join(IMAGE_DIR, "The High Priestess.jpg"),
    "The Empress": os.path.join(IMAGE_DIR, "The Empress.jpg"),
    "The Emperor": os.path.join(IMAGE_DIR, "The Emperor.jpg"),
    "The Hierophant": os.path.join(IMAGE_DIR, "The Hierophant.jpg"),
    "The Lovers": os.path.join(IMAGE_DIR, "The Lovers.jpg"),
    "The Chariot": os.path.join(IMAGE_DIR, "The Chariot.jpg"),
    "Strength": os.path.join(IMAGE_DIR, "Strength.jpg"),
    "The Hermit": os.path.join(IMAGE_DIR, "The Hermit.jpg"),
    "Wheel of Fortune": os.path.join(IMAGE_DIR, "Wheel of Fortune.jpg"),
    "Justice": os.path.join(IMAGE_DIR, "Justice.jpg"),
    "The Hanged Man": os.path.join(IMAGE_DIR, "The Hanged Man.jpg"),
    "Death": os.path.join(IMAGE_DIR, "Death.jpg"),
    "Temperance": os.path.join(IMAGE_DIR, "Temperance.jpg"),
    "The Devil": os.path.join(IMAGE_DIR, "The Devil.jpg"),
    "The Tower": os.path.join(IMAGE_DIR, "The Tower.jpg"),
    "The Star": os.path.join(IMAGE_DIR, "The Star.jpg"),
    "The Moon": os.path.join(IMAGE_DIR, "The Moon.jpg"),
    "The Sun": os.path.join(IMAGE_DIR, "The Sun.jpg"),
    "Judgement": os.path.join(IMAGE_DIR, "Judgement.jpg"),
    "The World": os.path.join(IMAGE_DIR, "The World.jpg"),
}

default_image = os.path.join(IMAGE_DIR, "default.jpg")
logo_image = os.path.join(IMAGE_DIR, "logo.png")

# Function to validate date of birth
def validate_dob(dob):
    try:
        datetime.strptime(dob, "%d:%m:%y")
        return True
    except ValueError:
        return False

# Function to draw a tarot card
def draw_card():
    card = random.choice(list(tarot_deck.keys()))
    interpretation = random.choice(tarot_deck[card])
    return card, interpretation

# Function to get image path for the card
def get_image_path(card):
    return tarot_images.get(card, default_image)

# Function to generate Tamil audio
def generate_tamil_audio(text, audio_file="output.mp3", speed_factor=1.0):
    tts = gTTS(text, lang='ta')
    tts.save(audio_file)

    sound = AudioSegment.from_file(audio_file)
    if speed_factor != 1.0:
        sound = speedup(sound, playback_speed=speed_factor)
    
    altered_file = f"altered_{audio_file}"
    sound.export(altered_file, format="mp3")
    return altered_file

# Function to convert images to Base64
def media_to_base64(file_path):
    with open(file_path, "rb") as media_file:
        return base64.b64encode(media_file.read()).decode()

# Add custom styling for the app
st.markdown(
    """
    <style>
    body {
            margin: 100px; /* Adds 50px margin around the entire content */
            padding: 50px; /* Optional: Adds padding inside the content area */
            background-color: #2e1a47; /* Keep the existing background color */
    }
    .main-header {  
        text-align: center;
        margin-top: 20px;
        color: #ffd700;
    }
    .main-header img {
        width: 200px;
        margin-bottom: 20px;
    }
    .card-image {
        display: block;
        margin: 20px auto;
        border-radius: 10px;
        box-shadow: 0px 0px 15px 5px #ffd700;
        max-width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="main-header">
        <img src="data:image/png;base64,{}" style="width: 400px; margin-bottom: 40px;">
        <h1 style="font-size: 40px; color: #ffd700; text-align: center;">
            🔮 Mirchi Joe's AI Tarot Reading 🔮
        </h1>
        <p>Step into the mystical realm and unveil your destiny!</p>
    </div>
    """.format(media_to_base64(logo_image)),
    unsafe_allow_html=True,
)

# User Input Section
st.sidebar.header("🔮 Your Journey Awaits")
name = st.sidebar.text_input("Your Name", placeholder="Enter your name", key="name_input")
dob = st.sidebar.text_input("Date of Birth (DD:MM:YY)", placeholder="Enter your DOB", key="dob_input")
reading_style = st.sidebar.radio("Choose Your Reading Style", ["Serious", "Fun"], key="reading_style_radio")
enable_audio = st.sidebar.checkbox("Enable Mystical Audio", value=False, key="enable_audio_checkbox")

# Speed Selection
audio_speed = st.sidebar.radio(
    "Choose Audio Speed",
    options=["Normal", "Fast", "Slow"],
    index=0,  # Default to "Normal"
    key="audio_speed_radio"
)

# Map speed options to playback speeds
speed_factor_mapping = {
    "Normal": 1.0,
    "Fast": 1.2,
    "Slow": 0.8,
}
selected_speed = speed_factor_mapping[audio_speed]

if st.sidebar.button("🔮 Draw the Card 🔮", key="reveal_button"):
    if not validate_dob(dob):
        st.sidebar.error("Invalid Date of Birth. Please use the format DD:MM:YY.")
    else:
        card, interpretation = draw_card()
        if reading_style == "Serious":
            interpretation += " இதை ஒரு ஆழ்ந்த செய்தியாக எடுத்துக் கொள்ளுங்கள்."
        else:
            interpretation += " சிரமத்தை அனுபவியுங்கள்!"

        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 20px;">
                <h2 style="color: #ffd700;">Welcome, {name}!</h2>
                <p style="font-size: 18px;">Your card holds the answers:</p>
                <img src="data:image/jpeg;base64,{media_to_base64(get_image_path(card))}" class="card-image">
                <h3 style="margin-top: 20px; color: #ffd700;">Card: {card}</h3>
                <p style="font-size: 16px;">{interpretation}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Generate and play audio
        if enable_audio:
            progress_bar = st.progress(0)  # Initialize progress bar
            status_text = st.empty()  # Placeholder for status text
            
            # Step 1: Prepare text for audio
            status_text.text("Preparing text for audio...")
            text_to_speak = f"வணக்கம் {name}, {interpretation}"
            progress_bar.progress(20)  # Update progress to 20%

            # Step 2: Generate audio using gTTS
            status_text.text("Generating audio file...")
            audio_file = "output.mp3"
            tts = gTTS(text_to_speak, lang='ta')
            tts.save(audio_file)
            progress_bar.progress(60)  # Update progress to 60%

            # Step 3: Adjust audio speed (if necessary)
            if selected_speed != 1.0:
                status_text.text("Adjusting audio speed...")
                sound = AudioSegment.from_file(audio_file)
                sound = speedup(sound, playback_speed=selected_speed)
                altered_file = f"altered_{audio_file}"
                sound.export(altered_file, format="mp3")
                audio_file = altered_file
            progress_bar.progress(90)  # Update progress to 90%

            # Step 4: Finalize and prepare playback
            status_text.text("Finalizing...")
            time.sleep(0.5)  # Simulate a small delay for finalization
            progress_bar.progress(100)  # Update progress to 100%

            # Show success message and audio
            progress_bar.empty()  # Clear progress bar
            status_text.empty()  # Clear status text
            st.success("Audio is ready! 🎵")
            st.audio(audio_file)

# Footer Section
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <hr>
        <p>_Thank you for stepping into the mystical realm with Mirchi Joe! ✨_</p>
    </div>
    """,
    unsafe_allow_html=True,
)
