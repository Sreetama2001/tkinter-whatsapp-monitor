import tkinter as tk
import signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os,sys
from PIL import ImageTk, Image
from time import sleep,strftime
from datetime import datetime
# from notify_run import Notify
import tkinter.messagebox as tmsg
# notify=Notify()
from threading import Thread
# from playsound import playsound

msg=[]
user=os.getlogin()



# --- functions ---
def signal_handler(sig, frame):
    print('Saving the file and exiting...')
    save_history()
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def save_history():
    with open("online_history.txt","a") as file:
        for m in msg:
            file.write(m + '\n\n')
def quit():
    save_history()
    sys.exit()



def monitor():
    th = Thread(target=start)
    th.start()



def about():
    msg='''
    
            Montitor Time spent by People 
                on whatsapp 
    '''
    a=tmsg.showinfo("About Whatsapp Monitor",msg)

    

def on_open():
    global driver
    global current_path

    if not driver:
        options = Options()
        options.add_argument("user-data-dir={}/profile/".format(current_path))
        driver = webdriver.Chrome(executable_path="D:\chromedriver.exe",options=options)
        driver.get("http://web.whatsapp.com")


def start():
    global driver,root,current_path,show_status,name,panel,history
    
    curr_name = driver.find_element_by_class_name("_2au8k").text
    name.config(text=curr_name)
    name.update_idletasks()
    try:
        img_path=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[5]/div/header/div[1]/div')
        src = img_path.get_attribute('src')
        driver.execute_script('''window.open("''' +src + '''","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        driver.save_screenshot("pro.png")
        driver.execute_script('''window.close();''')
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass

    img_path = 'pro.png'
    image = Image.open(img_path)
    width, height = image.size
    image = image.resize((round(180 / height * width), round(280)))
    img = ImageTk.PhotoImage(image)
    panel.configure(image=img)
    panel.pack(padx=20)
    panel.image = img
    updateo, updatef = True, True


    ut=True
    i=0
    while True:
        sleep(1)
        try:
            status = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[2]/span').text
            t = strftime("%Y-%m-%d %H:%M:%S")
            print("{0} ->  {1}".format(curr_name[:3], status))

            if status=='online':
                show_status.config(text=' ONLINE ',fg='green')
                show_status.update_idletasks()
                sleep(1)
                show_status.config(text=' ', fg='white')
                show_status.update_idletasks()
                if ut:
                    pt=datetime.now()
                    ut=False
                if updateo:
                    print("At {0} {1} is online".format(t[11:] , curr_name[:3]) + '\n')
                    history.insert(0,"{} 📱  {} is Online".format(t[11:],curr_name[:3]) )
                    msg.append("{} -- {} is Online".format(t[11:], curr_name[:3]))
                    history.itemconfig(0, {'fg': 'green'})
                    updateo = False
                    updatef = True
                continue



            else:
                show_status.config(text=' OFFLINE ',fg='red')
                show_status.update_idletasks()
                updateo = True
                if updatef:
                    history.insert(0, "{} 📱  {} is Offline".format(t[11:],curr_name))
                    msg.append("{} -- {} is Offline".format(t[11:],curr_name))
                    history.itemconfig(0, {'fg': 'red'})
                    updatef = False


        except:
            updateo = True
            show_status.config(text=' OFFLINE ', fg='red')
            show_status.update_idletasks()
            t = strftime("%Y-%m-%d %H:%M:%S")
            if not ut:
                ct = datetime.now()
                print("{} duration of online".format(str(ct-pt)[:-7]))
                history.insert(0,"{} 📱  duration of online".format(str(ct-pt)[:-7]))
                msg.append("{} --  duration of online".format(str(ct-pt)[:-7]))
                ut=True

            if updatef:
                history.insert(0, "{} 📱  {} is Offline".format(t[11:], curr_name))
                msg.append("{} --  {} is Offline".format(t[11:], curr_name))
                history.itemconfig(0, {'fg': 'red'})

                updatef=False
            pass

# --- main ---



#driver
driver = None
current_path = os.getcwd()
root = tk.Tk()
root.geometry("880x620")
root.title('Whatsapp Monitor')
root.config(background='white')
root.wm_iconbitmap()





#link



#Frames bottom=Graph,top=Button,right=Pic&status
bf=tk.Frame(root,bg="red",borderwidth=1)
bf.pack(side='bottom',fill='y')

tf=tk.Frame(root,bg="white",relief='sunken')
tf.pack(side='top',fill='y')




rf=tk.Frame(root,bg="",borderwidth=1)
rf.pack(side='right',fill='y',pady=100)

mf=tk.Frame(root,bg="white",borderwidth=1)
mf.pack(fill='y')





# profile pic
img_path='pro.png'
image=Image.open(img_path)
width, height = image.size
image = image.resize((round(180 / height * width), round(280)))
img = ImageTk.PhotoImage(image)
panel = tk.Label(rf, image = img)
panel.place(x=0,y=0)
panel.pack(padx=20)



#name
name = tk.Label(rf,text="Name", fg='Black',bg='white',font="Helvetica 25 bold")
name.pack()

#status
show_status = tk.Label(rf,text="Status", fg='blue',bg='white',font="Helvetica 25 bold")
show_status.pack()







#Button in top frame
b = tk.Button(tf, text='Open WhatsApp Web', command=on_open)
b.pack()

b = tk.Button(tf, text='Start Monitor', command=monitor)
b.pack()



#Real Time Graph
#graph = tk.Label(bf,text="GRAPH will be plot here", fg='Black',font="Helvetica 35 bold")
#graph.pack(padx=180,pady=40)

#history

lishis = tk.Label(mf,text="History :: Offline", fg='black',bg='white',font="Helvetica 15 bold")
lishis.pack(pady=10)
history = tk.Listbox(mf,height=50,width=60,font="Helvetica 20 bold")



history.pack(pady=0)







#Menu

mymenu=tk.Menu(root)
mymenu.add_command(label="About",command=about)
mymenu.add_command(label="Exit",command=quit)
root.config(menu=mymenu)

root.mainloop()