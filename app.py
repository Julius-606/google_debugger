import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import traceback
from datetime import datetime

st.set_page_config(page_title="G-Sheets Debugger", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ The Ultimate G-Sheets Snitch (V2)")
st.write("Let's catch the bug in 4K. Enter your target sheet URL below and let's run the diagnostics.")

sheet_url = st.text_input("Paste the full Google Sheet URL here:")

if st.button("Run Diagnostics & Print Receipt 🖨️"):
    if not sheet_url:
        st.warning("Bro, you gotta give me a URL first. I can't read minds! 🧠")
        st.stop()

    st.markdown("### 🔍 Diagnostic Run")
    
    # STEP 1: Check Secrets
    with st.spinner("Step 1: Checking if Streamlit Secrets exist..."):
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            st.success("✅ Step 1 Passed: Found the secrets block! (Looking juicy 🧃)")
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 1:** Weird error reading secrets.\n\nError: {e}")
            st.stop()

    # STEP 2: Authenticate with Google
    with st.spinner("Step 2: Trying to authenticate with Google... (Manifesting W's)"):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            client = gspread.authorize(credentials)
            st.success("✅ Step 2 Passed: Google accepted the credentials! We are IN the mainframe! 💻")
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 2:** Auth failed bro.\n\nError: {e}")
            st.code(traceback.format_exc())
            st.stop()

    # STEP 3: Connect to the specific Sheet
    with st.spinner("Step 3: Trying to find your specific Google Sheet..."):
        try:
            sheet = client.open_by_url(sheet_url)
            worksheet = sheet.sheet1
            st.success(f"✅ Step 3 Passed: Found the sheet! It's called '{sheet.title}'. Big W! 🎉")
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 3:** Unknown error finding sheet.\n\nError: {e}")
            st.code(traceback.format_exc())
            st.stop()

    # STEP 4: The Receipt (Append a Row)
    with st.spinner("Step 4: Printing the receipt to your sheet..."):
        try:
            # Get the current time to prove it's live
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Drop a new row at the bottom of the sheet
            receipt_data = [
                current_time, 
                "BULLISH BREAKOUT 🚀", 
                "Streamlit Cloud just touched this sheet! Bag secured all the way from Kisumu! 🇰🇪"
            ]
            
            worksheet.append_row(receipt_data)
                
            st.success(f"✅ Step 4 Passed: CHECK YOUR SHEET RIGHT NOW! I just appended a new row at the bottom. 🚀📈")
            st.balloons()
            
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 4:** Could connect, but couldn't edit. Permission issue?")
            st.code(traceback.format_exc())
            st.stop()
