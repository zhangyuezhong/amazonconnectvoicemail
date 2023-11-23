import struct
def convert_bytearray_to_wav(samples):
    length = len(samples)

    # Single 16bit PCM 8000Hz、ビットオーダーはリトルエンディアン
    channel = 1
    bit_par_sample = 16
    format_code = 1
    sample_rate = 8000

    header_size = 44
    wav = bytearray()

    # RIFFチャンク
    wav[0:4] = b'RIFF'                                          # チャンクID
    wav[4:8] = struct.pack('<I', length + header_size -
                           12)     # ファイルサイズ (このチャンクを含まない)
    wav[8:12] = b'WAVE'                                         # Wave ID

    # fmtチャンク
    wav[12:16] = b'fmt '                                # チャンクID
    wav[16:20] = struct.pack('<I', 16)                  # fmtチャンクのバイト数
    wav[20:22] = struct.pack('<H', format_code)         # フォーマットコード
    wav[22:24] = struct.pack('<H', channel)             # チャンネル数
    wav[24:28] = struct.pack('<I', sample_rate)         # サンプリングレート
    wav[28:32] = struct.pack('<I', sample_rate * 2)     # データ速度
    wav[32:34] = struct.pack('<H', 2)                   # ブロックサイズ
    wav[34:36] = struct.pack('<H', bit_par_sample)      # サンプルあたりのビット数

    # dataチャンク
    wav[36:40] = b'data'                                # チャンクID
    wav[40:44] = struct.pack('<I', length)              # 波形データのバイト数

    offset = header_size
    for i in range(0, length, 4):
        value = struct.unpack('<I', samples[i:i+4])[0]
        wav[offset:offset+4] = struct.pack('<I', value)
        offset += 4

    return wav
