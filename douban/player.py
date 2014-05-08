import subprocess

class Player:
    p = None

    @classmethod
    def play(cls, filename):
        cls.stop()
        cls.p = subprocess.call(["mpg123", filename])
        #out, error = cls.p.communicate()
        #return out, error

    @classmethod
    def stop(cls):
        try:
            if cls.p:
                cls.p.terminate()
                cls.p = None
        except:
            pass

