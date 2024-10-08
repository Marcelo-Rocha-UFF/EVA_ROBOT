from flask import Flask, render_template, request
import subprocess
import os
import time


# Variables for module processes.
cv_process = None
tts_process = None
ter_process = None
leds_process = None
light_process = None
audio_process = None
motion_process = None
stt_process = None
display_process = None

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eva_cv_module", methods=["POST"])
def eva_cv_module():
    global cv_process
    if 'btn_run_cv_module' in request.form:
        print("Running Computer Vision module")
        cv_process = subprocess.Popen(["python3", "eva-cv-module/eva-cv.py"])
    elif 'btn_kill_cv_module' in request.form:
        if cv_process is not None: # The process has not yet been initialized.
            cv_process.terminate()
            time.sleep(0.5)
            cv_process.poll()
    return render_template("index.html")

@app.route("/eva_tts_module", methods=["POST"])
def eva_tts_module():
    global tts_process
    if 'btn_run_tts_module' in request.form:
        print("Running TTS module")
        tts_process = subprocess.Popen(["python3", "eva-tts-module/eva-tts.py"])
    elif 'btn_kill_tts_module' in request.form:
        if tts_process is not None: # The process has not yet been initialized.
            tts_process.terminate()
            time.sleep(0.5)
            tts_process.poll()
    return render_template("index.html")


@app.route("/eva_ter_module", methods=["POST"])
def eva_ter_module():
    global ter_process
    if 'btn_run_ter_module' in request.form:
        print("Running TER module")
        ter_process = subprocess.Popen(["/usr/bin/python", "eva-ter-module/eva-ter.py"]) # all libraries from this module are in global python dir (I dont know why...).
    elif 'btn_kill_ter_module' in request.form:
        if ter_process is not None: # The process has not yet been initialized.
            ter_process.terminate()
            time.sleep(0.5)
            ter_process.poll()
    return render_template("index.html")


@app.route("/eva_leds_module", methods=["POST"])
def eva_leds_module():
    global leds_process
    if 'btn_run_leds_module' in request.form:
        print("Running LEDs module")
        leds_process = subprocess.Popen(["python3", "eva-leds-module/eva-leds.py"])
    elif 'btn_kill_leds_module' in request.form:
        if leds_process  is not None: # The process has not yet been initialized.
            leds_process.terminate()
            time.sleep(0.5)
            leds_process.poll()
    return render_template("index.html")


@app.route("/eva_light_module", methods=["POST"])
def eva_light_module():
    global light_process
    if 'btn_run_light_module' in request.form:
        print("Running Light module")
        light_process = subprocess.Popen(["python3", "eva-light-module/eva-light.py"])
    elif 'btn_kill_light_module' in request.form:
        if light_process is not None: # The process has not yet been initialized.
            light_process.terminate()
            time.sleep(0.5)
            light_process.poll()
    return render_template("index.html")


@app.route("/eva_audio_module", methods=["POST"])
def eva_audio_module():
    global audio_process
    if 'btn_run_audio_module' in request.form:
        print("Running Audio module")
        audio_process = subprocess.Popen(["python3", "eva-audio-module/eva-audio.py"])
    elif 'btn_kill_audio_module' in request.form:
        if audio_process is not None: # The process has not yet been initialized. 
            audio_process.terminate()
            time.sleep(0.5)
            audio_process.poll()
    return render_template("index.html")


@app.route("/eva_motion_module", methods=["POST"])
def eva_motion_module():
    global motion_process
    if 'btn_run_motion_module' in request.form:
        print("Running Motion module")
        motion_process = subprocess.Popen(["python3", "eva-motion-module/eva-motion.py"])
    elif 'btn_kill_motion_module' in request.form:
        if motion_process is not None: # The process has not yet been initialized.
            motion_process.terminate()
            time.sleep(0.5)
            motion_process.poll()
    return render_template("index.html")


@app.route("/eva_stt_module", methods=["POST"])
def eva_stt_module():
    global stt_process
    if 'btn_run_stt_module' in request.form:
        print("Running STT module")
        stt_process = subprocess.Popen(["python3", "eva-stt-module/eva-stt.py"])
    elif 'btn_kill_stt_module' in request.form:
        if stt_process is not None: # The process has not yet been initialized.
            stt_process.terminate()
            time.sleep(0.5)
            stt_process.poll()
    return render_template("index.html")


@app.route("/eva_display_module", methods=["POST"])
def eva_display_module():
    global display_process
    if 'btn_run_display_module' in request.form:
        print("Running Display module")
        display_process = subprocess.Popen(["python3", "eva-display-module/eva-display.py"])
    elif 'btn_kill_display_module' in request.form:
        if display_process is not None: # The process has not yet been initialized.
            display_process.terminate()
            time.sleep(0.5)
            display_process.poll()
    return render_template("index.html")


# Running or "Killing" all processes.
@app.route("/eva_all_modules", methods=["POST"])
def eva_all_modules():
    global cv_process, tts_process, ter_process, leds_process, light_process, audio_process, motion_process, stt_process, display_process
    if 'btn_run_all_modules' in request.form:
        cv_process = subprocess.Popen(["python3", "eva-cv-module/eva-cv.py"])
        tts_process = subprocess.Popen(["python3", "eva-tts-module/eva-tts.py"])
        ter_process = subprocess.Popen(["/usr/bin/python", "eva-ter-module/eva-ter.py"]) # all libraries from this module are in global python dir (I dont know why...).
        leds_process = subprocess.Popen(["python3", "eva-leds-module/eva-leds.py"])
        light_process = subprocess.Popen(["python3", "eva-light-module/eva-light.py"])
        audio_process = subprocess.Popen(["python3", "eva-audio-module/eva-audio.py"])
        motion_process = subprocess.Popen(["python3", "eva-motion-module/eva-motion.py"])
        stt_process = subprocess.Popen(["python3", "eva-stt-module/eva-stt.py"])
        display_process = subprocess.Popen(["python3", "eva-display-module/eva-display.py"])
        print("Runing all modules.")

    if 'btn_kill_all_modules' in request.form:
        print("Killing all modules.")
        if cv_process is not None: cv_process.terminate()
        if tts_process is not None: tts_process.terminate()
        if ter_process is not None: ter_process.terminate()
        if leds_process is not None: leds_process.terminate()
        if light_process is not None: light_process.terminate()
        if audio_process is not None: audio_process.terminate()
        if motion_process is not None: motion_process.terminate()
        if stt_process is not None: stt_process.terminate()
        if display_process is not None: display_process.terminate()
        time.sleep(0.5)
        if cv_process is not None: cv_process.poll()
        if tts_process is not None: tts_process.poll()
        if ter_process is not None: ter_process.poll()
        if leds_process is not None: leds_process.poll()
        if light_process is not None: light_process.poll()
        if audio_process is not None: audio_process.poll()
        if motion_process is not None: motion_process.poll()
        if stt_process is not None: stt_process.poll()
        if display_process is not None: display_process.poll()
        os.system("pkill -f eva")
    return render_template("index.html")


# Start the web application.
app.run(host="0.0.0.0", debug = True) 