class Workstation:
    """Объект предметной области: Workstation."""

    def __init__(self, number, assigned_worker, tools, is_occupied):
        self.__number = number
        self.__assigned_worker = assigned_worker
        self.__tools = tools
        self.__is_occupied = is_occupied

    @property
    def number(self):
        return self.__number

    @property
    def assigned_worker(self):
        return self.__assigned_worker

    @property
    def tools(self):
        return self.__tools

    @property
    def is_occupied(self):
        return self.__is_occupied

    def assign_worker(self, worker):
        self.__assigned_worker = worker
        self.__is_occupied = True

    def release(self):
        self.__assigned_worker = None
        self.__is_occupied = False

    def add_tool(self, tool):
        self.tools.append(tool)

