import tarfile
import requests
import zstandard as zstd


# 下载文件
def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # 检查请求是否成功

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {output_path}")


# 解压zst文件
def decompress_zst(input_path, output_path):
    with open(input_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        with open(output_path, 'wb') as output_file:
            dctx.copy_stream(compressed_file, output_file)
    print(f"Decompressed to {output_path}")


# 解压tar文件，显式传递 filter 参数
def extract_tar(tar_path, extract_path):
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=extract_path, filter=None)  # 显式禁用过滤器，避免警告
    print(f"Extracted {tar_path} to {extract_path}")


if __name__ == "__main__":
    vndb_url = "https://dl.vndb.org/dump/vndb-db-latest.tar.zst"
    tar_zst_path = "vndb-db-latest.tar.zst"
    tar_path = "vndb-db-latest.tar"
    extract_dir = "./vndb_data"

    # 下载文件
    download_file(vndb_url, tar_zst_path)

    # 解压 zst 文件到 tar 文件
    decompress_zst(tar_zst_path, tar_path)

    # 解压 tar 文件
    extract_tar(tar_path, extract_dir)
