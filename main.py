import curses
from curses import wrapper
import time
from random import choice

def load_text():
	with open("main.txt" , "r") as file:
		line = file.readlines()
		return choice(line).strip()

def startscr(stdscr):
	stdscr.clear()
	stdscr.addstr(1,0,"Welcom To Type Booster\n")
	stdscr.addstr(1,0,"Press any key to begin")
	stdscr.refresh()
	stdscr.getkey()

def display_text (stdscr,text,current,wpm=0):
 	stdscr.addstr(text)
 	stdscr.addstr(1,0,f"WPM:  {wpm}")
 	for i, char in enumerate(current):
 		correct = text[i]
 		if char == correct:
 			stdscr.addstr(0, i, char, curses.color_pair(1))
 		elif char != correct :
 			stdscr.addstr(0,i,char,curses.color_pair(2))

def wpm_test(stdscr):
	text = load_text()
	current = []
	wpm = 0
	starttime = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - starttime,1)
		wpm = round((len(current) / (time_elapsed/60))/5)
		stdscr.clear()
		display_text(stdscr,text,current,wpm)
		stdscr.refresh()
		if "".join(current) == text:
			stdscr.nodelay(False)
			break


		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE",'\b',"\x7f"):
			if len(current) > 0:
				current.pop()
		elif len(current) < len(text):
			current.append(key)



def main(stdscr):
	curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
	startscr(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2,0,"You completed the Test")
		key = stdscr.getkey()
		if ord(key) == 27:
			break

wrapper(main)
