# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 10:26:19 2017

A record of the .PPR parameters and a function to parse the parameter footer
in a .mrd file

@author: William Scott-Jackson
"""
# We want to use regular expressions to parse the footer
# import re

# TODO: Find out if there are any keywords that need including from other types
# of files, e.g. .SUR
# For now, add the keywords that will be helpful in improving the GE shimming
PPR_keywords = ['BUFFER_SIZE',
                'DATA_TYPE',
                'DECOUPLE_FREQUENCY',
                'DISCARD no_discard,',
                'DSP_ROUTINE',
                'EDITTEXT',
                'FOV',
                'EXPERIMENT_ARRAY',
                'rec_freq,',
                'VAR oversample',
                'VAR oversample2',
                'VAR oversample3',
                'FOV_READ_OFF',
                'FOV_PHASE_OFF',
                'FOV_SLICE_OFF',
                'GRADIENT_STRENGTH',
                'NO_ECHOES',
                'MULTI_ORIENTATION',
                'Multiple Receivers',
                'NO_AVERAGES',
                'NO_RECEIVERS',
                'NO_SAMPLES',
                'NO_SLICES',
                'NO_VIEWS',
                'NO_VIEWS_2',
                'OBLIQUE_ORIENTATION',
                'OBSERVE_FREQUENCY',
                'PHASE_CYCLE',
                'RECEIVER_FILTER',
                'READ/PHASE/SLICE_SELECTION',
                'SAMPLE_PERIOD sample_period,',
                'SAMPLE_PERIOD_2',
                'SCROLLBAR',
                'SLICE_BLOCK',
                'SLICE_FOV',
                'SLICE_INTERLEAVE',
                'SLICE_THICKNESS',
                'SLICE_SEPARATION',
                'SPECTRAL_WIDTH',
                'SWEEP_WIDTH',
                'SWEEP_WIDTH_2',
                'VAR_ARRAY',
                'VIEW_BLOCK',
                'SMX',
                'VIEWS_PER_SEGMENT',
                'SMY',
                'SWX',
                'SWY',
                'SMZ',
                'SWZ',
                'VAR ',
                'PHASE_ORIENTATION',
                'X_ANGLE',
                'Y_ANGLE',
                'Z_ANGLE',
                'PPL C',
                'no_b_steps',
                'b_steps_array',
                'b_grads_array',
                'no_diff_dir',
                'diff_grad_dir',
                'te,',
                'te_us,',
                'VAR FOVf',
                'VAR pe1_order',
                'VAR centric_on',
                'pe2_centric_on,',
                'te2_delay_us,',
                'tr,',
                'VAR tref',
                'tramp,',
                'ti,',
                'VAR_ARRAY venc_amp',
                'tdp,',
                'rfnum,',
                'nav_on']


def ParseKeywords(fileID):
    ppr_text = fileID.read()
    ppr_text = ppr_text.decode('ascii', errors='ignore').replace('\r\n', '')

    par = {}
    if len(ppr_text) > 0:

        for i in PPR_keywords:
            exp = ''.join(["(", i, ")[^_](.*?)(:)"])
            match = re.findall(exp, ppr_text, flags=re.S)
            if match:
                matches = re.findall(exp, ppr_text, flags=re.S)[0]
                tmp = dict(zip(matches[::2], matches[1::2]))
                par.update(tmp)
    else:
        par = {}

    return par
