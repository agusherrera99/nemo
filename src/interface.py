from argparse import ArgumentParser

class Interface:
    def __init__(self) -> None:
        self.parser = ArgumentParser(prog="Nemo", description="CLI task manager")