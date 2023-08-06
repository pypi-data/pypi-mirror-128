# prog: DAC81416 <- Rasberry Pie 4
# progman: Basil G
# started: 29-Sep-2021
# last changes: 08-Oct-2021

from gpiozero import OutputDevice

#DAC81416:
DAC_RANGE_VOLTS=5.0 #5.0 #-2.5...+2.5
DAC_RANGE_BITS=16
DAC_CHANNELS=16
DAC_BIN_MAX=65536   #2^DAC_RANGE_BITS
ACCESS_LEN=24       #word len
MSB_MASK=0x800000   #bit's ACCESS_LEN-1
# see slaseo0a.pdf page 28
CMD_WRITE=0x00
CMD_READ=0x800000   #bit 23 - RW: 0=write, 1=read
#Registers:
DEVICEID=0x01       #= 0x29C (668) + 2bits for version ID (=0) (for DAC81416)
STATUS=0x02         #bit0=1->T>140, bit1==1->busy, bit2==1->CRC error
SPICONFIG=0x03      #active mode, no streaming,standalone (no daisy-chain),24bit (ACCESS_LEN,no frame error checking),no toggle (unipolar out)
GENCONFIG=0x04      #bit14=1-powers down the internal reference, 0-activates
BRDCONFIG=0x05      #1-updates output to the value set in BDRCAST register, 0-output stays uneffected
SYNCCONFIG=0x06     #1-update on LDAC (sync mode), 0-update immediate (async mode)
TOGCONFIG0=0x07
TOGCONFIG1=0x08
DACPWDWN=0x09       #1-power down DAC
DACRANGE0=0x0A
DACRANGE1=0x0B
DACRANGE2=0x0C
DACRANGE3=0x0D
TRIGGER=0x0E        #LDAC=0x10   #bit=1 - sync load DAC (according to SYNCCONFIG register)
BRDCAST=0x0F        #broadcast value reg.
DAC0=0x10

def writeword(b):               # MSB-to-LSB ordered
    MOSI = OutputDevice(10)  # pin 19
    SCLK = OutputDevice(11)  # pin 23
    CE = OutputDevice(8)  # pin 24

    CE.off()                    # Enable data loading from SDI pin to shift register
    SCLK.off()                  # Start with clock low
    for i in range(ACCESS_LEN): # Send bits 23..0
        if b & MSB_MASK: MOSI.on()  #bit's 23 mask - MSB
        else: MOSI.off()
        b <<= 1                 # Shift left to MSB
        SCLK.on()               # rising edge: load SDI data into shift register
        SCLK.off()              # revert clock low        
    CE.on()                     # Execute the action specified in registers

def dac_init():
    #dac mode
    cmd=SPICONFIG<<16  | 0x00<<8 | 0x84   #SDO_EN=1 DEV_PWDWN=0  # see slaseo0a.pdf page 35
    writeword(cmd)
    cmd=GENCONFIG<<16  | 0x7F<<8 | 0x00   #REF_PWDWN # see slaseo0a.pdf page 36
    writeword(cmd)
    cmd=BRDCONFIG<<16  | 0x00<<8 | 0x00   #no broadcasting
    writeword(cmd)
    cmd=SYNCCONFIG<<16 | 0x00<<8 | 0x00  #0-immediate update - asynchronous, 1- synchronous update on LDAC
    writeword(cmd)
    cmd=TOGCONFIG0<<16 | 0x00<<8 | 0x00  #no toggle
    writeword(cmd)
    cmd=TOGCONFIG1<<16 | 0x00<<8 | 0x00  #no toggle
    writeword(cmd)
    #dac range see slaseo0a.pdf page 48
    B=0xEEEE                             #hardcoded range -2.5..+2.5 V;  see slaseo0a.pdf page 42
    cmd=DACRANGE0<<16 | B
    writeword(cmd)
    cmd=DACRANGE1<<16 | B
    writeword(cmd)
    cmd=DACRANGE2<<16 | B
    writeword(cmd)
    cmd=DACRANGE3<<16 | B
    writeword(cmd)
    #power up all of the dacs for this board
    cmd=DACPWDWN<<16 | 0x0000
    writeword(cmd)

def Volts2Bin(volts):   # see slaseo0a.pdf page 23  ==>volts=(binval/65536)*DAC_RANGE_VOLTS + 0
    if volts>=2.5: volts=2.49999
    if volts<=-2.5: volts=-2.5  
    binval=int((volts+2.5)*DAC_BIN_MAX/DAC_RANGE_VOLTS)
    return binval

def SetGain(G): #setup all the DACs' ouputs!!!
    dac_init() #single board
    for A in range(len(G)):
        V = G[A] * 0.00517 - 0.62
        U=Volts2Bin(V)
        cmd=(DAC0+A)<<16 | U
        writeword(cmd)
    return "ok"    
    
#eof dac81416.py
