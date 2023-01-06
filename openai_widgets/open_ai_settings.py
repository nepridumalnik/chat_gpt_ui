import openai
import atexit
import json
import os

MIN_RESOLUTION: int = 100
MAX_RESOLUTION: int = 4096


class OpenAISettings:
    API_KEY: str = os.environ['OPENAI_API_KEY']
    openai.api_key = API_KEY

    engineList = openai.Engine.list()

    __settings: dict = dict()

    __settings['currentEngine'] = 'text-davinci-003'
    __settings['maxTokens'] = 3000
    __settings['imageResolution'] = '1024x1024'

    __saveFile: str = 'settings.txt'

    def __init__(self) -> None:
        self.__load()

        engines = self.getEngines()

        if self.__settings['currentEngine'] not in engines:
            self.__settings['currentEngine'] = engines[0]

        atexit.register(self.__cleanup)

    def __save(self) -> None:
        dump: str = json.dumps(self.__settings)

        with open(self.__saveFile, 'w') as f:
            f.write(dump)

    def __load(self) -> None:
        data: str = ''
        with open(self.__saveFile, 'r') as f:
            data = f.read()

        deserializedSettings = json.loads(data)

        for key, val in deserializedSettings.items():
            self.__settings[key] = val

    def __cleanup(self) -> None:
        self.__save()

    def makeCompletion(self, prompt: str) -> str:
        completion = openai.Completion.create(
            engine=self.__settings['currentEngine'],
            prompt=prompt,
            max_tokens=self.__settings['maxTokens'],
        )

        respond: str = ''

        for c in completion.choices:
            respond += c.text

        return respond

    def makeImage(self, prompt: str):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=self.__settings['imageResolution'],
        )

        return response

    def setImageResolution(self, w: int = 1024, h: int = 1024) -> None:
        if w < MAX_RESOLUTION:
            w = MAX_RESOLUTION
        elif w > MAX_RESOLUTION:
            w = MAX_RESOLUTION

        if h < MAX_RESOLUTION:
            h = MAX_RESOLUTION
        elif h > MAX_RESOLUTION:
            h = MAX_RESOLUTION

        self.__settings['imageResolution'] = f'{w}x{h}'

    def getEngines(self):
        engines = []

        for engine in self.engineList.data:
            engines.append(engine.id)

        return engines


oaiSettings: OpenAISettings = OpenAISettings()
