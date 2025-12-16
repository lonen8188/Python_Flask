from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    # 파일 업로드에 필요한 밸리데이션을 설정한다
    image = FileField(
        validators=[
            FileRequired("이미지 파일을 지정해 주세요."),
            FileAllowed(["png", "jpg", "jpeg"], "지원되지 않는 이미지 형식입니다."),
        ]
    )
    submit = SubmitField("업로드")  # p210까지 추가


# p220 추가 물체감지기능의 폼 클래스 만들기
class DetectorForm(FlaskForm):
    submit = SubmitField("감지")


# 물체 감지 기능을 구현하기 위해 PyTorch라는 머신러능 라이브러리를 사용한다.
# 페이스북에서 개발을 주도한 파이썬 전용 라이브러리로
# pip install torch torchvision opencv-python으로 설치한다.
# 설치를 실패하는 경우 pip install --upgrade pip를 진행 후 재설치 한다.

# 설치후에 학습이 완료된 파일을 이용하여 진행한다.
# 현재는 사람, 강아지, 자동차가 가능한 model.pt파일을 사용한다.
# 콘솔 python 실행
# import torch -> 오류발생 그래픽카드 드라이버 원인 -> exit()
# 드라이버 확인 : nvidia-smi
# Tue Dec 16 12:50:38 2025
# +-----------------------------------------------------------------------------------------+
# | NVIDIA-SMI 581.57                 Driver Version: 581.57         CUDA Version: 13.0     |
# +-----------------------------------------+------------------------+----------------------+
# | GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
# |                                         |                        |               MIG M. |
# |=========================================+========================+======================|
# |   0  NVIDIA GeForce GTX 1060 3GB  WDDM  |   00000000:01:00.0  On |                  N/A |
# | 25%   45C    P8             12W /  120W |     738MiB /   3072MiB |     29%      Default |
# |                                         |                        |                  N/A |
# +-----------------------------------------+------------------------+----------------------+

# +-----------------------------------------------------------------------------------------+
# | Processes:                                                                              |
# |  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
# |        ID   ID                                                               Usage      |
# |=========================================================================================|
# |    0   N/A  N/A            1080    C+G   C:\Windows\System32\dwm.exe           N/A      |
# |    0   N/A  N/A            5840    C+G   ...Chrome\Application\chrome.exe      N/A      |
# |    0   N/A  N/A            6088    C+G   C:\Windows\System32\mstsc.exe         N/A      |
# |    0   N/A  N/A            7204    C+G   C:\Windows\explorer.exe               N/A      |
# |    0   N/A  N/A            8452    C+G   ... Files\Veyon\veyon-server.exe      N/A      |
# |    0   N/A  N/A            9080    C+G   ...h_cw5n1h2txyewy\SearchApp.exe      N/A      |
# |    0   N/A  N/A            9884    C+G   ...5n1h2txyewy\TextInputHost.exe      N/A      |
# |    0   N/A  N/A           10824    C+G   ...p\Systray\AzureArcSysTray.exe      N/A      |
# |    0   N/A  N/A           14488    C+G   ...xyewy\ShellExperienceHost.exe      N/A      |
# |    0   N/A  N/A           14792    C+G   ...ms\Microsoft VS Code\Code.exe      N/A      |
# |    0   N/A  N/A           14896    C+G   ...Chrome\Application\chrome.exe      N/A      |
# +-----------------------------------------------------------------------------------------+

# GPU: GTX 1060 3GB (Pascal, Compute Capability 6.1)

# 드라이버: 581.57 (아주 최신)
# 표시 CUDA: 13.0
# 문제: 최신 PyTorch(CUDA 12.x 이상) ↔ GTX 1060 아키텍처 미지원
# 👉 GTX 1060은 CUDA 12.x / 13.x PyTorch에서 공식적으로 지원이 끊긴 상태입니다.
# 그래서: PyTorch 다운그레이드
# pip uninstall torch torchvision torchaudio -y
# CUDA 11.8 전용 PyTorch 설치
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 콘솔 python 실행
# import torch
# import torchvision
# model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
# torch.save(model, "model.pt")


# p234 이미지 삭제용 추가
class DeleteForm(FlaskForm):
    submit = SubmitField("삭제")
