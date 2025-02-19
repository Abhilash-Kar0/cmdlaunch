import json
import os
from tkinter import *
from tkinter.ttk import *
import pprint


import tkinter as tk
from subprocess import call
from PIL import Image 
# aliasing
ask = input
pp = pprint.PrettyPrinter(indent=4)
jload = json.load

def pretty(*args):
    for arg in args:
        pp.pprint(arg)

class Icon:
    def __init__(self, photo, info, program):
        self.photo = photo
        self.info = info
        self.program = program

    def __repr__(self):
        return '\n@object {} {}\n'.format(self.info, self.program)

root = Tk()

def launch_window(command):
    if sys.platform.startswith('linux'):
        commands = 'gnome-terminal --command \"bash -c \\\"'+ command+'; exec bash\\\"\"'
    elif sys.platform.startswith('win'):
        commands = 'start cmd.exe @cmd /k'+ command
    elif sys.platform.startswith('darwin'):
        #To be implemented for Mac 
        pass        
    #print(commands)
    call(commands, shell = True)


class CmdGUI:
    def __init__(self, master):
        self.master = master

        self.programs = os.listdir('programs')
        self.photo = ''
        self.icons = []
        self.commands = []
        self.columns = 6
        #print('programs:', self.programs)
        for i, program in enumerate(self.programs):
            jsonpath = 'programs/{}/cmdlaunch.json'.format(program)
            info = jload(open(jsonpath))
            #resize the images for Once and ever
            im = Image.open('icons/'+info['icon'])
            if im.size != (300,240):
                im = im.resize((300,240))
                im.save('icons/'+info['icon'])
                print("Images resized to (300,240)")
            im.close()

            photo = PhotoImage(file = 'icons/'+info['icon']) 
            photoimage = photo.subsample(3, 3) 
            self.icons.append(Icon(photoimage, info, program))
            self.commands.append(info['commands'])


        # pretty(self.icons)
        # Twice the loop to preserve image reference
        for i, icon in enumerate(self.icons):
            self.x = tk.Button(root, text=icon.info['name'] +'\n' + icon.info['version'], 
                        image=icon.photo,
                        compound=TOP,
                        command=lambda icon=icon: self.button_exec(icon), width = 100,height =100)

            self.x.grid(row=i // self.columns, column=i % self.columns)

    def button_exec(self, icon):
        os.chdir('programs/'+icon.program)
        for command in icon.info['commands']:
            launch_window(command)
    

#        print(f'''
#            The following button with info was clicked:
#            program:{icon.program}
#            name:{icon.info['name']}
#            version:{icon.info['version']}
#            icon:{icon.info['icon']}
#            commands:{icon.info['commands']}
#            ''')
        
        os.chdir('../..')

cmdlaunch = CmdGUI(root)
root.mainloop()
