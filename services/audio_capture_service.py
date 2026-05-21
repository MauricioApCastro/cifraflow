from PyQt6.QtCore import QObject, pyqtSignal


class AudioCaptureService(QObject):
    volume_changed = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.stream = None
        self.numpy = None
        self.sounddevice = None

    def start(self):
        if self.is_active():
            return

        try:
            import numpy
            import sounddevice
        except Exception as error:
            self.error_occurred.emit(f"Erro ao carregar áudio: {error}")
            return

        self.numpy = numpy
        self.sounddevice = sounddevice

        try:
            device_index = self.find_default_input_device()
            if device_index is None:
                self.error_occurred.emit("Microfone não encontrado")
                return

            self.stream = self.sounddevice.InputStream(
                device=device_index,
                channels=1,
                samplerate=44100,
                blocksize=1024,
                callback=self.process_audio,
            )
            self.stream.start()
        except self.sounddevice.PortAudioError as error:
            self.close_stream()
            self.error_occurred.emit(f"Erro de áudio: {error}")
        except PermissionError:
            self.close_stream()
            self.error_occurred.emit("Permissão negada para acessar o microfone")
        except Exception as error:
            self.close_stream()
            self.error_occurred.emit(str(error))

    def stop(self):
        if not self.stream:
            return

        self.close_stream()
        self.volume_changed.emit(0)

    def is_active(self) -> bool:
        return self.stream is not None and self.stream.active

    def process_audio(self, indata, frames, time, status):
        if status:
            print(f"Aviso do microfone: {status}")

        rms = self.numpy.sqrt(self.numpy.mean(self.numpy.square(indata)))
        volume = min(100, int(rms * 500))
        self.volume_changed.emit(volume)

    def find_default_input_device(self) -> int | None:
        input_devices = self.list_input_devices()
        if not input_devices:
            return None

        default_device = self.sounddevice.default.device
        default_input_index = default_device[0] if isinstance(default_device, (list, tuple)) else default_device

        for index, device in input_devices:
            if index == default_input_index:
                print(f"Microfone padrão selecionado: [{index}] {device.get('name')}")
                return index

        try:
            default_input = self.sounddevice.query_devices(kind="input")
            default_input_name = default_input.get("name")
            for index, device in input_devices:
                if device.get("name") == default_input_name:
                    print(f"Microfone padrão selecionado: [{index}] {device.get('name')}")
                    return index
        except self.sounddevice.PortAudioError as error:
            print(f"Não foi possível consultar o microfone padrão: {error}")

        print(f"Microfone selecionado: [{input_devices[0][0]}] {input_devices[0][1].get('name')}")
        return input_devices[0][0]

    def list_input_devices(self) -> list[tuple[int, dict]]:
        devices = self.sounddevice.query_devices()
        input_devices = []

        print("Dispositivos de entrada disponíveis:")
        for index, device in enumerate(devices):
            if device.get("max_input_channels", 0) <= 0:
                continue

            input_devices.append((index, device))
            print(f"- [{index}] {device.get('name')} ({device.get('max_input_channels')} canais)")

        if not input_devices:
            print("- Nenhum microfone encontrado")

        return input_devices

    def close_stream(self):
        if not self.stream:
            return

        try:
            self.stream.stop()
            self.stream.close()
        finally:
            self.stream = None
