#!/usr/bin/env python3


class Terminal:
    def __init__(self, owner, t_type):
        self.owner_ = owner
        self.t_type_ = t_type
        self.node_ = None

    def __str__(self):
        return str(self.node_)

    def __repr__(self):
        ret = f'<{self.__class__.__name__}>'+str(self.node_)+"\n"
        return ret

    def set_node(self, node):
        if self.node_:
            self.node_.remove_terminal(self)
        node.add_terminal(self)
        self.node_ = node

    def get_node(self):
        return self.node_

    def get_name(self):
        return self.node_.get_name()

    def get_type_short(self):
        return self.t_type_[0]

    def get_owner_name(self):
        return self.owner_.get_name()


class Transistor:
    terminal_type = dict(gate=0, drain=1, source=2)

    def __init__(self, name, t_type):
        self.name_ = name
        self.t_type_ = t_type
        self.terminals = list()
        self.terminals.append(Terminal(self, 'gate'))
        self.terminals.append(Terminal(self, 'drain'))
        self.terminals.append(Terminal(self, 'source'))

    def get_terminal(self, t_idx):
        return self.terminals[t_idx]

    def get_terminal_with_type(self, t_type):
        return self.terminals[Transistor.terminal_type[t_type]]

    def get_terminal_with_short_type(self, s_type):
        if s_type == 'g':
            t_type = 'gate'
        elif s_type == 's':
            t_type = 'source'
        elif s_type == 'd':
            t_type = 'drain'
        else:
            raise ValueError(f'Type {s_type} is invalid')

        return self.terminals[Transistor.terminal_type[t_type]]

    def set_name(self, name):
        self.name_ = name

    def get_name(self):
        return self.name_

    def get_type(self):
        return self.t_type_

    def flip_type(self):
        if self.t_type_ == 'PMOS':
            self.t_type_ = 'NMOS'
        else:
            self.t_type_ = 'PMOS'

    def get_bulk(self):
        if self.t_type_ == 'PMOS':
            return 'VDD PMOS'
        else:
            return 'GND NMOS'

    def get_description(self, reverse_diffusions=False):
        ret = ''
        if reverse_diffusions:
            terminal_idx = (2, 0, 1)
        else:
            terminal_idx = (1, 0, 2)
        for i in terminal_idx:
            ret += str(self.terminals[i]) + ' '

        ret = f"{self.name_} {ret}{self.get_bulk()}\n"
        return ret

    def is_gate_same_as_one_diff(self):
        if self.terminals[0].get_name() == self.terminals[1].get_name():
            return True
        return self.terminals[0].get_name() == self.terminals[2].get_name()

    def __str__(self):
        return self.get_description()

    def __repr__(self):
        ret = f'<{self.__class__.__name__}>'+self.name_+"\n"
        for tx in self.terminals:
            ret += "\t" + repr(tx)
        return ret+"\n"
