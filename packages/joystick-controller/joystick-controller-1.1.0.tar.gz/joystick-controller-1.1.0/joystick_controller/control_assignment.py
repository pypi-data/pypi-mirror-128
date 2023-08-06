"""
MIT License
Copyright (c) 2021 Marcelo Jacinto
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author: Marcelo Fialho Jacinto
@email: marcelo.jacinto@tecnico.ulisboa.pt
@date: 25/11/2021
@licence: MIT
"""
import os
from typing import Dict
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time


def check_time_span_decorator(fnc):
    """
    Decorator function used to check the time-elapsed between consecutive function calls. This value
    is then passed on to the real function that will be executed
    :param fnc: A python function that receives a double as input (dt - time difference)
    :return: A function and the corresponding time-elapsed already received in the parameters
    """

    # Some setup for the first function call
    check_time_span_decorator.first_call = True
    if check_time_span_decorator.first_call:
        check_time_span_decorator.last_time = time.time()
        check_time_span_decorator.first_call = False

    # Define a wrapper function so that the "self" of the object can be passed to the function as well
    def wrapper(*args, **kwargs):
        # Compute the time difference between the previous and current function call
        dt = time.time() - check_time_span_decorator.last_time
        check_time_span_decorator.last_time = time.time()
        kwargs["dt"] = dt
        return fnc(*args, **kwargs)

    return wrapper


class ControlAssignment:
    """
    Data class used only to store the button assignments for the joystick and keyboard inputs
    NOTE: The keyboard inputs are "hard-coded" but the joystick values are customizable. This is an area for improvement
    in the future
    """

    def __init__(self, configurations):
        """
        Constructor for the class ControlAssignment. This class initializes pygame, a joystick and grabs the
        first joystick it finds. If more then one joysticks are connected to the system, then only one is picked and the
        others are ignored by default. This method receives a dictionary with all the button mappings.
        :param configurations: A dictionary that conforms to a scheme according to the following example
            {
            "surge": {"inputs":[
              {"type": "axis", "id": 1, "gain": -0.5, "offset": 0.0},
              {"type": "hat", "id": 0, "index": 1, "gain": 0.5, "offset": 0.0}],
            "integrate": false},

            "depth": {"inputs":[
              {"type": "button", "id": 8, "gain": -0.5, "offset": 0.0},
              {"type": "button", "id": 6, "gain": 0.5, "offset": 0.0}],
            "integrate": true,
            "lower_limit": -3,
            "upper_limit": 0}
            }

        The keys of the main dictionary are completely generic and instead of "surge" we could have any other name. But
        be careful, the name chosen in this configurations will be the also used as "key" for the output dictionary
        provided in the method 'check_events()'.

        Each control variable (such as "surge") must contain a dictionary with the following keys: 'inputs' and 'integrate'.
        If you want to limit the output values by the controller, you can also add the following (optional) keys: 'lower_limit'
        and 'upper_limit', for which the corresponding values are doubles.

        The value of 'inputs' must be a list of dictionaries that contain all the buttons/keys that can be assigned to a given
        control variable. Therefore, each control variables can have multiple buttons/keys assigned to it! These dictionarys must contain
        the following keys: 'type', 'id', 'gain', 'offset'
        - The key 'type' must have one of the following values: 'axis' (a.k.a analog joy), 'hat' (a.k.a d-pad), 'button'.
        - The key 'id' must have a positive int as a value (between 0 and some maximum value). These values depend from controller to controller and
        must be chosen manually (by trial and error). Fortunately, this library throws an ValueError exception
        with a warning if you go above the id of 'axis', 'hat' and 'button'. NOTE: the id of each of these modes
        are independent of each other, i.e. 'hat' with id=0 is different from 'button' with id=0. Moreover, this constructor
        will also print on the screen how many 'hats', 'buttons' and 'axis' the connected joystick provides.
        - The key 'gain' must be a double used to scale the inputs provided by the joystick (joystick inputs typically
        vary between [-1, 1] or [0, 1].
        - The key 'offset' must be a double and defines an offset which is summed to the controller input before
        being multiplied by the gain.
        NOTE: The key 'index' must be specified if the 'type' is 'hat' (a.k.a d-pad). It's type is either 0 or 1. The reason for this is that pygame
        stores this inputs in tuples and typically (but not always) (-1, 0) means left, (0, 1) means up, (-1, 1) means
        up and left keys pressed. We specify the index to select which one we want to read from.

        The values of the key 'integrate' must be either true or false. If true, the control variable will be integrated
        over-time as the key is pressed (and stored if the button is up). If false, the desired value is not integrated.
        This is useful to define speeds (not integrate) and desired positions (to integrate when the key is pressed)
        """

        # ---Initialize the pygame library and get the handle of the joystick (only considers the main joystick)
        # If multiple joysticks are connected to the system, they are ignored
        try:

            # Try to initiate pygame backend
            pygame.init()
            pygame.joystick.init()

            # Try to grab a joystick
            self.joystick_ = pygame.joystick.Joystick(0)

        # Handle a possible exception by creating our own (so that the end user does not have to deal with pygame costume exceptions!)
        except pygame.error as e:
            raise RuntimeError("Could not connect to a joystick or gamepad!")

        # --- Create a dictionary that maps possible inputs to functions---
        self.function_mapping_ = {"axis": lambda x: self.joystick_.get_axis(x),
                                  "hat": lambda x: self.joystick_.get_hat(x),
                                  "button": lambda x: self.joystick_.get_button(x)}

        # --- Create a dictionary with the maximum number of each input for the joystick that is plugged in
        self.validation_mapping_ = {"axis": self.joystick_.get_numaxes(),
                                    "hat": self.joystick_.get_numhats(),
                                    "button": self.joystick_.get_numbuttons()}

        # --- Save the configurations for each type of motion
        self.configurations_ = configurations

        # --- Create a desired inputs dictionary to store a desired input for each variable provided in the configurations
        self.desired_inputs_ = {}
        for config, config_value in self.configurations_.items():
            self.desired_inputs_[config] = 0.0

        # --- Validate if all the configurations are accepted by the current joystick
        self.validate_configurations__()
        

    def validate_configurations__(self):
        """
        Method used to validate the configurations dictionary received in the class constructor. If some value
        does not conform to the accepted standard a ValueError exception is raised
        """
        
        # Iterate through all the configurations for the surge, sway, heave and yaw
        for config, config_value in self.configurations_.items():

            # Check if the every configuration is itself a dictionary
            if not isinstance(config_value, dict):
                raise ValueError(
                    str("[" + config + "] " + "This structure must be a dictionary"))

            # Check if every variable specifies if it is integrable or not. If not, throw an error
            if "integrate" not in config_value:
                raise ValueError(
                    str("[" + config + "] " + "Every control variable should have a key 'integrate' and its respective boolean"))

            # Check if the value in integrate is a boolean
            if not isinstance(config_value["integrate"], bool):
                raise ValueError(str("[" + config + "] " + "Integrate key must have a boolean value (True/False)"))

            # Check if inputs is defined
            if "inputs" not in config_value:
                raise ValueError(
                    str("[" + config + "] " + "Every control variable should have a key 'inputs' and its respective list of inputs"))

            # Check if inside inputs we have a list
            if not isinstance(config_value["inputs"], list):
                raise ValueError(
                    str("[" + config + "] " + "Every control input must be a list of dictionaries"))

            # Check if there is an upper_bound variable, if it is a float
            if "upper_limit" in config_value and not (isinstance(config_value["upper_limit"], float) or isinstance(config_value["upper_limit"], int)):
                raise ValueError(
                    str("[" + config + "] " + "The upper limit value must be a float or int"))

            # Check if there is an upper_bound variable, if it is a float
            if "lower_limit" in config_value and not (isinstance(config_value["lower_limit"], float) or isinstance(config_value["lower_limit"], int)):
                raise ValueError(
                    str("[" + config + "] " + "The lower limit value must be a float or int"))

            # Iterate over the input list (each control variable can be controlled by several buttons or triggers)
            for control_method in config_value["inputs"]:

                # If the control method does not define a type, then throw an error
                if "type" not in control_method:
                    raise ValueError(str("[" + config + "] " + "Control input must have a 'type' key."))

                # Validate if the control method is a valid one
                if control_method["type"] not in self.function_mapping_:
                    raise ValueError(
                        str("[" + config + "] " + "Control input must have one of the following types: 'axis', 'hat' or 'button'"))

                # Check if control method has an 'id', 'gain' and 'offset' key
                if ("id" not in control_method) or ("gain" not in control_method) or ("offset" not in control_method):
                    raise ValueError(
                        str("[" + config + "] " + "Control input must have the following keys: 'id', 'gain' and 'offset'"))

                # Check the type of id
                if not isinstance(control_method["id"], int):
                    raise ValueError(
                        str("[" + config + "] " + "Control 'id' must be a positive int"))

                # Check the type of gain
                if not (isinstance(control_method["gain"], int) or isinstance(control_method["gain"], float)):
                    raise ValueError(
                        str("[" + config + "] " + "Control 'gain' must be either an int or float"))

                # Check the type of offset
                if not (isinstance(control_method["offset"], int) or isinstance(control_method["offset"], float)):
                    raise ValueError(
                        str("[" + config + "] " + "Control 'offset' must be either an int or float"))

                # If the control method is of type 'hat', then it must also have an 'index' key
                if control_method["type"] == "hat" and "index" not in control_method:
                    raise ValueError(
                        str("[" + config + "] " + "Control input of 'type'=hat must also contain an 'index' key"))

                # Check if the control method type is 'hat' and the indexes are between 0 and 1
                if control_method["type"] == "hat" and not 0 <= control_method["index"] <= 1:
                    raise ValueError(
                        str("[" + config + "] " + "Index must be either 0 or 1 for the hat control type"))

                # If the id assigned is not within the supported range values of the joystick, raise an error
                if control_method["id"] > self.validation_mapping_[control_method["type"]] or control_method[
                    "id"] < 0:
                    raise ValueError(str("[" + config + "] " + "Max. value for input of type " +
                                         str(control_method["type"]) + " is " +
                                         str(self.validation_mapping_[control_method["type"]] - 1)))

    @check_time_span_decorator
    def check_events(self, dt):
        """
        Loops through all the assigned controls and tracks whether a "button", "axis" or "hat" has been pressed or not.

        :param dt: The time difference between the previous function call and the current function call (in seconds)
        :return A dictionary with the same keys received in the configurations of the class constructor. The values
        for each key are computed according to:
                output = input_value_from_joystick + offset) * gain
                if integrate-> output = prev_output + (output * dt)
                output = max(min((output, upper_limit), lower_limit)
        NOTE: if having troubles configuring a remote, read the note near the end of this function
        """

        # ---Clean variables that are not integrable
        # For example, depth can be controlled using the analog joystick (axis) and a button. In this case, depth is
        # not a speed. It is a position that should increment of decrement the longer we press buttons

        # For each control variable (surge, sway, heave, etc.)
        for config, config_value in self.configurations_.items():

            # If it is not integrable, reset it's desired value
            if config_value["integrate"] == False:
                self.desired_inputs_[config] = 0.0

        # ---Make pygame check for joystick events---
        pygame.event.get()

        # Iterate through all the configurations for the config = surge, sway, heave, yaw, etc.
        for config, config_value in self.configurations_.items():

            # Iterate over the input methods list
            # (each control variable can be controlled by several buttons or triggers)
            for control_method in config_value["inputs"]:
                # Check the output of the (button->float 0 or 1), (axis->float range between -1 and 1)
                # or (hat-> tuple of (-1, 0))
                user_input = self.function_mapping_[control_method["type"]](control_method["id"])

                # Compute the new input value (note: here we have to handle the special case that the 'hat'/d-pad
                # returns a tupple and a not a float like the others. The first element of the tuple is typically
                # left_right (-1 or 1) and the second element of the tuple is typically up and down (-1 or 1)
                new_input = round(float(user_input), 2) if control_method["type"] != "hat" else round(
                    float(user_input[control_method["index"]]), 2)
                new_input += round(float(control_method["offset"]), 2)
                new_input *= round(float(control_method["gain"]), 2)

                # Check if this input should be integrated
                if config_value["integrate"]:
                    new_input *= dt

                # Sum the current input to the corresponding desired_inputs
                self.desired_inputs_[config] += new_input

                # Check if we should saturate the input or not
                if "lower_limit" in config_value and self.desired_inputs_[config] < config_value["lower_limit"]:
                    self.desired_inputs_[config] = config_value["lower_limit"]

                if "upper_limit" in config_value and self.desired_inputs_[config] > config_value["upper_limit"]:
                    self.desired_inputs_[config] = config_value["upper_limit"]

                # NOTE: if two triggers with the same function are pressed at the same time, their resulting outputs
                # will be summed

        # NOTES: Sometimes the controller analog sticks send a value different than zero even when stationary.
        # This can sometimes prove problematic, specially if a user defines a mix of analogue and digital buttons
        # to control a given variable as the (almost zero) value of the analogue can make the real value of a digital button
        # be ignored. For that matter, we round the joystick input to 2 decimal places. If this proves to not be enough
        # the offset variable can also be used to contradict this behaviour.
        # EXAMPLE OF WEIRD BEHAVIOUR THAT CAN ARISE (IF WE DID NOT USE ROUND):
        # The analog is sending 0.0025 for surge (in resting position)
        # This value stored in desired_inputs will be (0.0025 + offset) * gain
        # If offset = 0.0 and gain != 0, then the value stored in desired_inputs != 0.0
        # Then if the digital key is sending 1.0, this value will be ignored!
        return self.desired_inputs_
