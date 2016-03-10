import freenect
import sys
import cv
import frame_convert
import numpy as np
import serial, time
import math
import struct
import serial
import struct
import time
import datetime


CHARACTER_WIDTH = 20  # Number of characters that will fit on a line.
INSTRUCTION_DELAY = 0.01  # Number of seconds to wait between bytes.


class Pertelian(object):

  def __init__(self, tty='/dev/ttyUSB0'):
    self.ser = serial.Serial(tty)
    self.ser.isOpen()
    self._Setup()

  def __del__(self):
    """Close the serial connection when this object is destroyed."""
    self.ser.close()

  def _Setup(self):
    """Set up the display.

    Function set with 8-bit data length, 2 lines, and 5x7 dot size.
    Entry mode set; increment cursor direction; do not automatically shift.
    Cursor/display shift; cursor move.
    Display On; cursor off; do not blink.

    """
    for byte in (0x38, 0x06, 0x10, 0x0c, 0x01):
      self._SendInstruction(byte)

  def _SendBytes(self, bytesData, delay=INSTRUCTION_DELAY, pack='B'):
    """Send a stream of bytes to the Pertelian.

    Also, sleep for delay seconds between sending each byte.

    """
    for byte in struct.pack(pack * len(bytesData), *bytesData):
        self.ser.write(byte)
        time.sleep(delay)

  def _SendInstruction(self, byte):
    """Send an instruction byte to the Pertelian."""
    self._SendBytes((0xfe, byte))

  def Power(self, on):
    """Turn the power on or off."""
    if on:
      self._SendInstruction(0x0c)
    else:
      self._SendInstruction(0x08)

  def Backlight(self, on):
    """Turn the backlight on or off."""
    if on:
      self._SendInstruction(0x03)
    else:
      self._SendInstruction(0x02)

  def Clear(self):
    """Clear the display."""
    self._SendInstruction(0x01)

  def Message(self, msg):
    """Display a message."""
    self._SendBytes(msg, pack='c')

  def WrapMessage(self, msg):
    """Wrap messages to display on the Pertelian.

    TODO(damonkohler): Add support for words longer than CHARACTER_WIDTH and
    for new lines.

    """
    words = msg.split()
    lines = []
    line = words[0]
    for word in words[1:]:
      assert len(word) <= CHARACTER_WIDTH, 'Word too long.'
      if len(line) + len(word) < CHARACTER_WIDTH:
        line += ' ' + word
      else:
        lines.append(line.ljust(CHARACTER_WIDTH))
        line = word
    lines.append(line.ljust(CHARACTER_WIDTH))
    while len(lines) < 4:
      lines.append(' ' * CHARACTER_WIDTH)  # Add any missing blank lines.
    # The Pertelian displays lines a little out of order.
    self.Message(lines[0])
    self.Message(lines[2])
    self.Message(lines[1])
    self.Message(lines[3])


keep_running = True

def display_depth(dev, data, timestamp):
    global keep_running

    freenect.set_depth_mode(dev, freenect.RESOLUTION_HIGH, freenect.DEPTH_REGISTERED)
    #print(np.min(data))
    p.WrapMessage(str(np.min(data)))
    
    if (np.min(data) < 350 or np.min(data) == 2047):
        p.Backlight(0)
    else:
        p.Backlight(1)
    
    if cv.WaitKey(10) == 27:
        keep_running = False


def display_rgb(dev, data, timestamp):
    global keep_running
    cv.ShowImage('RGB', frame_convert.video_cv(data))
    if cv.WaitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill


print('Press ESC in window to stop')
p = Pertelian()

freenect.runloop(
    depth=display_depth,
    #video=display_rgb,
    body=body)
