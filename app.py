import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import traceback

st.set_page_config(page_title="G-Sheets Debugger", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ The Ultimate G-Sheets Snitch")
st.write("Let's catch the bug in 4K. Enter your target sheet URL below and let's run the diagnostics.")

sheet_url = st.text_input("Paste the full Google Sheet URL here:")

if st.button("Run Diagnostics 🚀"):
    if not sheet_url:
        st.warning("Bro, you gotta give me a URL first. I can't read minds! 🧠")
        st.stop()

    st.markdown("### 🔍 Diagnostic Run")
    
    # STEP 1: Check Secrets
    with st.spinner("Step 1: Checking if Streamlit Secrets exist..."):
        try:
            if "gcp_service_account" not in st.secrets:
                st.error("🚨 **FAILED AT STEP 1:** I can't find `[gcp_service_account]` in your Streamlit secrets!")
                st.info("💡 **Fix:** Make sure you pasted the TOML format exactly as shown in the instructions.")
                st.stop()
            
            # Extract the dict
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
        except ValueError as e:
            st.error("🚨 **FAILED AT STEP 2:** Google rejected the credentials formatting.")
            st.info("💡 **Fix:** Check your `private_key` in the secrets. Did you lose the `\\n` newline characters? It needs to be exact!")
            st.code(traceback.format_exc())
            st.stop()
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
        except gspread.exceptions.APIError as e:
            st.error("🚨 **FAILED AT STEP 3:** Google API Error. Usually means the API isn't enabled.")
            st.info("💡 **Fix:** Go to Google Cloud Console and ensure BOTH 'Google Sheets API' and 'Google Drive API' are enabled for your project.")
            st.code(traceback.format_exc())
            st.stop()
        except gspread.exceptions.SpreadsheetNotFound:
            st.error("🚨 **FAILED AT STEP 3:** Spreadsheet Not Found or Permission Denied! (This is the most common L)")
            st.info(f"💡 **Fix:** Did you share the Google Sheet with your service account email?\n\nGo to your Google Sheet -> Click 'Share' -> Paste this exact email and give it 'Editor' access: \n\n`{creds_dict.get('client_email', 'UNKNOWN_EMAIL')}`")
            st.stop()
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 3:** Unknown error finding sheet.\n\nError: {e}")
            st.code(traceback.format_exc())
            st.stop()

    # STEP 4: Try to Edit
    with st.spinner("Step 4: Attempting to write a test value to cell A1..."):
        try:
            # Save the old value to put it back
            old_value = worksheet.acell('A1').value
            
            # Write test value
            worksheet.update_acell('A1', 'STREAMLIT_TEST_SUCCESS')
            
            # Put old value back
            if old_value:
                worksheet.update_acell('A1', old_value)
            else:
                worksheet.update_acell('A1', '') # clear it if it was empty
                
            st.success("✅ Step 4 Passed: Successfully wrote to and edited the sheet! We did it fam! 🚀📈")
            st.balloons()
            
        except Exception as e:
            st.error(f"🚨 **FAILED AT STEP 4:** Could connect, but couldn't edit. Permission issue?")
            st.info("💡 **Fix:** Make sure the service account email is added as an **Editor**, not just a Viewer.")
            st.code(traceback.format_exc())
            st.stop()
