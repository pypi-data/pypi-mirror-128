'''
File: autd.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 24/11/2021
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import ctypes
from ctypes import c_void_p, byref, c_double
import math
import numpy as np
from functools import singledispatch

from .native_methods import Nativemethods, ErrorHandlerFunc, GainMode

NATIVE_METHODDS = Nativemethods()

NUM_TRANS_IN_UNIT = 249
NUM_TRANS_X = 18
NUM_TRANS_Y = 14
TRANS_SPACING_MM = 10.16
DEVICE_WIDTH = 192.0
DEVICE_HEIGHT = 151.4


class Gain:
    def __init__(self):
        self.gain_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteGain(self.gain_ptr)

    @ staticmethod
    def to_duty(amp):
        d = math.asin(amp) / math.pi
        return int(510.0 * d)

    @ staticmethod
    def grouped(gain_pairs):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainGrouped(byref(gain.gain_ptr))
        for (id, gp) in gain_pairs:
            NATIVE_METHODDS.autd3capi.AUTDGainGroupedAdd(gain.gain_ptr, id, gp.gain_ptr)
        return gain

    @ singledispatch
    def focal_point(pos, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainFocalPoint(byref(gain.gain_ptr), pos[0], pos[1], pos[2], duty)
        return gain

    @ focal_point.register
    def _(pos, amp: float = 1.0):
        return Gain.focal_point(pos, Gain.to_duty(amp))

    @ singledispatch
    def bessel_beam(pos, dir, theta_z, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainBesselBeam(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], theta_z, duty)
        return gain

    @ bessel_beam.register
    def _(pos, dir, theta_z, amp: float = 1.0):
        return Gain.bessel_beam(pos, dir, theta_z, Gain.to_duty(amp))

    @ singledispatch
    def plane_wave(pos, dir, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainPlaneWave(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], duty)
        return gain

    @ plane_wave.register
    def _(pos, dir, amp: float = 1.0):
        duty = Gain.to_duty(amp)
        return Gain.plane_wave(pos, dir, duty)

    @ staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint16)
        data = np.ctypeslib.as_ctypes(data)

        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainCustom(byref(gain.gain_ptr), data, size)
        return gain

    @ staticmethod
    def __pack_foci(foci):
        size = len(foci)
        foci_array = np.zeros([size * 3]).astype(np.float64)
        for i, focus in enumerate(foci):
            foci_array[3 * i] = focus[0]
            foci_array[3 * i + 1] = focus[1]
            foci_array[3 * i + 2] = focus[2]
        foci_array = np.ctypeslib.as_ctypes(foci_array)
        return foci_array

    def __pack_amps(amps):
        amps = np.array(amps).astype(np.float64)
        amps = np.ctypeslib.as_ctypes(amps)
        return amps

    @ staticmethod
    def holo_sdp(foci, amps, alpha: float = 1e-3, lambda_: float = 0.9, repeat: int = 100, normalize: bool = False):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloSDP(byref(gain.gain_ptr), backend, foci_array, amps, size, alpha, lambda_, repeat, normalize)
        return gain

    @ staticmethod
    def holo_evd(foci, amps, gamma: float = 1, normalize: bool = False):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloEVD(byref(gain.gain_ptr), backend, foci_array, amps, size, gamma, normalize)
        return gain

    @ staticmethod
    def holo_gs(foci, amps, repeat: int = 100):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloGS(byref(gain.gain_ptr), backend, foci_array, amps, size, repeat)
        return gain

    @ staticmethod
    def holo_gspat(foci, amps, repeat: int = 100):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloGSPAT(byref(gain.gain_ptr), backend, foci_array, amps, size, repeat)
        return gain

    @ staticmethod
    def holo_naive(foci, amps):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloNaive(byref(gain.gain_ptr), backend, foci_array, amps, size)
        return gain

    @ staticmethod
    def holo_lm(foci, amps, eps1: float = 1e-8, eps2: float = 1e-8, tau: float = 1e-3, k_max: int = 5, initial=None):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloLM(
            byref(
                gain.gain_ptr),
            backend,
            foci_array,
            amps,
            size,
            eps1,
            eps2,
            tau,
            k_max,
            initial,
            0 if initial is None else len(initial))
        return gain

    @ staticmethod
    def holo_gauss_newton(foci, amps, eps1: float = 1e-6, eps2: float = 1e-6, k_max: int = 500, initial=None):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloGaussNewton(
            byref(
                gain.gain_ptr),
            backend,
            foci_array,
            amps,
            size,
            eps1,
            eps2,
            k_max,
            initial,
            0 if initial is None else len(initial))
        return gain

    @ staticmethod
    def holo_gradient_descent(foci, amps, eps: float = 1e-6, step: float = 0.5, k_max: int = 2000, initial=None):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloGradientDescent(
            byref(
                gain.gain_ptr),
            backend,
            foci_array,
            amps,
            size,
            eps,
            step,
            k_max,
            initial,
            0 if initial is None else len(initial))
        return gain

    @ staticmethod
    def holo_apo(foci, amps, eps: float = 1e-8, lambda_: float = 1.0, k_max: int = 200):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloAPO(
            byref(
                gain.gain_ptr),
            backend,
            foci_array,
            amps,
            size,
            eps,
            lambda_,
            k_max)
        return gain

    @ staticmethod
    def holo_greedy(foci, amps, phase_div=16):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDGainHoloGreedy(byref(gain.gain_ptr), foci_array, amps, size, phase_div)
        return gain

    @ staticmethod
    def transducer_test(idx: int, duty: int, phase: int):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainTransducerTest(byref(gain.gain_ptr), idx, duty, phase)
        return gain

    @ staticmethod
    def null():
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGainNull(byref(gain.gain_ptr))
        return gain


class Modulation:
    def __init__(self):
        self.modulation_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteModulation(self.modulation_ptr)

    @ property
    def sampling_frequency_div(self):
        return NATIVE_METHODDS.autd3capi.AUTDModulationSamplingFreqDiv(self.modulation_ptr)

    @ sampling_frequency_div.setter
    def sampling_frequency_div(self, value: int):
        return NATIVE_METHODDS.autd3capi.AUTDModulationSetSamplingFreqDiv(self.modulation_ptr, value)

    @ property
    def sampling_freq(self):
        return NATIVE_METHODDS.autd3capi.AUTDModulationSamplingFreq(self.modulation_ptr)

    @ staticmethod
    def static(amp=255):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationStatic(byref(mod.modulation_ptr), amp)
        return mod

    @ staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint8)
        data = np.ctypeslib.as_ctypes(data)

        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationCustom(byref(mod.modulation_ptr), data, size)
        return mod

    @ staticmethod
    def sine(freq: int, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationSine(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    @ staticmethod
    def sine_pressure(freq: int, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationSinePressure(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    @ staticmethod
    def sine_legacy(freq: float, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationSineLegacy(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    @ staticmethod
    def square(freq: int, low: int = 0, high: int = 255, duty: float = 0.5):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDModulationSquare(byref(mod.modulation_ptr), freq, low, high, duty)
        return mod


class Sequence:
    def __init__(self):
        self.seq_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteSequence(self.seq_ptr)

    def set_frequency(self, freq: float):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSetFreq(self.seq_ptr, freq)

    @ property
    def frequency(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceFreq(self.seq_ptr)

    @ property
    def sampling_frequency(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingFreq(self.seq_ptr)

    @ property
    def sampling_frequency_div(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingFreqDiv(self.seq_ptr)

    @ sampling_frequency_div.setter
    def sampling_frequency_div(self, value: int):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSetSamplingFreqDiv(self.seq_ptr, value)

    @ property
    def period(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequencePeriod(self.seq_ptr)

    @ property
    def sampling_period(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingPeriod(self.seq_ptr)


class PointSequence(Sequence):
    def __init__(self):
        super().__init__()
        NATIVE_METHODDS.autd3capi.AUTDSequence(byref(self.seq_ptr))

    def __del__(self):
        super().__del__()

    @ staticmethod
    def circum(center, normal, radius, num_points):
        seq = PointSequence()
        NATIVE_METHODDS.autd3capi.AUTDCircumSequence(
            byref(
                seq.seq_ptr),
            center[0],
            center[1],
            center[2],
            normal[0],
            normal[1],
            normal[2],
            radius,
            num_points)
        return seq

    def add_point(self, point, duty: int = 0xFF):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceAddPoint(self.seq_ptr, point[0], point[1], point[2], duty)

    def add_points(self, points, duties):
        points_size = len(points)
        points_array = np.zeros([points_size * 3]).astype(np.float64)
        for i, p in enumerate(points):
            points_array[3 * i] = p[0]
            points_array[3 * i + 1] = p[1]
            points_array[3 * i + 2] = p[2]
        points_array = np.ctypeslib.as_ctypes(points_array)

        duties_size = len(duties)
        duties_array = np.zeros([duties_size]).astype(np.uint8)
        for i, d in enumerate(duties):
            duties_array[i] = d
        duties_array = np.ctypeslib.as_ctypes(duties_array)

        return NATIVE_METHODDS.autd3capi.AUTDSequenceAddPoints(self.seq_ptr, points_array, points_size, duties_array, duties_size)


class GainSequence(Sequence):
    def __init__(self, gain_mode: GainMode = GainMode.DUTY_PHASE_FULL):
        super().__init__()
        NATIVE_METHODDS.autd3capi.AUTDGainSequence(byref(self.seq_ptr), gain_mode)

    def __del__(self):
        super().__del__()

    def add_gain(self, gain: Gain):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceAddGain(self.seq_ptr, gain.gain_ptr)


class Link:
    def __init__(self):
        self.link_ptr = c_void_p()

    @ staticmethod
    def enumerate_adapters():
        NATIVE_METHODDS.init_autd3capi_soem_link()
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.autd3capi_soem_link.AUTDGetAdapterPointer(byref(handle))

        for i in range(size):
            sb_desc = ctypes.create_string_buffer(128)
            sb_name = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.autd3capi_soem_link.AUTDGetAdapter(handle, i, sb_desc, sb_name)
            res.append([sb_name.value.decode('mbcs'), sb_desc.value.decode('mbcs')])

        NATIVE_METHODDS.autd3capi_soem_link.AUTDFreeAdapterPointer(handle)

        return res

    @ staticmethod
    def soem(ifname, dev_num, cycle_ticks=1, error_handler=None):
        NATIVE_METHODDS.init_autd3capi_soem_link()
        link = Link()
        error_handler = ErrorHandlerFunc(error_handler) if error_handler is not None else None
        NATIVE_METHODDS.autd3capi_soem_link.AUTDLinkSOEM(byref(link.link_ptr), ifname.encode('mbcs'), dev_num, cycle_ticks, error_handler)
        return link

    @ staticmethod
    def twincat():
        link = Link()
        NATIVE_METHODDS.autd3capi_twincat_link.AUTDLinkTwinCAT(byref(link.link_ptr))
        return link

    @ staticmethod
    def remote_twincat(remote_ip_addr, remote_ams_net_id, local_ams_net_id):
        link = Link()
        NATIVE_METHODDS.autd3capi_twincat_link.AUTDLinkRemoteTwinCAT(
            byref(
                link.link_ptr),
            remote_ip_addr.encode('mbcs'),
            remote_ams_net_id.encode('mbcs'),
            local_ams_net_id.encode('mbcs'))
        return link

    @ staticmethod
    def emulator(port, autd):
        link = Link()
        NATIVE_METHODDS.autd3capi_emulator_link.AUTDLinkEmulator(byref(link.link_ptr), port, autd.p_cnt)
        return link


class AUTD:
    def __init__(self):
        self.p_cnt = c_void_p()
        NATIVE_METHODDS.autd3capi.AUTDCreateController(byref(self.p_cnt))
        self.__disposed = False

    def __del__(self):
        self.dispose()

    def last_error():
        size = NATIVE_METHODDS.autd3capi.AUTDGetLastError(None)
        err = ctypes.create_string_buffer(size)
        NATIVE_METHODDS.autd3capi.AUTDGetLastError(err)
        return err.value.decode('mbcs')

    def open(self, link: Link):
        return NATIVE_METHODDS.autd3capi.AUTDOpenController(self.p_cnt, link.link_ptr)

    def firmware_info_list(self):
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.autd3capi.AUTDGetFirmwareInfoListPointer(self.p_cnt, byref(handle))

        for i in range(size):
            sb_cpu = ctypes.create_string_buffer(128)
            sb_fpga = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.autd3capi.AUTDGetFirmwareInfo(handle, i, sb_cpu, sb_fpga)
            res.append([sb_cpu.value.decode('mbcs'), sb_fpga.value.decode('mbcs')])

        NATIVE_METHODDS.autd3capi.AUTDFreeFirmwareInfoListPointer(handle)

        return res

    def dispose(self):
        if not self.__disposed:
            self.close()
            self._free()
            self.__disposed = True

    def add_device(self, pos, rot):
        return NATIVE_METHODDS.autd3capi.AUTDAddDevice(self.p_cnt, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2])

    def add_device_quaternion(self, pos, q):
        return NATIVE_METHODDS.autd3capi.AUTDAddDeviceQuaternion(self.p_cnt, pos[0], pos[1], pos[2], q[0], q[1], q[2], q[3])

    def stop(self):
        return NATIVE_METHODDS.autd3capi.AUTDStop(self.p_cnt)

    def pause(self):
        return NATIVE_METHODDS.autd3capi.AUTDPause(self.p_cnt)

    def resume(self):
        return NATIVE_METHODDS.autd3capi.AUTDResume(self.p_cnt)

    def close(self):
        return NATIVE_METHODDS.autd3capi.AUTDCloseController(self.p_cnt)

    def clear(self):
        return NATIVE_METHODDS.autd3capi.AUTDClear(self.p_cnt)

    def update_ctrl_flags(self):
        return NATIVE_METHODDS.autd3capi.AUTDUpdateCtrlFlags(self.p_cnt)

    def _free(self):
        NATIVE_METHODDS.autd3capi.AUTDFreeController(self.p_cnt)

    @ property
    def is_open(self):
        return NATIVE_METHODDS.autd3capi.AUTDIsOpen(self.p_cnt)

    @ property
    def output_enable(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetOutputEnable(self.p_cnt)

    @ output_enable.setter
    def output_enable(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetOutputEnable(self.p_cnt, value)

    @ property
    def silent_mode(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetSilentMode(self.p_cnt)

    @ silent_mode.setter
    def silent_mode(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetSilentMode(self.p_cnt, value)

    @ property
    def force_fan(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetForceFan(self.p_cnt)

    @ force_fan.setter
    def force_fan(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetForceFan(self.p_cnt, value)

    @ property
    def output_balance(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetOutputBalance(self.p_cnt)

    @ output_balance.setter
    def output_balance(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetOutputBalance(self.p_cnt, value)

    @ property
    def check_ack(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetCheckAck(self.p_cnt)

    @ check_ack.setter
    def check_ack(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetCheckAck(self.p_cnt, value)

    @ property
    def wavelength(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetWavelength(self.p_cnt)

    @ wavelength.setter
    def wavelength(self, wavelength: float):
        NATIVE_METHODDS.autd3capi.AUTDSetWavelength(self.p_cnt, wavelength)

    @ property
    def attenuation(self):
        return NATIVE_METHODDS.autd3capi.AUTDGetAttenuation(self.p_cnt)

    @ attenuation.setter
    def attenuation(self, attenuation: float):
        NATIVE_METHODDS.autd3capi.AUTDSetAttenuation(self.p_cnt, attenuation)

    @ property
    def reads_fpga_info(self):
        NATIVE_METHODDS.autd3capi.AUTDGetReadsFPGAInfo(self.p_cnt)

    @ reads_fpga_info.setter
    def reads_fpga_info(self, value: bool):
        NATIVE_METHODDS.autd3capi.AUTDSetReadsFPGAInfo(self.p_cnt, value)

    @ property
    def fpga_info(self):
        infos = np.zeros([self.num_devices()]).astype(np.ubyte)
        pinfos = np.ctypeslib.as_ctypes(infos)
        NATIVE_METHODDS.autd3capi.AUTDGetFPGAInfo(self.p_cnt, pinfos)
        return infos

    def set_delay_offset(self, delays, offsets):
        size = len(delays)
        if delays is not None:
            delays_ = np.zeros([size]).astype(np.ubyte)
            for i, v in enumerate(delays):
                delays_[i] = v
            delays_ = np.ctypeslib.as_ctypes(delays_)
        else:
            delays_ = None
        if offsets is not None:
            offsets_ = np.zeros([size]).astype(np.ubyte)
            for i, v in enumerate(offsets):
                offsets_[i] = v
            offsets_ = np.ctypeslib.as_ctypes(offsets_)
        else:
            offsets = None
        return NATIVE_METHODDS.autd3capi.AUTDSetDelayOffset(self.p_cnt, delays_, offsets_)

    def num_devices(self):
        return NATIVE_METHODDS.autd3capi.AUTDNumDevices(self.p_cnt)

    def num_transducers(self):
        return self.num_devices() * NUM_TRANS_IN_UNIT

    def send(self, gain: Gain, mod: Modulation):
        return NATIVE_METHODDS.autd3capi.AUTDSendGainModulation(
            self.p_cnt, gain.gain_ptr if gain is not None else None, mod.modulation_ptr if mod is not None else None)

    def send_seq(self, seq: PointSequence, mod: Modulation = None):
        return NATIVE_METHODDS.autd3capi.AUTDSendSequenceModulation(self.p_cnt, seq.seq_ptr, mod.modulation_ptr if mod is not None else None)

    def send_gain_seq(self, seq: GainSequence, mod: Modulation = None):
        return NATIVE_METHODDS.autd3capi.AUTDSendGainSequenceModulation(self.p_cnt, seq.seq_ptr, mod.modulation_ptr if mod is not None else None)

    def stm(self):
        handle = c_void_p()
        NATIVE_METHODDS.autd3capi.AUTDSTMController(byref(handle), self.p_cnt)
        return STMController(handle)

    def trans_pos(self, dev_idx: int, trans_idx_local):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDTransPosition(self.p_cnt, dev_idx, trans_idx_local, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_x(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceXDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_y(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceYDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_z(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceZDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])


class STMController:
    def __init__(self, handle):
        self.handle = handle

    def add(self, gain: Gain):
        NATIVE_METHODDS.autd3capi.AUTDAddSTMGain(self.handle, gain.gain_ptr)

    def start(self, freq: float):
        return NATIVE_METHODDS.autd3capi.AUTDStartSTM(self.handle, freq)

    def stop(self):
        return NATIVE_METHODDS.autd3capi.AUTDStopSTM(self.handle)

    def finish(self):
        return NATIVE_METHODDS.autd3capi.AUTDFinishSTM(self.handle)
