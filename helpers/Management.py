#TODO

class Management:

    def update_firmware(self):
        if self.is_debug:
            print ("%f HAL::update_firmware()" % time.time())

        cmd = 'apt update -y'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

        # TODO: double check
        cmd = 'apt install -y emacs-nox subversion python3 python3-pip git nodejs i2c-tools libgpiod-dev emacs-bin-common emacs-common libgpiod2 libsvn1 libapr1 libaprutil1 libserf-1-1 libutf8proc2'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)
          
        cmd = 'mount /dev/sda1 /mnt'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

        cmd = 'dpkg --force-overwrite -i /mnt/name/name-project-*.deb'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

        cmd = 'umount /mnt'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

    def save_logs(self):
        
        cmd = 'mount /dev/sda1 /mnt'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)
            
        cmd = 'cp /var/log/name/* /mnt/name/'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

        cmd = 'umount /mnt'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)

    def reboot(self):
        if self.is_debug:
            print ("%f HAL::reboot)" % time.time())
    
        cmd = 'reboot'
        output = subprocess.check_output(cmd, shell = True).decode('ascii')
        if self.is_debug:
            print (output, flush = True)
