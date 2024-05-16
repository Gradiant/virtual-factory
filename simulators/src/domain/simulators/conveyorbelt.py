from src.domain.simulators.Bottle import Bottle
from src.domain.simulators.flowable import FlowAble
import random
import string


class ConveyorBelt(FlowAble):
    '''
    :param width: width of the belt mm
    :type width: float
    :param speed: current speed at which the belt is moving (slots/s)width
    :type speed: int
    :param slots: number of slots in this belt
    :type slots: int
    :param mode:

        - cyclical. Items are placed at the start when they reach the end.

        - lineal. When items reach the end they are discarded (by the update() method)
    '''

    def __init__(self, params: dict):
        self._discarded_items = []
        self._moving = False  # whether the belt is moving or not
        super().__init__(params)
        self._speed = params.get("speed", 1)
        self._discarded_items = [None] * self._speed
        self._slots = params.get("slots")
        self._mode = params.get("mode", 'lineal')
        self._flowable_inputs = params.get('flowable_inputs')

        self.notify()

        self._curr_speed = self._speed
        self._curr_pos = 0  # current position of the converyor belt (relative to its first position)
        self._belt = {}  # list of items currently on the conveyor belt. Free spaces contain 'None'

        self._slot_availability_around_input = [0] * (len(self._flowable_inputs) + 2)
        self._slot_availability = [0] * self._slots

        for i in range(self._slots):
            self._belt[i] = None

        if self._logging:
            self._dont_log_variables.extend(['_flowable_inputs'])

    def internal_run(self):
        info = self.read_industrial_info(self.get_read_info_for_industry())
        self.set_moving(info.get("onoff"))
        self.manip_belt_items()

        self.shift_items()
        self.check_available_slots()
        self.notify()
        self.write_industrial_info(self.get_write_info_for_industry())
        if __debug__:
            print("Cinta: {} - moving: {} - speed: {}, elements: {}".format(self._name, self._moving, self._speed, self.__str__()))

    def get_msg_to_notify(self) -> dict:
        items_out = []
        for x in self._discarded_items:
            if x is None:
                items_out.append(None)
            else:
                items_out.append(x.__dict__)
        msg_to_notify = {"input_blocked": False}
        msg_to_notify.update({"items_out": items_out})
        return msg_to_notify

    def get_read_info_for_industry(self) -> list:
        return ["onoff"]

    def get_write_info_for_industry(self):

        msg_for_industry = {"onoff": self._moving}
        for ndx, _slot in enumerate(self._slot_availability_around_input):
            msg_for_industry.update({f"availslot{ndx+1}": _slot})

        return msg_for_industry

    def manip_belt_items(self):
        '''
        Manipulates the items on the conveyor belt according to the message received.
        '''
        for _input in self._inputs:
            if not _input._input_blocked:
                pos = self._flowable_inputs[_input._name]._position
                pour_amount = _input._output_level

                if self._belt[pos] is not None:  # no necesario si el script de FUXA desactiva el recolectorvalve
                    if __debug__:
                        print(f"Cinta {self._name}: Echando {pour_amount}L en slot {pos}")
                    self._belt[pos].fill(pour_amount)

    def add_item(self, item, st_pos):
        '''
        Places an item on the conveyor belt at the specified location.

        :param item: item  to be added.
        :type item: Item
        :param st_pos: position of the station making this operation.
        :type st_pos: int
        '''
        if self._belt[st_pos] is None:
            self._belt[st_pos] = item

    def remove_item(self, st_pos):
        '''
        Removes an item from the conveyor belt at the specified location.

        :param st_pos: position of the station making this operation.
        :type st_pos: int
        :rtype: The item removed
        '''
        item = self._belt[st_pos]
        self._belt[st_pos] = None
        return item

    def start_stop(self):
        '''
        Toggles the state of the conveyor belt. If it's stopped, this method will make it operational and viceversa
        '''
        self._moving = not self._moving

    def shift_items(self):
        '''
        Moves the items in the conveyor belt and sends a message to the broker when it's available to stations.

        :param delta: time to simulate the belt moving.
        :type delta: float
        '''
        if self._moving:
            self._curr_pos += self._speed
            shift_pos_by = int(self._speed)
            if self._curr_pos >= self._slots:
                self._curr_pos = 0
            # move the items by 'self._speed' positions
            if self._mode == 'cyclical':
                aux_list = list(self._belt.values())[-shift_pos_by:] + list(self._belt.values())[:-shift_pos_by]
                i = 0
                for k in self._belt.keys():
                    self._belt[k] = aux_list[i]
                    i += 1
                for n in range(0, shift_pos_by):
                    if self._belt[n] is None:    # TODO quitar
                        params = {"_code": ''.join(random.choices(string.hexdigits, k=4)),
                                  "_width": 1,
                                  "_height": 2,
                                  "_weight": 0.1,
                                  "_capacity": 0.5,
                                  "_level": 0.0}
                        b = Bottle(params)
                        self._belt[n] = b
            elif self._mode == 'lineal':
                discards_list = list(self._belt.values())[-shift_pos_by:]
                empty_list = [None] * shift_pos_by
                aux_list = empty_list + list(self._belt.values())[:-shift_pos_by]
                i = 0
                for k in self._belt.keys():
                    self._belt[k] = aux_list[i]
                    i += 1
                for n in range(0, shift_pos_by):
                    if self._belt[n] is None:    # TODO quitar
                        params = {"_code": ''.join(random.choices(string.hexdigits, k=4)),
                                  "_width": 1,
                                  "_height": 2,
                                  "_weight": 0.1,
                                  "_capacity": 0.5,
                                  "_level": 0.0}
                        b = Bottle(params)
                        self._belt[n] = b
                self._discarded_items = discards_list
        else:
            self._discarded_items = [None] * self._speed

    def __str__(self):
        '''
        Returns a string with codes representing the items on the conveyor belt
        '''
        ret = ''
        for v in self._belt.values():
            ret += " " + str(v)
        return ret.strip()

    def set_moving(self, moving: bool):
        self._moving = moving

    def set_speed(self, speed: int):
        self._speed = speed

    def check_available_slots(self):
        # para un unico input
        for key in self._flowable_inputs:
            first_key = key
            break
        # informamos una posición antes, la suya y una despues
        pos = self._flowable_inputs[first_key]._position
        ndx = pos - 1 if pos > 0 else 0

        for n in range(len(self._slot_availability_around_input)):
            item = self._belt[ndx]
            if item is not None:
                if item.can_be_filled():
                    self._slot_availability_around_input[n] = True
                else:
                    self._slot_availability_around_input[n] = False
            else:
                self._slot_availability_around_input[n] = False
            ndx += 1

        for n in range(len(self._belt)):
            item = self._belt[n]
            if item is not None:
                if item.can_be_filled():
                    self._slot_availability[n] = True
                else:
                    self._slot_availability[n] = False
            else:
                self._slot_availability[n] = False

    def dict_for_log(self):
        ret_dict = super().dict_for_log()
        ret_dict['_belt'] = self.__str__()
        discarded_items = ret_dict['_discarded_items']
        if discarded_items is not None:
            discarded_items_types = set(map(type, discarded_items))
            if discarded_items_types == set([type(None)]):
                ret_dict['_discarded_items'] = None
            else:
                for ndx, value in enumerate(ret_dict['_discarded_items']):
                    if value is not None:
                        ret_dict['_discarded_items'][ndx] = value.__str__()
        return ret_dict
