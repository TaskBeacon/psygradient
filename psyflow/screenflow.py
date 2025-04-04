from psychopy import visual, event, core
from psychopy import gui
import os
def show_instructions(win, use_image=True, img_file='img/instructions.bmp', intro_text=None, continue_key='space'):
    """
    Display instructions using either an image or text.

    Args:
        win (visual.Window): PsychoPy window.
        use_image (bool): Whether to display an image. Default True.
        img_file (str): Path to image file (only used if use_image=True).
        intro_text (str): Instruction text (used if use_image=False or provided explicitly).
        continue_key (str): Key to press to proceed. Default is 'space'.
    """
    if intro_text is not None:
        use_image = False

    if use_image:
        if not os.path.exists(img_file):
            print(f"[Error] Image file not found: {img_file}")
            core.quit()
        instruction_stim = visual.ImageStim(win, image=img_file, pos=(0, 0))
    else:
        if not isinstance(intro_text, str) or not intro_text.strip():
            print("[Error] Invalid or missing instruction text.")
            core.quit()
        instruction_stim = visual.TextStim(win, text=intro_text, height=0.6, wrapWidth=25, color='black', pos=(0, 0))

    while not event.getKeys(keyList=[continue_key]):
        instruction_stim.draw()
        win.flip()

def show_goodbye(win, outro_text="Thanks!"):
    """
    Display a thank-you message and close the task window.

    Args:
        win (visual.Window): PsychoPy window.
        outro_text (str): Text to show before quitting.
    """
    outro = visual.TextStim(win, height=0.6, wrapWidth=25, color='black', pos=(0, 0), text=outro_text)

    while not event.getKeys():
        outro.draw()
        win.flip()

    win.close()
    core.quit()



def get_subject_info():
    """
    Opens a GUI dialog to collect and validate basic subject information.

    The following fields are requested:
        - Subject ID (must be a 3-digit integer between 101–199)
        - Age (must be a 2-digit integer ≥ 18)
        - Gender (choice list)
        - Race (choice list)

    The function ensures:
        - Subject ID and Age are valid before proceeding
        - Shows error dialogs if validation fails
        - Confirmation dialog is shown after successful entry

    Returns:
        list: A list of subject information in the following order:
              [SubjectID (str), Age (str), Gender (str), Race (str)]

    Example:
        subdata = get_subject_info()
        # subdata = ['102', '22', 'Female', 'Asian']
    """
    
    # Make a GUI dialogue to receive sub data
    dataDlg = gui.Dlg(title="Subject data")
    dataDlg.addText('For subject ID, change the last two digits only!')
    dataDlg.addField('Subject ID (three digit):', 100)
    dataDlg.addField('Age:', 1)
    dataDlg.addField('Gender:', choices=["Male", "Female"])
    dataDlg.addField('Race:', choices=[
        "Caucasian", "African-American", "Asian", "Hispinic", "Native-American"
    ])
    
    # Use validation flag in while loop
    vflag = True

    while vflag:
        IDflag = False
        AGEflag = False
        
        subdata = dataDlg.show()
        
        # Validate Subject ID: must be 3-digit int between 101 and 199
        if isinstance(subdata[0], int) and len(str(subdata[0])) == 3 and 100 < subdata[0] < 200:
            IDflag = True
        else:
            errorDlg = gui.Dlg()
            errorDlg.addText('Subject ID should be a 3-digit integer between 101 and 199.')
            errorDlg.addText('For example: 101 or 106')
            errorDlg.show()
            continue
        
        # Validate Age: must be 2-digit int ≥ 18
        if isinstance(subdata[1], int) and len(str(subdata[1])) == 2 and subdata[1] >= 18:
            AGEflag = True
        else:
            errorDlg = gui.Dlg()
            errorDlg.addText('Age must be a 2-digit integer (≥ 18).')
            errorDlg.show()
            continue

        if IDflag and AGEflag:
            vflag = False

    # Confirmation window
    ConfirmDlg = gui.Dlg()
    ConfirmDlg.addText('Subject information successfully registered!')
    ConfirmDlg.show()

    # Convert ID and Age to strings for consistent handling
    subdata[0] = str(subdata[0])
    subdata[1] = str(subdata[1])
    
    return subdata

def show_static_countdown(win, start=3, interval=1.0):
    """
    Displays a simple countdown on screen, with fixed intervals between numbers.

    Args:
        win (visual.Window): The PsychoPy window object.
        start (int): Number to start counting down from (e.g., 3 → 2 → 1).
        interval (float): Time (in seconds) to wait between updates.

    Example:
        show_static_countdown(win, start=3, interval=1.0)
    """
    countdown_text = visual.TextStim(win, height=0.6, wrapWidth=10, color='black', pos=[0, 0])
    
    for i in range(start, 0, -1):
        countdown_text.text = f'Task will begin in {i} s'
        countdown_text.draw()
        win.flip()
        core.wait(interval)


def show_realtime_countdown(win, duration=3):
    """
    Displays a smooth, real-time-updated countdown using a timer.

    Args:
        win (visual.Window): The PsychoPy window object.
        duration (float): Total countdown duration in seconds.

    Notes:
        The display updates every frame and shows the remaining seconds,
        rounded up to avoid displaying '0 s' at the last second.

    Example:
        show_realtime_countdown(win, duration=3)
    """
    countdown_text = visual.TextStim(win, height=0.6, wrapWidth=10, color='black', pos=[0, 0])
    timer = core.Clock()
    
    while timer.getTime() < duration:
        time_left = duration - timer.getTime()
        countdown_text.text = f'Task will begin in {int(time_left) + 1} s'  # +1 avoids '0 s' flash
        countdown_text.draw()
        win.flip()

