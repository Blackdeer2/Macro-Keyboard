class EncoderMode:
    def __init__(self, name, left_cmd="", right_cmd="", alt_left_cmd="", alt_right_cmd=""):
        self.name = name
        self.left_cmd = left_cmd
        self.right_cmd = right_cmd
        self.alt_left_cmd = alt_left_cmd
        self.alt_right_cmd = alt_right_cmd

    def get_left_command(self, alt=False):
        return self.alt_left_cmd if alt and self.alt_left_cmd else self.left_cmd

    def get_right_command(self, alt=False):
        return self.alt_right_cmd if alt and self.alt_right_cmd else self.right_cmd

    def __repr__(self):
        return (f"EncoderMode(name='{self.name}', left='{self.left_cmd}', right='{self.right_cmd}', "
                f"alt_left='{self.alt_left_cmd}', alt_right='{self.alt_right_cmd}')")
