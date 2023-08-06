import commpy as comm
import numpy as np
import soundfile as sf
import bitstring as bs
import requests #
import os.path #
from scipy.signal import max_len_seq
from scipy.signal import resample
from scipy.signal import filtfilt
from scipy.signal import butter
from scipy.signal import freqz
from scipy.fft import rfft, rfftfreq
from matplotlib import pyplot as plt
import warnings

class model:
    
    """Данный класс позволяет провести моделирование системы передачи данных с расширением спектра методом DSSS.
    
        data_path               - Путь к информационному аудифайлу.\n
        mod_type                - Тип модуляции. Может принимать значения: 'PSK', 'QAM'.\n 
        mod_order               - Порядок модуляции.\n 
        polinom                 - Полином генератора расширяющей последовательности. Указываются только степени с ненулевым коэффициентом.\n 
                                  Пример: x^8+x^7+x^2+x+1 записывается как [8, 7, 2, 1, 0].\n 
        noise_type              - Тип сигнала шума. Может принимать значения: 'white', 'gray', 'pink'.\n  
        max_attenuation         - Затухание амплитуды информационного сигнала в дБ относительно максимальной амплитуды,     
                                  после которого сигнал считается затухшим. Используется для вычисления максимальной частоты информационного сигнала.\n 
        SNRdB                   - Желаемое соотношение сигнал/шум в дБ после наложения шума.\n    
        sine_freq_multiplier    - Множитель частоты синусоиды (целое положительное число, не более 4). Показывает, во сколько раз 
                                частота синусоиды больше максимальной частоты сигнала.\n
        nbits = 9               - Количество бит в генераторе м-последовательности.\n 
        log = True              - Вывод информации и графиков в ходе вычислений.\n    

    Для получения доступа к промежуточным значениям сигнала их частот дискретизации можно использовать следующие переменные:\n

        data                data_samplerate                 - Исходный аудиосигнал\n
        dsss_data           dsss_data_samplerate            - Сигнал после DSSS\n
        modulated_data      modulated_data_samplerate       - Модулированный сигнал\n
        channel_signal      channel_signal_sample_rate      - Сигнал после добавления синусоиды и шума\n
        filtered_signal     channel_signal_sample_rate      - Сигнал после фильтрации\n
        demodulated_data    dsss_data_samplerate            - Демудулированный сигнал\n
        recivied_data       data_samplerate                 - Конечный принятый сигнал\n

    Для визуализации информации о сигналах можно использовать следующие методы:\n

        plot_spectrum(signal, fs, dB = True)    - Построение спектра сигнала\n
            signal                              - Сигнал\n
            fs                                  - Часота дискретизации\n
            dB = True                           - Отображать ось y в дБ\n

        plot_psd(self, signal, fs, name = "Спектральная плотность мощности")    - Построение спектральной плотности мощности сигнала\n
            signal                                                              - Сигнал\n
            fs                                                                  - Часота дискретизации\n
            name = "Спектральная плотность мощности"                            - Имя графика\n
    
    Пример использвоания:\n
    ```
    m = model(
    data_path = 'original_music.wav', 
    mod_type = 'QAM', 
    mod_order = 64,  
    polinom = [8, 7, 2, 1, 0], 
    noise_type =  'gray', 
    max_attenuation = 6, 
    SNRdB =  0, 
    sine_freq_multiplier = 2, 
    )

    m.read_data()
    m.data_to_binary()
    m.add_msequence()
    m.modulate_signal()
    m.add_noise_and_sine()
    m.filter_signal()
    m.demodulate_signal()
    m.export_recivied_audio('output')
    ```
    """
    mod_types                   = ['QAM', 'PSK']
    noise_to_id                 = {'white' : '192v3dbPctSFiKM-QqzYAgd6FvZ4iffNL', 'gray' : '1LbFgpAtSFkTTx1pslI6ZbkAswLa0k5rv', 'pink': '1LDOjzZAJVEcD7UCPWohjk_QLYIX_dIiS'}
    data_samplerate             = 48000
    dsss_data_samplerate        = 96000
    modulated_data_samplerate   = 96000
    channel_signal_sample_rate  = None
    chipping_rate               = 2
    data                        = None
    m_seq                       = None
    bin_data                    = None
    dsss_data                   = None
    modulated_data              = None
    channel_signal              = None
    filtered_signal             = None
    modem                       = None
    demodulated_data            = None
    recivied_data_bin           = None
    recivied_data               = None
    workspace_path              = None
    data_fragment               = None
    recivied_data_fragment      = None

    def __init__(self, data_path, mod_type, mod_order, polinom, noise_type, max_attenuation, SNRdB, sine_freq_multiplier,  nbits = 9, log = True, low_ram_usage =  True, print_logo = False, transmit_fragment_size = 1, disable_lim = False):
        if(mod_type not in self.mod_types): raise ValueError("Поддерживаемые типы модуляции: 'PSK', 'QAM'")
        if(noise_type not in self.noise_to_id): raise ValueError("Поддерживаемые типы шума: 'white', 'pink', 'gray'")
        if(int(sine_freq_multiplier) > 4): raise ValueError("Частота синусоиды может быть больше максимальной частоты информационного сигнала не более, чем в 4 раза")
        if(int(sine_freq_multiplier) < 0): raise ValueError("Частота синусоиды должна быть больше максимальной частоты информационного сигнала")
        self.channel_signal_sample_rate = self.modulated_data_samplerate*sine_freq_multiplier

        self.data_path                  = data_path
        self.log                        = log
        self.nbits                      = nbits
        self.poli                       = polinom
        self.mod_type                   = mod_type
        self.mod_order                  = mod_order
        self.noise_type                 = noise_type
        self.max_attenuation            = max_attenuation
        self.SNRdB                      = SNRdB
        self.sine_freq_multiplier       = int(sine_freq_multiplier)
        self.print_logo                 = print_logo
        self.low_ram_usage              = low_ram_usage
        self.transmit_fragment_size     = transmit_fragment_size
        self.disable_lim                = disable_lim



        if os.path.isdir('workspace') == False:
            os.mkdir('workspace')
            self.workspace_path = os.path.abspath('workspace')
            if self.log: print("Создана рабочая директория workspace: ", self.workspace_path)
        else:
            self.workspace_path = os.path.abspath('workspace') 
            if self.log: print("Рабочая директория workspace уже существует: ", self.workspace_path)
        
    def transmit_fragment(self):
        self.data_to_binary()
        self.add_msequence()
        self.modulate_signal()
        self.add_noise_and_sine()
        self.filter_signal()
        self.demodulate_signal()

    def transmit_data(self):
        if self.log: print('Разделение данных на фрагменты:')
        step = self.transmit_fragment_size*self.data_samplerate
        if self.log: print('Шаг в секундах:', self.transmit_fragment_size)
        if self.log: print('Шаг в семплах:', step)

        self.recivied_data = np.empty(0)
        fragments_count = int(np.ceil(self.data.shape[0]/self.data_samplerate))
        if self.log: print('Количество фрагментов:', fragments_count)
        log_back = self.log
        for fragment_indx in range(fragments_count):
            self.data_fragment = self.data[fragment_indx*step:(fragment_indx+1)*step]
            self.transmit_fragment()
            self.recivied_data = np.hstack((self.recivied_data, self.recivied_data_fragment))
            self.log = False
            if log_back: print('Передано фрагментов:', fragment_indx+1, '/', fragments_count)
        self.log  = log_back 

    def plot_logo(self):
        print("    __  __   U _____ u    _  __        _        _____     _____      U  ___ u\n U\|\' \/ '|u \| ___\"|/   |\"|/ /    U  /\"\  u   |_ \" _|   |_ \" _|      \/\"_ \/\n  \| |\/| |/  |  _|\"     | ' /      \/ _ \/      | |       | |        | | | |\n  \| |  | |   | |___   U/| . \\u     / ___ \     /| |\     /| |\   .-,_| |_| |\n  \|_|  |_|   |_____|    |_|\_\    /_/   \_\   u |_|U    u |_|U    \_)-\___/\n  <<,-,,-.    <<   >>  ,-,>> \ \.  \ \    >>  _/ / \ \_ _/ / \ \_       \ \ \n   (./  \.)  (__) (__)  \..) (__/ (___) (___)(___) (___)(___) (___)     (__)  ")

    def plot_spectrum(self, signal, fs, dB = True):       
        # N = signal.shape[0]
        N = 1000
        yf = rfft(signal,norm='ortho' )
        if dB: yf = 10*np.log10(abs(yf))
        else: yf = abs(yf)
        xf = rfftfreq(N, 1 / fs)
        plt.plot(xf, yf)
        plt.show()

    def plot_psd(self, signal, fs, name = "Спектральная плотность мощности"):
        fig, ax = plt.subplots(1,figsize=(15,5))
        fig.suptitle(name, fontsize=16)
        ax.psd(signal, len(signal), fs)
        plt.show()
        
    def resample(self, signal, new_rate, old_rate ):
        number_of_samples = round(len(signal) * float(new_rate) / old_rate)
        return resample(signal, number_of_samples)

    def export_recivied_audio(self, fname = 'recivied_audio' ):
        fname = fname + '.wav'
        sf.write(os.path.join(self.workspace_path, fname), self.recivied_data, self.data_samplerate)
        if self.log: print("Экспорт аудиофайла:\n -Аудиофайл успешно экспортирован как", fname)

    def read_data(self):
        data, data_samplerate = sf.read(self.data_path)
        if(self.print_logo): self.plot_logo()
        if self.log: print('Загрузка аудиофайла:\n-Частота дискретизации:', data_samplerate)
        if  (len(data.shape) > 1):
            warnings.warn(message =  'Аудиофайл содержит два канала. Для повышения производительности будет импортирован только один из них', stacklevel=2)
            data = data[:, 0]
        if (data_samplerate != self.data_samplerate):
            warnings.warn(message =  'Частота дискретизации файла не поддерживается, она будет изменена на 48000', stacklevel=2)
            data = self.resample(data, self.data_samplerate, data_samplerate) 
        if  (data.shape[0]/data_samplerate > 15 and not self.disable_lim ):
            warnings.warn("Длительность аудиофайла превышает 15 секунд. Для повышения производительности он будет обрезан.", stacklevel=2)
            data = data[0:data_samplerate*15]
        self.data = data
        if self.log: print('- Аудиофайл успешно импортирован, частота дискретизации: ', self.data_samplerate)
        if self.log: self.plot_psd(self.data, self.data_samplerate, name= "Спектральная плотность мощности исходного аудиофайла")
         

    def generate_mseq(self):
         if self.log: print('Генерация м-последовательности')
         self.m_seq, _ = max_len_seq(self.nbits, length = self.bin_data.shape[0]*self.chipping_rate, taps = self.poli )
         self.m_seq = [bool(x) for x in self.m_seq]
          

    def float_to_binary(self, num):
        bitstring = bs.BitArray(float=num, length=32)
        bit_arr = [x for x in bitstring]
        return bit_arr

    def data_to_binary(self):
        if self.log: print('Конвертация аудиофайла в биты:')
        bin_data = [self.float_to_binary(x) for x in self.data_fragment]
        bin_data = np.asanyarray(bin_data)
        if self.log: print(" - Размерность массива данных: ", bin_data.shape)
        bin_data = np.reshape(bin_data,(-1))
        if self.log: print(" - Размерность массива данных после развертки: ", bin_data.shape)
        self.bin_data = bin_data
        if self.low_ram_usage: self.data_fragment = None
         

    def add_msequence(self):
        self.generate_mseq()
        if self.log: print('Расширение спектра методом DSSS:')
        self.dsss_data = self.bin_data
        if self.low_ram_usage: self.bin_data = None 
        self.dsss_data = self.dsss_data.repeat(self.chipping_rate, axis=0) # upsample
        self.dsss_data = np.logical_xor(self.dsss_data, self.m_seq)
        self.dsss_data = [int(x) for x in self.dsss_data]
        self.msg_len = len(self.dsss_data)
        if self.log: print(' - Размерность данных после расширения спектра:', len(self.dsss_data) )
        if (self.log and (not self.low_ram_usage)) : print(" - Приемер данных до и после расширения пректра:", "\n -", self.data[0:10], "\n -" , self.dsss_data[0:20], "\n -" , 'chipping_rate = ', self.chipping_rate  )
        if self.log: print(" - Частота дискретизации после расширения спектра:", self.dsss_data_samplerate  )
        if self.log: self.plot_psd(self.dsss_data, self.dsss_data_samplerate, name= "Спектральная плотность мощности сигнала после сложения с м-последовательностью")
         

    def modulate_signal(self):
        if self.log: print('Модуляция сигнала:')
        if (self.mod_type == 'QAM'): self.modem = comm.QAMModem(self.mod_order)
        elif (self.mod_type == 'PSK'): self.modem = comm.PSKModem(self.mod_order)
        if self.log: print(' - Создан модем', self.mod_type, self.mod_order)
        self.modulated_data = self.modem.modulate(self.dsss_data)
        if self.low_ram_usage: self.dsss_data = None 
        if self.log: print(' - Сигнал модулирован', self.mod_type, self.mod_order)
        if self.log: print(' - Размерность сигнала:', self.modulated_data.shape)
        if self.log: self.plot_psd(self.modulated_data, self.modulated_data_samplerate, name= "Спектральная плотность мощности модулированного сигнала")
         

    def download_file_from_google_drive(self, id, destination):
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = self.get_confirm_token(response)
        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)
        self.save_response_content(response, destination)    

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                
    def prepare_noise(self):
        noise_path = os.path.join(self.workspace_path, self.noise_type + '.wav')
        if (not os.path.isfile(noise_path)):
            if self.log: print('Загрузка файла с шумом. Это может занять некоторое время...')
            file_id = self.noise_to_id[self.noise_type]
            self.download_file_from_google_drive(file_id, noise_path)


    def add_noise(self):
        if self.log: print('Добавление шума:')
        self.prepare_noise()
        filename = os.path.join(self.workspace_path, self.noise_type + '.wav')
        self.noise, self.noise_samplerate = sf.read(filename)
        if self.log: print(' - Размерность шума:', self.noise.shape)
        self.noise = self.noise[0:self.channel_signal.shape[0]]
        if self.log: print(' - Размерность шума после обрезания(кек):', self.noise.shape)
        P_sig = (np.mean(self.channel_signal.real**2)+np.mean(self.channel_signal.imag**2))/2
        if self.log: print(' - Мощность сигнала (в среднем на один канал) равна: ', P_sig)
        P_noise = np.mean(self.noise**2)
        if self.log: print(' - Мощность шума (один канал) равна: ', P_noise)
        gamma = 10**(self.SNRdB/10) #SNR to linear scale
        if self.log: print(' - SNR в разах: ', gamma)
        target_noise_amp = np.sqrt(P_sig/gamma)
        noise_scale_coeff = target_noise_amp/np.sqrt(P_noise)
        if self.log: print(' - Скалирование мощности шума')
        self.noise *= noise_scale_coeff
        self.noise = self.noise + self.noise*1j
        P_noise2 = np.mean(self.noise**2)
        if self.log: print(' - Мощность шума (в среднем на один канал) после скалирования: ', P_noise2)
        if self.log: self.plot_psd(self.noise, self.noise_samplerate, name = "Спектральная плотность мощности шумового сигнала")
        if self.log: print(' - Сложение сигнала с шумом')
        self.channel_signal = self.channel_signal + self.noise
        if self.low_ram_usage: self.noise = None
        if self.log: self.plot_psd(self.channel_signal, self.channel_signal_sample_rate, name= "Спектральная плотность мощности сигнала с наложенным шумом")
         

    def add_sine(self):
        if self.log: print('Добавление синусоидальной помехи:')
        (mag,freq, _) = plt.magnitude_spectrum(self.channel_signal, Fs=self.channel_signal_sample_rate)
        plt.close()
        mag_log     = 20*np.log10(mag)
        max_mag     = max(mag_log)
        th_value    = max_mag - self.max_attenuation 
        th_index    = np.max(np.argwhere(mag_log > th_value))
        self.treshold_freq     = freq[th_index]
        if self.log: print(' - Максимальная частота информационного сигнала: ', self.treshold_freq)
        if self.log: print(' - Генерация синусоиды с частотой: ', self.sine_freq_multiplier*self.treshold_freq)
        x = np.arange(0,self.channel_signal.shape[0], 1)
        self.sine = np.sin(2*np.pi*self.treshold_freq*self.sine_freq_multiplier*x/self.channel_signal_sample_rate)
        if self.log: self.plot_psd(self.sine, self.channel_signal_sample_rate, name= "Спектральная плотность мощности синусоидального сигнала")
        if self.log: print(' - Сложение сигнала с синусоидой ')
        self.channel_signal = self.channel_signal + self.sine
        if self.low_ram_usage: self.sine = None
        if self.log: self.plot_psd(self.channel_signal, self.channel_signal_sample_rate, name= "Спектральная плотность мощности сигнала с наложенным шумом и синусоидой")
         

    def add_noise_and_sine(self):
        if(self.modulated_data_samplerate != self.channel_signal_sample_rate):
            if self.log: print(' - Увеличение частоты семплирования сигнала до ', self.channel_signal_sample_rate)
            self.channel_signal = self.resample(self.modulated_data, self.channel_signal_sample_rate, self.modulated_data_samplerate)
            if self.low_ram_usage: self.modulated_data = None
        else:
            self.channel_signal = self.modulated_data
            if self.low_ram_usage: self.modulated_data = None
        self.add_noise()
        if (self.channel_signal_sample_rate > self.noise_samplerate):
            if self.log: print('Частота дискретизации сигнала превышает частоту дискретизации шума. Тем не менее, полоса шума совпадает или превышает полосу полезного сигнала.')
        self.add_sine()
         

    def filter_signal(self):
        cutoff = self.treshold_freq*1.1
        if self.log: print(' - Создание LPF с частотой среза',cutoff )
        nyq = 0.5 * self.channel_signal_sample_rate
        normal_cutoff = cutoff / nyq
        b, a = butter(10, normal_cutoff, btype='low', analog=False)
        ### ачх фильтра
        if self.log:
            fig, ax = plt.subplots(1,figsize=(10,5))
            w, h = freqz(b, a, worN=80000)
            ax.plot(0.5*self.channel_signal_sample_rate*w/np.pi, 20 * np.log10(abs(h)), 'b')
            ax.plot(cutoff, 0.5*np.sqrt(2), 'ko')
            ax.axvline(self.treshold_freq, color='k')
            ax.set_xlim(0, 0.5*self.channel_signal_sample_rate)
            ax.set_title("АЧХ фильтра")
            ax.set_ylabel('Амплитуда [дБ]', color='b')
            ax.set_xlabel('Частота [Гц]')
            ax.grid()
            plt.show()
        self.filtered_signal = filtfilt(b, a, self.channel_signal)
        if self.low_ram_usage: self.channel_signal = None
        if self.log: self.plot_psd(self.filtered_signal, self.channel_signal_sample_rate, name = "Спектральная плотность мощности отфильтрованного сигнала")
         

    def demodulate_signal(self):
        if self.log: print(' - Уменьшение частоты семплирования сигнала до 96000')
        received_signal = self.resample(self.filtered_signal, self.dsss_data_samplerate, self.channel_signal_sample_rate)
        if self.low_ram_usage: self.filtered_signal = None
        if self.log: self.plot_psd(received_signal, self.dsss_data_samplerate, name = "Спектральная плотность мощности принятого сигнала с пониженной частотой дискретизации")
        if self.log: print(' - Демодуляция сигнала')
        self.demodulated_data = self.modem.demodulate(received_signal, 'hard' )
        del received_signal
        self.demodulated_data = self.demodulated_data[0:self.msg_len]
        if self.log: self.plot_psd(self.demodulated_data, self.dsss_data_samplerate, name = "Спектральная плотность мощности демодулированного сигнала")
        if self.log: print(' - Формирование массива бит')
        self.demodulated_data = np.asanyarray([bool(x) for x in self.demodulated_data])
        if self.log: print(' - Сложение сигнала с м-последовательностью')
        self.recivied_bin_data = np.logical_xor(self.demodulated_data, self.m_seq)
        if self.low_ram_usage: self.demodulated_data = None
        if self.log: print(' - Определение значения бит')
        self.recivied_bin_data = self.recivied_bin_data[::2]
        if self.log: print(' - Частота дискретизации перед конвертацией в float ',self.data_samplerate ) 
        self.recivied_data_fragment = np.reshape(self.recivied_bin_data, ((-1, 32)))
        self.recivied_data_fragment = [bs.BitArray(x) for x in self.recivied_data_fragment]
        if self.log: print(' - Конвертация бит в float')
        self.recivied_data_fragment = (np.asanyarray([x.float for x in self.recivied_data_fragment]))
         
        


