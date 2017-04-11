import os,sys

scriptdir=os.path.dirname(os.path.realpath(__file__))

DNAME=input("Please Input Device Name:")

os.system("sudo apt-get install tmux lftp omxplayer feh unclutter vsftpd vim")
os.system("sudo chmod +777 %s/stopit.sh"%scriptdir)
os.system("sudo chmod +777 %s/adplay.sh"%scriptdir)

os.system("sudo sed -i 's/GD-01/%s/g' %s/adplay.py"%(scriptdir,scriptdir))
os.system("sudo sed -i 'N;4%s/adplay.sh' /etc/rc.local"%scriptdir)
