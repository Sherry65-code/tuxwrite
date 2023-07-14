#!/usr/bin/env python3

from tkinter import Tk, Button, Label, PhotoImage
import argparse
import queue
import sys
import sounddevice as sd
import json
from os import system

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def notify(head, body):
    system(f"notify-send \"{head}\" \"{body}\"")

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)


def transcribe(root, but):
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info["default_samplerate"])
        if args.model is None:
            model = Model(lang="en-in")
        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None    
        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
                dtype="int16", channels=1, callback=callback):
            islisten = True
            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(f'{rec.Result()}')['text']
                    voice.config(text=result, fg='green')
                    root.update()

                else:
                    partial = json.loads(rec.PartialResult())['partial']
                    if partial == '':
                        pass
                    else:
                        voice.config(text=partial, fg='red')
                        root.update()
                if dump_fn is not None:
                    dump_fn.write(data)
    except KeyboardInterrupt:
        print("\nDone")
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))


def close():
    root.destroy()
    sys.exit(0)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)


running = False
wannarun = True

def transcribe():
    global running
    if running:
        close()
    else:
        running = True
    but.config(text='Listening')
    root.update()
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info["default_samplerate"])
        if args.model is None:
            model = Model(lang="en-in")
        else:
            model = Model(lang=args.model)
        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None    
        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
                dtype="int16", channels=1, callback=callback):
            islisten = True
            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                if not wannarun:
                    return
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(f'{rec.Result()}')['text']
                    voice.config(text=result, fg=green)
                    root.update()

                else:
                    partial = json.loads(rec.PartialResult())['partial']
                    if partial == '':
                        pass
                    else:
                        voice.config(text=partial, fg=red)
                        root.update()
                if dump_fn is not None:
                    dump_fn.write(data)
    except KeyboardInterrupt:
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))


def close():
    wannarun = False
    root.destroy()
    sys.exit(0)
    


bg = '#303030'
fg = '#ffffff'
font = ("MS Sans Serif", 12)
red = '#ffb7b7'
green = '#a8ff83'

root = Tk()
root.geometry("400x300+50+50")
root.title("TuxWrite")
root.config(bg=bg)

mic = PhotoImage(file=r"img/mic.png")

voice = Label(text="^_^", fg=fg, bg=bg, font=font, width=49, wraplength=350, justify="center")
voice.pack(pady=40)

but = Button(image=mic, relief="flat", highlightthickness=0, borderwidth=0, bg=bg, command=transcribe)
but.pack(side="bottom", pady=10)

root.mainloop()