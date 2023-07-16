import GPUtil
import psutil
import cpuinfo

def recommend_model(mem):
    mem = int(mem)
    if mem >= 65:
        return '65B, q8_0'
    elif mem >= 46:
        return '65B, q5_1'
    elif mem >= 38:
        return '65B, q4_1'
    elif mem >= 33:
        return '33B, q8_0'
    elif mem >= 24:
        return '33B, q5_1'
    elif mem >= 20:
        return '33B, q4_1'
    elif mem >= 13:
        return '13B, q8_0'
    elif mem >= 10:
        return '13B, q5_1'
    elif mem >= 8:
        return '13B, q4_1'
    elif mem >= 7:
        return '7B, q8_0'
    elif mem >= 5:
        return '7B, q5_1'
    elif mem >= 4:
        return '7B, q4_1'
    else:
        return ''

def system_info():
    GPUs = GPUtil.getGPUs()
    n_gpus = len(GPUs)
    device_type = ''
    gpus = ''
    model_name = ''

    if n_gpus > 0:
        device_type = 'gpu'
        gpus = ','.join([str(gpu.id) for gpu in GPUs])

        avail_mem = []
        mem_total = []
        for gpu in GPUs:
            avail_mem.append(gpu.memoryFree)
            mem_total.append(gpu.memoryTotal)

        avail_mem = sum(avail_mem) * 0.9 / 1024  # Convert from MB to GB
        total_mem = sum(mem_total) * 0.9 / 1024  # Convert from MB to GB

        model_name = recommend_model(avail_mem)
    else:
        mem_info = psutil.virtual_memory()
        total_mem = mem_info.total / (1024 ** 3)  # Convert from bytes to GB
        avail_mem = mem_info.available * 0.75 / (1024 ** 3)  # Convert from bytes to GB

        device_type = 'mps' if 'Apple' in cpuinfo.get_cpu_info().get('brand_raw') else 'cpu'
        model_name = recommend_model(avail_mem)

    return model_name, device_type, gpus

if __name__ == '__main__':
    model_name, device_type, gpus = system_info()
    print("Model Name: ", model_name)
    print("Device Type: ", device_type)
    print("GPU IDs: ", gpus)

