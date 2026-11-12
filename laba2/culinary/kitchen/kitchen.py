class Kitchen:
    """Объект предметной области: Kitchen."""

    def __init__(self, name, workstations, equipment, cleanliness_level):
        self.__name = name
        self.__workstations = workstations
        self.__equipment = equipment
        self.__cleanliness_level = cleanliness_level

    @property
    def name(self):
        return self.__name

    @property
    def workstations(self):
        return self.__workstations

    @property
    def equipment(self):
        return self.__equipment

    @property
    def cleanliness_level(self):
        return self.__cleanliness_level

    def add_workstation(self, workstation):
        self.workstations.append(workstation)

    def register_equipment(self, equipment):
        self.equipment.append(equipment)

    def is_clean(self, minimum=80):
        return self.cleanliness_level >= minimum

