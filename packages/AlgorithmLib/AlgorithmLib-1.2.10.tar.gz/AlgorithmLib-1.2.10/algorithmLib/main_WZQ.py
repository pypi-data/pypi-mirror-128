from operator import methodcaller
from computeAudioQuality.mainProcess import computeAudioQuality
from ctypes import  *


def compute_audio_quality(metrics, testFile=None, refFile=None, cleFile=None, outFile=None, noiseFile=None,
                              samplerate=16000, bitwidth=2, channel=1, refOffset=0, testOffset=0, maxComNLevel=-48.0,
                              speechPauseLevel=-35.0,audioType=0):
    """
    :param metrics: G160/P563/POLQA/PESQ/STOI/STI/PEAQ/SDR/SII/LOUDNESS/MUSIC/MATCH/TRANSIENT/GAINTABLE/ATTACKRELEASE/MUSICSTA/AGCDELAY，必选项
    # G160 无采样率限制；  WAV/PCM输入 ；三端输入: clean、ref、test；无时间长度要求；
    # 计算 信噪比提升、短时降噪、长时降噪、语音损伤等指标
    # P563 8000hz(其他采样率会强制转换到8khz)；  WAV/PCM输入 ；单端输入: test；时长 < 20s；
    # 计算 无参考的mos分
    # POLQA 窄带模式  8k  超宽带模式 48k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # 计算 有参考的客观语音质量评分
    # PESQ 窄带模式  8k   宽带模式 16k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # 计算 有参考的客观语音质量评分
    # STOI 无采样率限制; 双端输入：ref、test；无时间长度要求；
    # 计算 可懂度
    # STI >8k(实际会计算8khz的频谱)； WAV/PCM输入 ；双端输入：ref、test；时长 > 20s
    # 计算 可懂度
    # PEAQ 无采样率限制；WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # 计算 音乐和音乐编解码的质量
    # SDR 无采样率限制; WAV/PCM输入 ; 双端输入：ref、test；无时间长度要求；
    # MATCH 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    # 信号对齐
    # MUSIC 无采样率限制;WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # 计算音乐下的信噪比
    # TRANSIENT 无采样率限制,WAV/PCM输入;三端输入：cle、noise、test； 无时间长度要求；
    # 计算突发噪声的信噪比
    # GAINTABLE 无采样率限制,WAV/PCM输入;双端输入：ref、test；固定信号输入；
    #计算 gain table
    # ATTACKRELEASE 无采样率限制,WAV/PCM输入;双端输入：ref、test；固定信号输入；
    # 计算AGC attack 和release 的时间
    # MUSICSTA 无采样率限制,WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # 音乐信号的稳定性
    # AGCDELAY 无采样率限制,WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # 用于测试AGC文件的对齐
    不同指标输入有不同的采样率要求，如果传入的文件不符合该指标的要求，会自动变采样到合法的区间
    :param testFile: 被测文件，必选项
    :param refFile:  参考文件，可选项，全参考指标必选，比如POLQA/PESQ/PEAQ
    :param cleFile:  干净语音文件，可选项，G160,TRANSIENT需要
    :param noiseFile 噪声文件，可选项，突发噪声信噪比计算需要
    :param outFile 输出文件，可选项，对其文件可选
    :param samplerate: 采样率，可选项，pcm文件需要 default = 16000
    :param bitwidth: 比特位宽度，可选项，pcm文件需要 default = 2
    :param channel: 通道数，可选项，pcm文件需要 default = 1
    :param refOffset: ref文件的样点偏移，可选项，指标G160需要
    :param testOffset: test文件的样点偏移，可选项，指标G160需要
    :param maxComNLevel: 测试G160文件的最大舒适噪声
    :param speechPauseLevel 测试G160文件的语音间歇段的噪声
    :param gaintableType 测试gaintable的模式 0：语音 1：音乐
    :return:
    """
    paraDicts = {
        'metrics':metrics,
        'testFile':testFile,
        'refFile':refFile,
        'cleFile':cleFile,
        'noiseFile':noiseFile,
        'outFile':outFile,
        'samplerate':samplerate,
        'bitwidth':bitwidth,
        'channel':channel,
        'refOffset':refOffset,
        'testOffset':testOffset,
        'maxComNLevel':maxComNLevel,
        "speechPauseLevel":speechPauseLevel,
        'audioType':audioType
    }
    comAuQUA = computeAudioQuality(**paraDicts)
    return methodcaller(metrics)(comAuQUA)

if __name__ == '__main__':

    # speech = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\speech.wav'
    # music = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\music_rap.wav'
    # transi = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\transientNoise.wav'
    # test = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\test.wav'
    # res = compute_audio_quality('MUSIC',refFile=speech,testFile=music)
    #
    # print(res)
    #
    # res = compute_audio_quality('TRANSIENT',cleFile=speech,noiseFile=transi,testFile=test)
    # print(res)
    #
    # res = compute_audio_quality('MATCH',refFile=speech,testFile=test,outFile='123.wav')
    # print(res)
    #print(compute_audio_quality('G160', testFile=src,refFile=src,samplerate=16000))

    #print(match_sig(refFile='speech.wav', targetFile='test.wav', outFile='outfile.wav'))
    import os
    import xlwt
    path = r'E:\3a_auto_test_porject\WZQ\module_out_no_initialaec'
    path_list = os.listdir(path)
    wk1 = xlwt.Workbook(encoding='utf-8')
    sheet1 = wk1.add_sheet("sheet1")

    for i in range(len(path_list)):
        index = path_list[i]
        cur_path = path + '\\' + index

        file = cur_path + '\\' + r'input_' + index + '.wav'
        test_lowcut = cur_path + '\\' + r'1_lowcut_' + index + '.wav'
        test_aec = cur_path + '\\' + r'2_aec_' + index + '.wav'
        test_ns = cur_path + '\\' + r'3_noise_suppression_' + index + '.wav'
        test_aecm = cur_path + '\\' + r'4_aecm_' + index + '.wav'
        test_agc = cur_path + '\\' + r'5_agc_' + index + '.wav'
        test_agc2 = cur_path + '\\' + r'6_agc2_' + index + '.wav'
        test_post = cur_path + '\\' + r'7_post_processor_' + index + '.wav'

        lowcut_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_lowcut)
        aec_mos = compute_audio_quality('POLQA',refFile=test_lowcut,testFile=test_aec)
        ns_mos = compute_audio_quality('POLQA',refFile=test_aec,testFile=test_ns)
        aecm_mos = compute_audio_quality('POLQA',refFile=test_ns,testFile=test_aecm)
        agc_mos = compute_audio_quality('POLQA',refFile=test_aecm,testFile=test_agc)
        agc2_mos = compute_audio_quality('POLQA',refFile=test_agc,testFile=test_agc2)
        post_mos = compute_audio_quality('POLQA',refFile=test_agc2,testFile=test_post)


        file2lowcut_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_lowcut)
        file2aec_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_aec)
        file2ns_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_ns)
        file2aecm_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_aecm)
        file2agc_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_agc)
        file2agc2_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_agc2)
        file2post_mos = compute_audio_quality('POLQA',refFile=file,testFile=test_post)

        sheet1.write(3, 2 * i + 1, float(lowcut_mos['mos']))
        sheet1.write(4, 2 * i + 1, float(aec_mos['mos']))
        sheet1.write(5, 2 * i + 1, float(ns_mos['mos']))
        sheet1.write(6, 2 * i + 1, float(aecm_mos['mos']))
        sheet1.write(7, 2 * i + 1, float(agc_mos['mos']))
        sheet1.write(8, 2 * i + 1, float(agc2_mos['mos']))
        sheet1.write(9, 2 * i + 1, float(post_mos['mos']))

        sheet1.write(11, 2 * i + 1, float(file2lowcut_mos['mos']))
        sheet1.write(12, 2 * i + 1, float(file2aec_mos['mos']))
        sheet1.write(13, 2 * i + 1, float(file2ns_mos['mos']))
        sheet1.write(14, 2 * i + 1, float(file2aecm_mos['mos']))
        sheet1.write(15, 2 * i + 1, float(file2agc_mos['mos']))
        sheet1.write(16, 2 * i + 1, float(file2agc2_mos['mos']))
        sheet1.write(17, 2 * i + 1, float(file2post_mos['mos']))
    sheet1.write(3, 0, 'lowcut_mos')
    sheet1.write(4, 0, 'aec_mos')
    sheet1.write(5, 0, 'ns_mos')
    sheet1.write(6, 0, 'aecm_mos')
    sheet1.write(7, 0, 'agc_mos')
    sheet1.write(8, 0, 'agc2_mos')
    sheet1.write(9, 0, 'post_mos')

    sheet1.write(11, 0, 'ori2lowcut_mos')
    sheet1.write(12, 0, 'ori2aec_mos')
    sheet1.write(13, 0, 'ori2ns_mos')
    sheet1.write(14, 0, 'ori2aecm_mos')
    sheet1.write(15, 0, 'ori2agc_mos')
    sheet1.write(16, 0, 'ori2agc2_mos')
    sheet1.write(17, 0, 'ori2post_mos')
    wk1.save(r'E:\\3a_auto_test_porject\\WZQ\\noaecinitial_mos_scores.xls')
    # file = r'C:\Users\vcloud_avl\Downloads\agc_eva\speech_gaintable.wav'
    # test = r'C:\Users\vcloud_avl\Downloads\agc_eva\test.wav'
    # lim,gain_table,DR = compute_audio_quality('GAINTABLE',refFile=file,testFile=test,audioType=1)
    # print(lim,gain_table[0],DR[2])
    # for a in gain_table:
    #     print(a)
    # for a in DR:
    #     print(a)
    #
    # file = r'C:\Users\vcloud_avl\Downloads\agc_eva\music_stability_.wav'
    # test = r'C:\Users\vcloud_avl\Downloads\agc_eva\test_music_stability.wav'
    # res = compute_audio_quality('MUSICSTA',refFile=file, testFile=test)
    # for a in res:
    #     print(a)
    #
    # file = r'C:\Users\vcloud_avl\Downloads\agc_eva\speech_gaintable.wav'
    # test = r'C:\Users\vcloud_avl\Downloads\agc_eva\test.wav'
    # delay = compute_audio_quality('AGCDELAY',refFile=file,testFile=test)
    # print(delay)
    #
    # compute_audio_quality('MATCH',refFile=file,testFile=test,outFile='out.wav',audioType=1)