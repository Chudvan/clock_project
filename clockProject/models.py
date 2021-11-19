from peewee import *
import datetime

db = SqliteDatabase(None)


class BaseModel(Model):

    class Meta:
        database = db

    @staticmethod
    def panels():
        arr = []
        ind = 1
        for i in Panel.select(Panel.name,Panel.description).distinct():
            arr.append([ind, i.name, i.description])
            ind += 1
        return arr

    @staticmethod
    def createNewPanel(name, description):
        Panel.create(name=name, description=description)

    @staticmethod
    def getClockFaceByPanelName(panelName):
        return [(i.name, i.UTC, i.mode) for i in ClockFace().select().join(Panel).where(Panel.name == panelName).distinct()]

    @staticmethod
    def getPanelByPanelName(panelName):
        return Panel.get(name=panelName)

    @staticmethod
    def createClockFace(name, mode, UTC, panel, created_at=None, ends_at=None):
        if mode == 1:
            ClockFace.create(name=name, mode=mode, UTC=UTC, panel=panel)
        elif mode == 2:
            ClockFace.create(name=name, mode=mode, UTC=UTC,
                             created_at=created_at, ends_at=ends_at, panel=panel)
        else:
            raise Exception('mode: 1 or 2')


class Panel(BaseModel):
    panelId = PrimaryKeyField(null=False)
    name = CharField(max_length=50)
    description = CharField(max_length=100)


class ClockFace(BaseModel):
    clockId = PrimaryKeyField(null=False)
    name = CharField(max_length=50)

    MODE = (
        (1, 'CURRENT'),
        (2, 'COUNTDOWN')
    )
    mode = IntegerField(choices=MODE)
    UTC = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    ends_at = DateTimeField(null=True)
    panel = ForeignKeyField(Panel)


def initDatabase():
    panelEntries = [['Текущее время', 'Отображает время в разных городах мира.', None],
                    ['Время забега', 'Отображает время забега на дистанцию 100 м.', None],
                    ['Время выдачи билета', 'Отображает время выдачи билета.', None]]
    for entry in panelEntries:
        try:
            entry[2] = Panel.get(name=entry[0], description=entry[1])
        except DoesNotExist:
            entry[2] = Panel.create(name=entry[0], description=entry[1])
    current_time_panel = panelEntries[0][2]
    sprint_time_panel = panelEntries[1][2]
    exam_time_panel = panelEntries[2][2]

    current_date_time = datetime.datetime.now()
    clockFaceEntries = [['Moscow', 1, 3, None, current_time_panel],
                        ['New York', 1, -5, None, current_time_panel],
                        ['Tokyo', 1, 9, None, current_time_panel],
                        ['Демидов Артём Камильевич', 2, 3, None, sprint_time_panel,
                         current_date_time, current_date_time + datetime.timedelta(seconds=13.9)],
                        ['Зотов Руслан Андреевич', 2, 3, None, sprint_time_panel,
                         current_date_time, current_date_time + datetime.timedelta(seconds=14.3)],
                        ['Михайлова Василиса Владиславовна', 2, 3, None, exam_time_panel,
                         current_date_time, current_date_time + datetime.timedelta(minutes=45)],
                        ['Владимирова Виктория Дмитриевна', 2, 3, None, exam_time_panel,
                         current_date_time, current_date_time + datetime.timedelta(minutes=45)]]
    for entry in clockFaceEntries:
        try:
            entry[3] = ClockFace.get(name=entry[0], mode=entry[1], UTC=entry[2], panel=entry[4])
        except DoesNotExist:
            if entry[1] == 1:
                entry[3] = ClockFace.create(name=entry[0], mode=entry[1], UTC=entry[2], panel=entry[4])
            elif entry[1] == 2:
                entry[3] = ClockFace.create(name=entry[0], mode=entry[1], UTC=entry[2],
                                            created_at=entry[5], ends_at=entry[6], panel=entry[4])
    moscow_clock = clockFaceEntries[0][3]
    NY_clock = clockFaceEntries[1][3]
    tokyo_clock = clockFaceEntries[2][3]
    pupil_1_clock = clockFaceEntries[3][3]
    pupil_2_clock = clockFaceEntries[4][3]
    student_1_clock = clockFaceEntries[5][3]
    student_2_clock = clockFaceEntries[6][3]


def startDatabase():
    filename_db = 'clock_panel.db'
    db.init(filename_db)
    db.connect()
    db.create_tables(BaseModel.__subclasses__())
    initDatabase()
