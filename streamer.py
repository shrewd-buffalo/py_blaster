import subprocess, os, signal, sys


class Streamer(object):
    STREAM_CMD = "/usr/bin/dvblast -q -l -a 0 -f %s -c %s -m %s -b 8"
    PID_FILE = "dvblast.pid"
    CONFIG_FILE = "dvblast.config"
    CONFIG_ENTRY = "%s:%s 1 %s"
    MULTICAST_IP = "225.0.0.41"
    MULTICAST_PORT = "20000"

    def __init__(self, channel):
        self.channel = channel

    def stream(self):
        print("Streaming %s" % self.channel.getName())
        self.write_config()
        stream_args = self.STREAM_CMD % (self.channel.getFrequency(), self.CONFIG_FILE, self.channel.modulation)
        self.terminate_if_running()
        process = subprocess.Popen(stream_args.split(), )
        self.write_pid(process.pid)

    def write_config(self):
        f = open(self.get_file_location(self.CONFIG_FILE), 'w')
        f.write(self.CONFIG_ENTRY % (self.MULTICAST_IP, self.MULTICAST_PORT, self.channel.getChannelId()))
        f.close()

    def write_pid(self, pid):
        f = open(self.get_file_location(self.PID_FILE), 'w')
        f.write(str(pid))
        f.close()

    def is_running(self):
        os.getpgid()
        return True

    def get_pid(self):
        f = open(self.get_file_location(self.PID_FILE), 'r')
        pid = f.read()
        f.close()
        return pid

    def terminate_if_running(self):
        try:
            pid = self.get_pid()
            os.kill(int(pid), signal.SIGTERM)
        except OSError as e:
            # nothing to kill
            pass
        except FileNotFoundError as e:
            print("Nothing to kill, no PID found %s" % format(e))

    def get_file_location(self, file):
        return os.path.join(os.path.join(sys.path[0], file))

