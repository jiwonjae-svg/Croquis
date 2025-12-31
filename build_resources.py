"""
리소스 빌더 스크립트
btn 폴더의 이미지를 암호화하여 resources.dat와 embedded_resources.py에 저장
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet
from pathlib import Path

# 암호화 키 생성
key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
fernet = Fernet(key)

def build_resources():
    """btn 폴더의 이미지를 resources.dat에 저장"""
    btn_dir = Path(__file__).parent / "btn"
    dat_dir = Path(__file__).parent / "dat"
    dat_dir.mkdir(exist_ok=True)
    
    resources = {}
    
    # btn 폴더의 모든 PNG 파일 읽기
    for img_file in btn_dir.glob("*.png"):
        with open(img_file, "rb") as f:
            image_data = f.read()
        
        # 파일명을 키로 사용 (확장자 제외)
        key_name = img_file.stem
        resources[key_name] = base64.b64encode(image_data).decode()
        print(f"Added: {key_name}")
    
    # JSON으로 직렬화하고 암호화
    import json
    json_data = json.dumps(resources, ensure_ascii=False)
    encrypted = fernet.encrypt(json_data.encode())
    
    # resources.dat에 저장
    resources_file = dat_dir / "resources.dat"
    with open(resources_file, "wb") as f:
        f.write(encrypted)
    
    print(f"\nresources.dat created: {resources_file}")
    print(f"Total resources: {len(resources)}")
    
    # embedded_resources.py 생성
    generate_embedded_module(resources)

def generate_embedded_module(resources):
    """내장 리소스 모듈 생성"""
    output_file = Path(__file__).parent / "embedded_resources.py"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('내장 리소스 모듈\n')
        f.write('resources.dat가 없거나 손상되었을 때 사용하는 백업 리소스\n')
        f.write('"""\n\n')
        f.write('# 이 파일은 자동 생성되었습니다. 수동으로 편집하지 마세요.\n\n')
        f.write('EMBEDDED_RESOURCES = {\n')
        
        for key, data in resources.items():
            # 긴 base64 문자열을 여러 줄로 나누기
            lines = [data[i:i+80] for i in range(0, len(data), 80)]
            f.write(f'    "{key}": (\n')
            for line in lines[:-1]:
                f.write(f'        "{line}"\n')
            f.write(f'        "{lines[-1]}"\n')
            f.write('    ),\n')
        
        f.write('}\n')
    
    print(f"embedded_resources.py created: {output_file}")

if __name__ == "__main__":
    build_resources()
