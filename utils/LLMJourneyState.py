class LLMJourneyState:
    """
    Manages the state and associated messages of interactive buttons used in a GPT-powered journey.

    Attributes:
        button_messages (dict): Maps button names (e.g., "button1") to their associated message text.
        button_states (dict): Tracks whether each button has been pressed (True) or not (False).
    """

    def __init__(self):
        self.button_messages = {}
        self.button_states = {}

    def set_button_messages(self, sessionObject):
        """
        Replaces the current button messages with the contents of the given session object.

        Args:
            sessionObject (dict): A dictionary mapping button names to messages.
        """
        self.button_messages = sessionObject

    def setup_button_state(self, button_name):
        """
        Marks a specific button as pressed by setting its state to True.

        Args:
            button_name (str): The name of the button to mark as pressed.
        """
        self.button_states[button_name] = True

    def setup_button_messages(self, options):
        """
        Assigns each option string in the list to a sequentially numbered button.

        Example:
            options = ["Yes", "No"]
            Resulting button_messages = {"button1": "Yes", "button2": "No"}

        Args:
            options (list of str): List of message options to assign to buttons.
        """
        for i, option in enumerate(options):
            self.button_messages[f"Option {i+1}"] = option

    def reset_message_states(self):
        """
        Clears all stored button messages.
        """
        self.button_messages = {}

    def reset_button_states(self):
        """
        Resets all button states to False for the currently defined buttons.
        """
        for btname in self.button_messages.keys():
            self.button_states[btname] = False

    def get_all_button_messages(self):
        """
        Retrieves the complete dictionary of button messages.

        Returns:
            dict: A mapping of button names to messages.
        """
        return self.button_messages

    def get_all_button_states(self):
        """
        Retrieves the complete dictionary of button states.

        Returns:
            dict: A mapping of button names to their current states (True/False).
        """
        return self.button_states

    def get_button_message(self, button_name):
        """
        Gets the message assigned to a specific button.

        Args:
            button_name (str): The name of the button.

        Returns:
            str or None: The message text if found, else None.
        """
        return self.button_messages.get(button_name)

    def get_button_state(self, button_name):
        """
        Gets the current state of a specific button.

        Args:
            button_name (str): The name of the button.

        Returns:
            bool or None: True if pressed, False if not, or None if undefined.
        """
        return self.button_states.get(button_name)


    def button_state_init(self):
        self.button_states = {}

    def button_message_init(self):
        self.button_messages = {}