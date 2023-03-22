#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ process.py                [Created: 2023-02-05 | 10:45 - AM]  #
#                                       [Updated: 2023-02-10 |  4:53 - PM]  #
#---[Info]------------------------------------------------------------------#
#  Execute command and prompt the STDOUT and STDERR                         #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
#  Thomas Pellissier (MyMeepSQL)                                            #
#  Jonas Petitpierre (Bashy)                                                #
#---[Operating System]------------------------------------------------------#
#  Developed for Linux                                                      #
#---[License]---------------------------------------------------------------#
#  GNU General Public License v3.0                                          #
#  -------------------------------                                          #
#                                                                           #
#  This program is free software; you can redistribute it and/or modify     #
#  it under the terms of the GNU General Public License as published by     #
#  the Free Software Foundation; either version 2 of the License, or        #
#  (at your option) any later version.                                      #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             #
#  GNU General Public License for more details.                             #
#                                                                           #
#  You should have received a copy of the GNU General Public License along  #
#  with this program; if not, write to the Free Software Foundation, Inc.,  #
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              #
#---------------------------------------------------------------------------#

# Import section
import os
import time
import signal
from subprocess import Popen, PIPE

## Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
class Process(object):
    '''
    Represents a running/ran process 
    '''

    @staticmethod
    def devnull():
        '''
        Helper method for opening devnull 
        '''
        return open('/dev/null', 'w')

    @staticmethod
    def call(command, cwd=None, shell=False):
        '''
        Calls a command (either string or list of args).
        Returns tuple:
            (stdout, stderr)
        '''
        if type(command) is not str or ' ' in command or shell:
            shell = True
            if Configuration.verbose >= 1:
                Color.pe('  {&} Executing (Shell): {B}%s{W}' % command)
        else:
            shell = False
            if Configuration.verbose >= 1:
                Color.pe('  {&} Executing: {B}%s{W}' % command)

        pid = Popen(command, cwd=cwd, stdout=PIPE, stderr=PIPE, shell=shell)
        pid.wait()
        (stdout, stderr) = pid.communicate()

        # Python 3 compatibility
        if type(stdout) is bytes: stdout = stdout.decode('utf-8')
        if type(stderr) is bytes: stderr = stderr.decode('utf-8')

        if Configuration.verbose >= 2 and stdout is not None and stdout.strip() != '':
            Color.pe('  {#}{P} [stdout] %s{W}' % '\n  {#}{P} [stdout] '.join(stdout.strip().split('\n')))
        if Configuration.verbose >= 2 and stderr is not None and stderr.strip() != '':
            Color.pe('  {#}{P} [stderr] %s{W}' % '\n  {#}{P} [stderr] '.join(stderr.strip().split('\n')))

        return (stdout, stderr)

    @staticmethod
    def exists(program):
        '''
        Checks if program is installed on this system 
        '''
        p = Process(command=f'which {program}')
        stdout = p.stdout().strip()
        stderr = p.stderr().strip()

        if stdout == '' and stderr == '':
            return False

        return True

    def __init__(self, command, devnull=False, stdout=PIPE, stderr=PIPE, cwd=None, bufsize=0, stdin=PIPE):
        '''
        Starts executing command 
        '''

        if type(command) is str:
            # Commands have to be a list
            command = command.split(' ')

        self.command = command

        if Configuration.verbose >= 1:
            Color.pe('  {&} Executing: {B}%s{W}' % ' '.join(command))

        self.out = None
        self.err = None
        if devnull:
            sout = Process.devnull()
            serr = Process.devnull()
        else:
            sout = stdout
            serr = stderr

        self.start_time = time.time()

        self.pid = Popen(command, stdout=sout, stderr=serr, stdin=stdin, cwd=cwd, bufsize=bufsize)

    def __del__(self):
        '''
        Ran when object is GC'd.
        If process is still running at this point, it should die.
        '''
        try:
            if self.pid and self.pid.poll() is None:
                self.interrupt()
        except AttributeError:
            pass

    def stdout(self):
        '''
        Waits for process to finish, returns stdout output
        '''
        self.get_output()
        if Configuration.verbose >= 2 and self.out is not None and self.out.strip() != '':
            Color.pe('  {#}{P} [stdout] %s{W}' % '\n  {#}{P} [stdout] '.join(self.out.strip().split('\n')))
        return self.out

    def stderr(self):
        '''
        Waits for process to finish, returns stderr output
        '''
        self.get_output()
        if Configuration.verbose >= 2 and self.err is not None and self.err.strip() != '':
            Color.pe('  {#}{P} [stderr] %s{W}' % '\n  {#}{P} [stderr] '.join(self.err.strip().split('\n')))
        return self.err

    def stdoutln(self):
        return self.pid.stdout.readline()

    def stderrln(self):
        return self.pid.stderr.readline()

    def stdin(self, text):
        if self.pid.stdin:
            self.pid.stdin.write(text.encode('utf-8'))
            self.pid.stdin.flush()

    def get_output(self):
        '''
        Waits for process to finish, sets stdout & stderr
        '''
        if self.pid.poll() is None:
            self.pid.wait()
        if self.out is None:
            (self.out, self.err) = self.pid.communicate()

        if type(self.out) is bytes:
            self.out = self.out.decode('utf-8')

        if type(self.err) is bytes:
            self.err = self.err.decode('utf-8')

        return (self.out, self.err)

    def poll(self):
        '''
        Returns exit code if process is dead, otherwise 'None'
        '''
        return self.pid.poll()

    def wait(self):
        self.pid.wait()

    def running_time(self):
        '''
        Returns number of seconds since process was started
        '''
        return int(time.time() - self.start_time)

    def interrupt(self, wait_time=2.0):
        '''
        Send interrupt to current process.
        If process fails to exit within `wait_time` seconds, terminates it.
        '''
        try:
            pid = self.pid.pid
            cmd = self.command
            if type(cmd) is list:
                cmd = ' '.join(cmd)

            if Configuration.verbose >= 1:
                Color.pe('  {&} Sending interrupt to PID %d (%s)' % (pid, cmd))

            os.kill(pid, signal.SIGINT)

            start_time = time.time()  # Time since Interrupt was sent
            while self.pid.poll() is None:
                # Process is still running
                time.sleep(0.1)
                if time.time() - start_time > wait_time:
                    # We waited too long for process to die, terminate it.
                    if Configuration.verbose > 1:
                        Color.pe('\n  {&} Waited > %0.2f seconds for process to die, killing it' % wait_time)
                    os.kill(pid, signal.SIGTERM)
                    self.pid.terminate()
                    break

        except OSError as e:
            if 'No such process' in e.__str__():
                return
            raise e  # process cannot be killed

