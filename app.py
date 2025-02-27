import streamlit as st
import time

# Page configuration and styling
st.set_page_config(page_title="Countdown Timer by ZeeJay", page_icon="⏱️")

st.markdown('''
# ⏱️Countdown Timer by ZeeJay🙅‍♂️

This is a simple countdown timer app built with Streamlit with added features.
''')
st.write('---')

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
          35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
          52, 53, 54, 55, 56, 57, 58, 59]

col1, col2, col3 = st.columns(3)

hour = col1.selectbox(
   "Hour:",
   numbers,
   index=0,
)

min = col2.selectbox(
   "Minute:",
   numbers,
   index=0,
)

sec = col3.selectbox(
   "Second:",
   numbers,
   index=0,
)

# Feature: Timer Label
timer_label = st.text_input("Timer Label (Optional):", placeholder="e.g., Workout, Meeting")

timeInSecond = (hour*3600) + (min*60) + sec

# Initialize session state for timer control
if 'timer_running' not in st.session_state:
    st.session_state['timer_running'] = False
if 'time_remaining' not in st.session_state:
    st.session_state['time_remaining'] = timeInSecond
if 'initial_time' not in st.session_state: # Store initial time for reset
    st.session_state['initial_time'] = timeInSecond
if 'custom_message' not in st.session_state: # Store custom message
    st.session_state['custom_message'] = "✅ Time Over!" # Default message


# Feature: Custom Message Input
custom_message_input = st.text_input("Custom Message on Timer End (Optional):", placeholder="e.g., Task Completed!", value=st.session_state['custom_message'])
st.session_state['custom_message'] = custom_message_input # Update session state


col4, col5 = st.columns(2) # Columns for Start/Pause and Reset buttons

if not st.session_state['timer_running']:
    if col4.button("Start"):
        if timeInSecond > 0: # Prevent starting with 0 time
            st.session_state['timer_running'] = True
            st.session_state['time_remaining'] = timeInSecond # Reset time if start is pressed again
            st.session_state['initial_time'] = timeInSecond # Update initial time as well


else: # Timer is running - Show Pause button
    if col4.button("Pause"):
        st.session_state['timer_running'] = False


if col5.button("Reset"): # Reset button always available
    st.session_state['timer_running'] = False
    st.session_state['time_remaining'] = st.session_state['initial_time'] # Reset to initial time
    timeInSecond = st.session_state['initial_time'] # Update timeInSecond for display on reset
    hour = int(timeInSecond/3600) # Recalculate hour, min, sec for display
    min = int(timeInSecond/60) %60
    sec = timeInSecond % 60


if st.session_state['timer_running']:
    if st.session_state['time_remaining'] > 0: # Continue countdown only if time is remaining
        with st.empty():
            progress_bar = st.progress(0) # Initialize progress bar
            initial_time_for_progress = st.session_state['initial_time'] # Use initial time for progress calculation
            if initial_time_for_progress == 0: # Avoid division by zero if initial time is 0
                initial_time_for_progress = 1 # Set to 1 to avoid error but progress bar won't be meaningful

            while st.session_state['timer_running'] and st.session_state['time_remaining'] > 0: # Check timer_running and time_remaining in loop
                seconds = st.session_state['time_remaining'] % 60
                minutes = int(st.session_state['time_remaining']/60) %60
                hours = int(st.session_state['time_remaining']/3600)

                displayTime = '<h2>' + f'⏳ {hours:02}:{minutes:02}:{seconds:02}' + '</h2>'

                if timer_label: # Display timer label if provided
                    st.markdown(f"<h3>{timer_label}</h3>", unsafe_allow_html=True)
                st.write(displayTime, unsafe_allow_html=True)

                progress_percent = 100 - (st.session_state['time_remaining'] / initial_time_for_progress) * 100 # Calculate progress
                progress_bar.progress(int(progress_percent)) # Update progress bar

                time.sleep(1)
                st.session_state['time_remaining'] -= 1

            if st.session_state['time_remaining'] <= 0: # Timer finished naturally
                st.session_state['timer_running'] = False # Stop the timer
                progress_bar.progress(100) # Ensure progress bar is full
                st.write(f"<h2 style='color: green;'>{st.session_state['custom_message']}</h2>",unsafe_allow_html=True) # Use custom message


    else: # time_remaining <= 0 when timer started with 0 or reached 0 after pause/reset and then start again
        st.session_state['timer_running'] = False # Ensure timer is stopped
        st.write(f"<h2 style='color: green;'>{st.session_state['custom_message']}</h2>",unsafe_allow_html=True) # Still display time over message


else: # Timer not running, display initial time or paused time
    seconds = st.session_state['time_remaining'] % 60
    minutes = int(st.session_state['time_remaining']/60) %60
    hours = int(st.session_state['time_remaining']/3600)

    displayTime = '<h2>' + f'⏳ {hours:02}:{minutes:02}:{seconds:02}' + '</h2>'
    if timer_label: # Display timer label if provided
        st.markdown(f"<h3>{timer_label}</h3>", unsafe_allow_html=True)
    st.write(displayTime, unsafe_allow_html=True)
    st.progress(0) # Show empty progress bar when timer is not running