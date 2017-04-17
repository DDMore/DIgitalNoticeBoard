from intro_to_flask import app
from flask import render_template,request,flash,session,url_for, redirect
#from flask.ext.mail import Message,Mail
#mail=Mail()
#import RPi.GPIO as GPIO

from models import db,User

main()


LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
"""
"""
def main():
  # Main program block

  # Initialise display
  lcd_init()

  # Toggle backlight on-off-on
  GPIO.output(LED_ON, True)
  time.sleep(1)
  GPIO.output(LED_ON, False)
  time.sleep(1)
  GPIO.output(LED_ON, True)
  time.sleep(1)

  # Send some centred test
  
  # Turn off backlight
  GPIO.output(LED_ON, False)

def lcd_init():
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   








x=0
data1="Welcome to IT Dept"





'''********************************************************'''





@app.route("/about1")
def about2():
    return render_template("web.html")


'''***********************************************************'''



  
@app.route("/change", methods=['POST'])
def change():
 if request.method == 'POST':
    # Getting the value from the webpage
    global data1
    global x
    data1 = request.form['lcd']
    x=1
    shownotice()
    return render_template('web.html', value=data1)


    
def shownotice():
   global data1
   print(data1*10)
   lcd_byte(LCD_LINE_1, LCD_CMD)
   lcd_string(data1,1)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string(time.strftime("%m/%d/%Y"),2)
   print(data1)
   length=len(data1);
   index=1
   cnt=1
   while(index+16<=length):
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string(data1[index:],1)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(time.strftime("%m/%d/%Y"),2)
        index=index+1
        time.sleep(0.5)
        if(index+16==length):
          index=0
          cnt=cnt+1 
          if(cnt==3):
            index=0
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string(data1[index:],1)
            break
   return render_template('web.html', value=data1)












@app.route('/testdb')
def testdb():
         user = User.query.filter_by(email = 'dnyaneshawar38more@gmail.com').first()	
         if user:
                 return user.username
         
@app.route('/')
def root():
	return render_template('index.html')



@app.route('/signup',methods=['POST','GET'])
def signup():
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            confirmpassword=request.form['confirmpassword']
            email=request.form['email']
            username=username.strip()
            password=password.strip()
            email=email.strip()
            confirmpassword=confirmpassword.strip()
            user = User.query.filter_by(username = username).first()
            if user:
             return user.username+"  Already registered "
            if confirmpassword==password:
                    newuser = User(username,email, password)
                    db.session.add(newuser)
                    db.session.commit()
        return render_template('signup.html')



@app.route('/login',methods=['POST','GET'])
def login():
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            # confirmpassword=request.form['confirmpassword']
            #email=request.form['email']
            username=username.strip()
            password=password.strip()
            #email=email.strip()
            #confirmpassword=confirmpassword.strip()
            user = User.query.filter_by(username = username).first()
            #if 'username' not in session:
                    
            if user:
                    session['username']=user.username;
                    return redirect(url_for('user'))
                    """return user.username+"  Already registered "
                    if confirmpassword==password:
                    newuser = User(username,email, password)
                    db.session.add(newuser)
                    db.session.commit()"""
            
            #render_template('login.html')    
        
        if 'username'  in session:
                    return redirect(url_for('user'))                    
        else:
                return render_template('login.html')


@app.route('/user',methods=['POST','GET'])
def user():
        if 'username' not in session:
            return redirect(url_for('login'))
        user = User.query.filter_by(username = session['username']).first()
 
        if user is None:
            return redirect(url_for('login'))
        else:
           return render_template('user.html',data=(session['username'],))


        
@app.route('/signout')
def signout():
 
  if 'username' not in session:
    return redirect(url_for('signin'))
     
  session.pop('username', None)
  return redirect(url_for('/'))
