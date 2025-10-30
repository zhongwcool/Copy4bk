import os
import shutil
from pathlib import Path
from datetime import datetime
try:
    import msvcrt  # Windows: 支持任意键退出
except Exception:
    msvcrt = None


def print_intro():
    print("===============================")
    print(" Copy4bk - 自动复制最新版本文件工具")
    print("===============================")
    print("主要功能：")
    print("- 自动识别每个子目录中最新修改的文件")
    print("- 保持源目录的子目录结构")
    print("- 支持多目标目录一次性复制")
    print("- 复制保留文件时间戳")
    print("- 详细日志输出，便于排查")
    print("")

def read_config(config_file='copy4bk.txt'):
    """
    从配置文件中读取源目录和目标目录（支持多目标目录）
    支持格式：
    1) 键值对：source=路径；target=路径（可写多行）；targets=路径1,路径2
    2) 简单格式：第一行是源目录；之后每一行都是一个目标目录
    """
    if not os.path.exists(config_file):
        print(f"配置文件不存在: {config_file}")
        return None, []

    source_dir = None
    target_dirs = []

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip().strip('"').strip("'")

                if key in ['源目录', 'source', '源路径', 'a目录', 'a']:
                    source_dir = value
                elif key in ['目标目录', 'target', '目标路径', 'b目录', 'b']:
                    # 单个目标目录（可多行重复出现）
                    if value:
                        target_dirs.append(value)
                elif key in ['目标目录们', '目标列表', 'targets']:
                    # 多个目标目录，逗号/分号分隔
                    parts = [p.strip() for p in value.replace('；', ';').replace('，', ',').replace(';', ',').split(',')]
                    target_dirs.extend([p for p in parts if p])
            else:
                # 简单格式：第一行为源目录，其余每行为一个目标目录
                if source_dir is None:
                    source_dir = line.strip().strip('"').strip("'")
                else:
                    target_dirs.append(line.strip().strip('"').strip("'"))

    except Exception as e:
        print(f"读取配置文件失败: {str(e)}")
        return None, []

    # 兼容旧格式：如果未提供目标列表但存在单个target（历史逻辑），保持兼容
    # 去重并保持顺序
    dedup = []
    seen = set()
    for td in target_dirs:
        if td not in seen:
            dedup.append(td)
            seen.add(td)

    return source_dir, dedup


def get_latest_files_in_dir(source_dir):
    """
    获取目录中最新版本的文件
    返回修改时间最新的文件列表
    """
    files = []
    if not os.path.exists(source_dir):
        return files
    
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            files.append(item_path)
    
    if not files:
        return []
    
    # 按修改时间排序，获取最新修改的文件时间
    files_with_time = [(f, os.path.getmtime(f)) for f in files]
    files_with_time.sort(key=lambda x: x[1], reverse=True)
    
    # 获取最新修改时间
    latest_time = files_with_time[0][1]
    
    # 返回所有具有最新修改时间的文件（可能有多个文件在同一时间修改）
    latest_files = [f for f, t in files_with_time if t == latest_time]
    
    return latest_files


def copy_latest_files(source_dir, target_dir):
    """
    将源目录下每个子目录中的最新版本文件复制到目标目录的对应子目录中
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        print(f"源目录不存在: {source_dir}")
        return
    
    # 创建目标目录（如果不存在）
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 遍历源目录下的每个子目录
    for subdir in source_path.iterdir():
        if subdir.is_dir():
            subdir_name = subdir.name
            print(f"\n处理子目录: {subdir_name}")
            
            # 获取该子目录中的最新文件
            latest_files = get_latest_files_in_dir(str(subdir))
            
            if not latest_files:
                print(f"  子目录 {subdir_name} 中没有找到文件")
                continue
            
            # 创建目标子目录
            target_subdir = target_path / subdir_name
            target_subdir.mkdir(parents=True, exist_ok=True)
            
            # 复制最新文件到目标子目录
            for file_path in latest_files:
                file_name = os.path.basename(file_path)
                target_file = target_subdir / file_name
                
                try:
                    shutil.copy2(file_path, target_file)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"  已复制: {file_name} (修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
                except Exception as e:
                    print(f"  复制失败 {file_name}: {str(e)}")


if __name__ == '__main__':
    def wait_for_keypress():
        try:
            if msvcrt is not None:
                print("\n按任意键退出...")
                msvcrt.getch()
                return
            # 非 Windows 兜底
            input("\n按回车键退出...")
        except Exception:
            pass

    try:
        print_intro()
        # 从配置文件读取源目录和目标目录们
        source_directory, target_directories = read_config('copy4bk.txt')

        if not source_directory or not target_directories:
            print("错误：无法从配置文件读取源目录或目标目录！")
            print("\n请确保配置文件 copy4bk.txt 存在且格式正确。")
        else:
            print("开始复制最新版本文件...")
            print(f"源目录: {source_directory}")
            print("目标目录:")
            for idx, td in enumerate(target_directories, 1):
                print(f"  {idx}. {td}")

            for td in target_directories:
                print(f"\n=> 正在处理目标目录: {td}")
                copy_latest_files(source_directory, td)

            print("\n全部目标目录处理完成！")
    finally:
        wait_for_keypress()
