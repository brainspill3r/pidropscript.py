# pidropscript.py
Pimoroni Display Hat Mini - Implant/Dropbox script - Using the four tacticle buttons to test connections/flush/renew IP'S/Display Custom Image/ Make the screen go black 

Enable root login at startup, so that any of the commands we do throughout the entire process and when the dropbox is finished has no complications. 
*please note best practice is to have a user, but for ease of something not going wrong because of a issue with permissions, I prefer to use auto login as root to avoid any issues. 

CMD = sudo nano /etc/lightdm/lightdm.conf

CMD = uncomment #autologin-user=root (you may have to type in root if missing)

CMD =sudo reboot
On reboot we will be root. 

The display is what caused me the most amount of headaches and research, the display I have is 340x240 and I wanted the tactile buttons to have a purpose but to also be affective in what they could do. 

In order to get the displayhatmini screen to function the way I got it to function follow these steps. 

Check that your dtparam=spi=on is uncommented in the /boot/config.txt file.  Then git clone both of these repos; 

https://github.com/pimoroni/st7789-python
https://github.com/pimoroni/displayhatmini-python

And install all of the dependencies. 
You will also need to enable spi & i2c. 
 
Once we have these settings. We can use the pidropscript.py code which will. 

Button A - Show current connections. ( Good for pressing when you’ve plugged into a companies network)
Button B - Renews and flush all IPs connected (Once connected flush and renew the IP’s)
Button X - Show a custom image of your choice. (I use our company logo (Why not, had a button spare)
Button Y - Blacks out the screen ( Usually the last button to press on a real red team engagement) 
