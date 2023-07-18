import GPUtil
import psutil
import cpuinfo

def recommend_model(mem, device_type):
    model = ''
    instructions = ''
    mem = int(mem)
    if device_type == 'gpu':
        if mem >= 34:
            model = 'TheBloke/guanaco-65B-GPTQ'
        elif mem >= 17:
            model = 'TheBloke/guanaco-33B-GPTQ'
        elif mem >= 8:
            model = 'TheBloke/guanaco-13B-GPTQ'
        elif mem >= 4:
            model = 'TheBloke/guanaco-7B-GPTQ'
        else:
            model = ''
        instructions = f"In the text-generation-webui folder, run\n  python download-model.py {model}"
    else:
        if mem >= 47:
            model = 'https://huggingface.co/TheBloke/guanaco-65B-GGML/resolve/main/guanaco-65B.ggmlv3.q5_K_M.bin'
        elif mem >= 40:
            model = 'https://huggingface.co/TheBloke/guanaco-65B-GGML/resolve/main/guanaco-65B.ggmlv3.q4_K_M.bin'
        elif mem >= 27:
            model = 'https://huggingface.co/TheBloke/guanaco-65B-GGML/resolve/main/guanaco-65B.ggmlv3.q2_K.bin'
        elif mem >= 23:
            model = 'https://huggingface.co/TheBloke/guanaco-33B-GGML/resolve/main/guanaco-33B.ggmlv3.q5_K_S.bin'
        elif mem >= 18:
            model = 'https://huggingface.co/TheBloke/guanaco-33B-GGML/resolve/main/guanaco-33B.ggmlv3.q3_K_L.bin'
        elif mem >= 16:
            model = 'https://huggingface.co/TheBloke/guanaco-33B-GGML/resolve/main/guanaco-33B.ggmlv3.q3_K_M.bin'
        elif mem >= 14:
            model = 'https://huggingface.co/TheBloke/guanaco-33B-GGML/resolve/main/guanaco-33B.ggmlv3.q2_K.bin'
        elif mem >= 11:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q6_K.bin'
        elif mem >= 10:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q5_1.bin'
        elif mem >= 9:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q5_0.bin'
        elif mem >= 8:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q4_K_M.bin'
        elif mem >= 7:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q3_K_L.bin'
        elif mem >= 6:
            model = 'https://huggingface.co/TheBloke/guanaco-13B-GGML/resolve/main/guanaco-13B.ggmlv3.q3_K_S.bin'
        elif mem >= 5:
            model = 'https://huggingface.co/TheBloke/guanaco-7B-GGML/resolve/main/guanaco-7B.ggmlv3.q5_K_M.bin'
        elif mem >= 4:
            model = 'https://huggingface.co/TheBloke/guanaco-7B-GGML/resolve/main/guanaco-7B.ggmlv3.q4_K_S.bin'
        elif mem >= 3:
            model = 'https://huggingface.co/TheBloke/guanaco-7B-GGML/resolve/main/guanaco-7B.ggmlv3.q3_K_S.bin'
        else:
            model = ''
        instructions = f"In the text-generation-webui folder, download the following to the 'models' folder\n  {model}"
    return model, instructions

def system_info():
    GPUs = GPUtil.getGPUs()
    total_mem = -1
    avail_mem = -1
    n_gpus = len(GPUs)
    device_type = ''
    gpus = ''
    total_model_name = ''
    avail_model_name = ''
    if n_gpus > 0:
        device_type = 'gpu'
        gpus = ','.join([str(gpu.id) for gpu in GPUs])

        avail_mem = []
        mem_total = []
        for gpu in GPUs:
            avail_mem.append(gpu.memoryFree)
            mem_total.append(gpu.memoryTotal)

        total_mem = sum(mem_total) * 0.9 / 1024  # Convert from MB to GB
        avail_mem = sum(avail_mem) * 0.9 / 1024  # Convert from MB to GB

    else:
        mem_info = psutil.virtual_memory()
        total_mem = mem_info.total / (1024 ** 3)  # Convert from bytes to GB
        avail_mem = mem_info.available * 0.75 / (1024 ** 3)  # Convert from bytes to GB

        device_type = 'mps' if 'Apple' in cpuinfo.get_cpu_info().get('brand_raw') else 'cpu'

    total_model_name, total_inst = recommend_model(total_mem, device_type)
    avail_model_name, avail_inst = recommend_model(avail_mem, device_type)

    return device_type, total_mem, avail_mem, total_model_name, total_inst, avail_model_name, avail_inst, gpus

if __name__ == '__main__':
    device_type, total_mem, avail_mem, total_model_name, total_inst, avail_model_name, avail_inst, gpus = system_info()
    print("Detected device: ", device_type)
    print(f"Detected total memory: {total_mem}; Detected available memory: {avail_mem}")
    print(f"Recommended model for total memory: {total_model_name}")
    print(f"  {total_inst}")
    print(f"Recommended model for available memory: {avail_model_name}")
    print(f"  {avail_inst}")
    print("GPU IDs: ", gpus)
