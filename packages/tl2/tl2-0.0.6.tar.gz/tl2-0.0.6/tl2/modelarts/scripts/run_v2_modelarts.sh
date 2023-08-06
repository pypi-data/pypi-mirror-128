set -x

# v2
# "bash $PROJ_NAME/tl2_lib/tl2/modelarts/scripts/run_v2_modelarts.sh 1 bucket-3690"

# bash tl2_lib/tl2/modelarts/scripts/run_v2_modelarts.sh 0 bucket-3690

# Env vars e.g.
# PROJ_NAME=CIPS-exp

run_num=${1:-0}
bucket=${2:-bucket-3690}
cuda_devices=${3:-0,1,2,3,4,5,6,7}

#curdir: /home/ma-user/modelarts/user-job-dir
pwd
ls -la

proj_root=$PROJ_NAME

############ copy code
cd $proj_root
## modelarts code
python tl2_lib/tl2/modelarts/scripts/copy_tool.py \
  -s s3://$bucket/ZhouPeng/codes/$proj_root \
  -d ../$proj_root \
  -t copytree -b ../$proj_root/code.zip
## cache code
#bucket=bucket-3690 && proj_root=CIPS-exp
python tl2_lib/tl2/modelarts/scripts/copy_tool.py \
  -s s3://$bucket/ZhouPeng/codes/$proj_root \
  -d /cache/$proj_root \
  -t copytree -b /cache/$proj_root/code.zip

# replace modelarts start file
#cp /cache/$proj_root/exp/dev/nerf_inr/bash_v2/train_ffhq_freeze_nerf_photo2cartoon_r256.sh \
#   exp/dev/nerf_inr/bash_v2/train_ffhq_freeze_nerf_metfaces_r256.sh

cd /cache/$proj_root
pwd
############ Prepare envs
#cp tl2_lib/tl2/modelarts/sources/pip.conf.modelarts /root/.pip/pip.conf
#cp tl2_lib/tl2/modelarts/sources/sources.list.modelarts /etc/apt/sources.list
        python tl2_lib/tl2/modelarts/scripts/copy_tool.py \
          -s s3://$bucket/ZhouPeng/pypi/torch182_cu101_py36 -d /cache/pypi -t copytree
        for filename in /cache/pypi/*.whl; do
            pip install $filename
        done
pip install -e tl2_lib
#pip install torch==1.8.2+cu102 torchvision==0.9.2+cu102 torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
pip install --no-cache-dir easydict fvcore tensorboard tqdm opencv-python matplotlib scikit-video plyfile mrcfile
pip install --no-cache-dir streamlit ninja
#pip install -e torch_fidelity_lib

############ copy results
#resume_dir=outdir/train_ffhq_r128_partial_grad-20210920_165510_097_grad96
#python tl2_lib/tl2/modelarts/scripts/copy_tool.py \
#  -s s3://$bucket/ZhouPeng/results/$proj_root/$resume_dir \
#  -d /cache/$proj_root/results/$resume_dir -t copytree


export CUDA_VISIBLE_DEVICES=$cuda_devices
export PORT=12345
export TIME_STR=1
export RUN_NUM=${run_num}
export PYTHONPATH=.

python -c "from tl2_lib.tl2.modelarts.tests.test_run import TestingRun;\
  TestingRun().test_run_v2_modelarts(debug=False)" \
  --tl_opts root_obs s3://$bucket/ZhouPeng/


