import serial, time, re, psutil
from symbols import *

##############################################################
# We need to change permission for the usb file of the modem #
# To make a udev file adding a specific rule for this modem, #
# two parameter are necessary: idVendor and idProduct, found #
# with command: <lsusb -vvv> (look for ZTE modem in the list)#
# Udev file goes to: /etc/udev/rules.d/<50-filename.rules> ###
# Add the bellow line to the file: ###########################
# SUBSYSTEMS=="usb", ATTRS{idVendor}=="<idVendor_for_modem>", ATTRS{idProduct}=="<idProduct_for_modem>", GROUP="users", MODE="0666"
# In optiplex-7070-sc-2, idVendor=19d2 and idProduct=1589 ####
# Reload udev with command: <sudo udevadm control --reload> ##
# Insert (or take out and reinsert) modem in the usb slot ####
# Verify modem file permission with the bellow command: ######
# <stat /dev/ttyUSB0> ########################################
# Access must be with description (0666/crw-rw-rw) ###########
# Also, kill ModemManagement proccess with commands: #########
# <sudo lsof -t /dev/ttyUSB0> then <sudo kill proccess_id> ###
# Sometimes it's necessary kill, start, than kill again the ##
# ModemManager proccess. Use the following commands: #########
# <sudo service ModemManager status> (look for Main PID) #####
# <sudo kill process_ID> #####################################
# <sudo service ModemManager start> ##########################
# Keep ModemManager proccess killed! #########################
# Wait until the modem is ready, sometimes 60 seconds ########
##############################################################


class Modem:
    def __init__(self, path=usbmodemport, debug=False):
        self.path = path
        self.debug = debug
        self.msgnumber = None
        self.serial_connection = serial.Serial(path, baudrate=115200, timeout=5)
        self.serial_connection.reset_input_buffer()

    def send_to_modem(self, msg, sleep=0.2):
        self.serial_connection.write(msg.encode())
        # time.sleep(sleep)

    def get_answer(self, strt_sleep=0, sleep=0):
        time.sleep(strt_sleep)
        quantity = self.serial_connection.in_waiting
        ans = ''
        while True:
            if quantity > 0:
                ans += self.serial_connection.read(quantity).decode()
                # time.sleep(sleep)
            else:
                pass
                # time.sleep(sleep)
            quantity = self.serial_connection.in_waiting
            if quantity == 0:
                break
        if self.debug:
            print(ans)
        return ans

    def get_answer2(self):
        self.serial_connection.readline()
        while True:
            line = self.serial_connection.readline()
            if line == b'OK\r\n':
                return True
            if line == b'nOk\r\n':
                return False
            if line == b'NO CARRIER\r\n':
                return False

    def echo_mode(self, mode=1):
        if mode == 0:
            cmd = ATE0
        elif mode == 1:
            cmd = ATE1
        self.send_to_modem(cmd)
        ans = self.get_answer(sleep=0.2)
        return ans

    def send_command(self, cmd, sleep=2, endchar=CR):
        if endchar == 'ESC':
            endchar = chr(26)
        aux = cmd + endchar
        self.send_to_modem(aux)
        return self.get_answer(int(sleep))

    def reset(self):
        cmd = ATZ
        self.send_to_modem(cmd)
        ans = self.get_answer(sleep=2)
        return ans

    def verbose_on_error(self, turn=True):
        if turn:
            cmd = CMEE_1
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
        elif turn == False:
            cmd = CMEE_0
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
        return ans

    def set_mode(self, mode='text'):
        if mode == 'text':
            cmd = CMGF_1
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.5)
            return ans
        elif mode == 'PDU':
            return 'error on set_mode: PDU mode not implemented'
        else:
            return 'error on set_mode: option not supported'

    def write_to_storage(self, index, msg):
        cmd = CMGW + '"' + index + '"' + CR
        self.send_to_modem(cmd)
        ans = self.get_answer(sleep=0.2)
        if ans == '>':
            cmd = msg + SUB
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
            if '+CMGW:' in ans:
                pattern = '[\d]+'
                if re.search(pattern, ans) is not None:
                    for catch in re.finditer(pattern, ans):
                        msgnumber = catch[0]
                    return msgnumber
        return ans

    def send_from_storage(self, index):
        cmd = CMSS + str(index) + CR
        self.send_to_modem(cmd)
        ans = self.get_answer(sleep=0.2)
        return ans

    def set_storage_area(self, area='ME'):
        if area == 'ME':
            area = '"' + area + '"'
            cmd = CPMS + area + ','+ area + CR
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
            return ans

    #index = memory location of stored SMS, set storage area before using this.
    #flags:
    #0 = delete only selected message;
    #1 = ignore index (use any number), delete all received read;
    #2 = ignore index, delete all received read and stored sent;
    #3 = ignore index, delete all received read, stored unsent and stored sent;
    #4 = ignore index, delete all stored SMS messages;
    def clear_storage(self, index, flag=4):
        aux = str(index) + ',' + str(flag) + '\r'
        cmd = CMGD + aux
        self.send_to_modem(cmd)
        ans = self.get_answer(sleep=1)
        return ans

    def kill_modem_proc(self):
        for proc in psutil.process_iter():
            if proc.name() == 'ModemManager':
                proc.kill()
                print('Modem process killed')

    def initialize(self):
        self.reset()
        ans = self.reset()
        if self.debug == True:
            if ('OK' in ans) and ('nOK' not in ans):
                self.verbose_on_error()
            else:
                return ans
        if ('OK' in ans) and ('nOK' not in ans):
            self.set_mode(mode='text')
        else:
            return ans
        if ('OK' in ans) and ('nOK' not in ans):
            self.set_storage_area(area='ME')
        else:
            return ans
        if ('OK' in ans) and ('nOK' not in ans):
            return ans
        else:
            return ans

    #Operations Group number
    def sendsms(self, mode='direct', number='+5519997397443', msg='SMS message test.', clearmemo=True):
        if mode == 'direct':
            cmd = CMGS + '"' + number + '"' + CR
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
            if '>' in ans:
                cmd = msg + chr(26)
                self.send_to_modem(cmd)
                time.sleep(5)
                ans = self.get_answer()
            if msg and 'OK' in ans:
                return 'ok'
            else:
                return 'nOk'

        elif mode == 'indirect':
            cmd = CMGW + '"' + number + '"' + CR
            self.send_to_modem(cmd)
            ans = self.get_answer(sleep=0.2)
            if '>' in ans:
                cmd = msg + chr(26)
                self.send_to_modem(cmd)
                ans = self.get_answer(sleep=0.2)
                if '+CMGW:' in ans:
                    pattern = '[\d]+'
                    if re.search(pattern, ans) is not None:
                        for catch in re.finditer(pattern, ans):
                            msgnumber = catch[0]
                        if msgnumber.isnumeric():
                            cmd = CMSS + msgnumber + CR
                            self.send_to_modem(cmd)
                            ans = self.get_answer(sleep=4)
                            if ('OK' in ans) and ('nOK' not in ans):
                                if clearmemo:
                                    self.clear_storage(msgnumber)
                                    return ans
                            return ans
                return ans
            return ans

    def closeconnection(self):
        self.serial_connection.close()

# m = Modem(debug=True)
# m.send_to_modem(ATZ)

# m.sendsms(mode='indirect', number='+5519997397443', msg='teste')
# m.closeconnection()
